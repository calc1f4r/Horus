"""Offline evaluation of declared review records, with explicit unknowns."""
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

from .schema import is_identifier

ASSESSMENTS = {
    'eligibility': {'unknown', 'eligible', 'ineligible'},
    'delivery': {'unknown', 'delivered', 'missing'},
    'provisional_presence': {'unknown', 'present', 'absent'},
    'closure': {'unknown', 'bounded', 'unbounded', 'not-applicable'},
    'grading': {'unknown', 'rubric-consistent', 'severity-error', 'claim-understated', 'claim-overstated', 'venue-rule-difference', 'insufficient-match', 'unresolved'},
}
for statuses in ASSESSMENTS.values():
    statuses.add('unresolved')
SEVERITIES = {'critical', 'high', 'medium', 'low', 'informational'}


def keys(obj, fields, label):
    if not isinstance(obj, dict) or set(obj) != set(fields):
        raise ValueError(f'{label}: fields must be exactly {sorted(fields)}')


def strings(value, label, identifiers=False):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(f'{label}: expected nonempty strings in an array')
    if len(value) != len(set(value)) or (identifiers and any(not is_identifier(x) for x in value)):
        raise ValueError(f'{label}: duplicate or noncanonical identifiers')
    return value


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label}: expected nonempty text')


def indexed(rows, fields, label):
    if not isinstance(rows, list):
        raise ValueError(f'{label}: expected an array')
    result = {}
    for row in rows:
        keys(row, fields, label)
        key = row['id']
        if not is_identifier(key) or key in result:
            raise ValueError(f'{label}: duplicate or noncanonical ID')
        result[key] = row
    return result


def sources_valid(rows, root):
    sources = indexed(rows, {'id', 'path', 'sha256', 'revision', 'line_start', 'line_end'}, 'source')
    root = Path(root).resolve()
    for row in sources.values():
        nonempty(row['revision'], 'source revision')
        nonempty(row['path'], 'source path')
        path = Path(row['path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Source path must stay within the archived evidence root')
        path = (root / path).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Source path does not resolve inside evidence root')
        if not isinstance(row['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', row['sha256']):
            raise ValueError('Source hash must be lowercase SHA256')
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError('Archived source changed: ' + row['id'])
        start, end = row['line_start'], row['line_end']
        count = (len(data.split(b'\n')) - (1 if data.endswith(b'\n') else 0)) if data else 0
        if type(start) is not int or type(end) is not int or not 1 <= start <= end <= count:
            raise ValueError('Source line range is invalid: ' + row['id'])
    return sources


def assess(row, field, sources):
    keys(row, {'status', 'authority', 'reviewer_id', 'basis_ids', 'reason', 'coverage', 'scope', 'limitations'}, 'assessment ' + field)
    if row['status'] not in ASSESSMENTS[field] or row['authority'] not in {'unknown', 'reported', 'human'}:
        raise ValueError('Unknown assessment status/authority')
    if row['coverage'] not in {'unknown', 'partial', 'complete'}:
        raise ValueError('Unknown evidence coverage')
    nonempty(row['reason'], 'assessment reason')
    if not isinstance(row['scope'], str) or not isinstance(row['limitations'], str):
        raise ValueError('Assessment scope/limitations must be strings')
    basis = strings(row['basis_ids'], 'assessment basis', True)
    if not set(basis) <= set(sources):
        raise ValueError('Unknown assessment source')
    if row['status'] == 'unknown':
        if row['authority'] != 'unknown' or row['reviewer_id'] is not None or row['coverage'] != 'unknown':
            raise ValueError('Unknown assessments cannot claim completed review')
        return 'unknown'
    if row['authority'] == 'unknown' or not basis or not is_identifier(row['reviewer_id']):
        raise ValueError('A substantive assessment requires attributed evidence')
    nonempty(row['scope'], 'assessment scope')
    if row['coverage'] == 'unknown':
        raise ValueError('A substantive assessment requires stated evidence coverage')
    if row['coverage'] == 'partial':
        nonempty(row['limitations'], 'partial-review limitations')
    # Reported interpretations remain visible but never become verified stages.
    if row['authority'] == 'reported' or row['status'] == 'unresolved':
        return 'unknown'
    if (field, row['status']) in {('delivery', 'missing'), ('provisional_presence', 'absent')} and row['coverage'] != 'complete':
        raise ValueError('Absence conclusions require complete evidence for the declared scope')
    if row['coverage'] == 'partial' and field != 'closure':
        return 'unknown'
    return row['status']


def evaluate(payload, inventory, inventory_sha256, evidence_root):
    keys(inventory, {'schema_version', 'cases'}, 'inventory')
    keys(payload, {'schema_version', 'inventory_sha256', 'observation_unit', 'sources', 'cases'}, 'payload')
    if type(inventory['schema_version']) is not int or inventory['schema_version'] != 1 or type(payload['schema_version']) is not int or payload['schema_version'] != 1:
        raise ValueError('Schema version must be integer 1')
    if not re.fullmatch('[0-9a-f]{64}', str(inventory_sha256)) or payload['inventory_sha256'] != inventory_sha256:
        raise ValueError('External inventory hash mismatch')
    nonempty(payload['observation_unit'], 'observation unit')
    expected = indexed(inventory['cases'], {'id', 'cohort', 'reference_severity', 'included', 'exclusion_reason', 'exclusion_basis_ids'}, 'inventory case')
    if not expected:
        raise ValueError('An evaluation inventory must contain at least one case')
    for row in expected.values():
        nonempty(row['cohort'], 'cohort')
        if row['reference_severity'] not in SEVERITIES or type(row['included']) is not bool:
            raise ValueError('Invalid inventory severity/inclusion')
    actual = indexed(payload['cases'], {'id', 'owner_label', 'matched_candidate_ids', 'label_basis_ids', 'claimed_severities', 'reported_annotation', 'annotation_basis_ids', 'assessments'}, 'case')
    if set(expected) != set(actual):
        raise ValueError('Cases must exactly conserve the external inventory')
    sources = sources_valid(payload['sources'], evidence_root)
    for row in expected.values():
        basis = strings(row['exclusion_basis_ids'], 'exclusion basis', True)
        if not isinstance(row['exclusion_reason'], str) or not set(basis) <= set(sources):
            raise ValueError('Invalid exclusion reason/basis')
        if not row['included'] and (not row['exclusion_reason'].strip() or not basis):
            raise ValueError('Excluded cases need reason and archived basis')
    grouped = defaultdict(list)
    dispositions = []
    for key, row in sorted(actual.items()):
        if row['owner_label'] not in {'matched', 'unmatched', 'unknown'}:
            raise ValueError('Unknown owner label')
        candidates = strings(row['matched_candidate_ids'], 'candidate IDs', True)
        if bool(candidates) != (row['owner_label'] == 'matched'):
            raise ValueError('Matched owner label and candidate inventory disagree')
        basis = strings(row['label_basis_ids'], 'label basis', True)
        if not basis or not set(basis) <= set(sources):
            raise ValueError('Owner labels require resolving source references')
        strings(row['claimed_severities'], 'claimed grades')
        if not isinstance(row['reported_annotation'], str):
            raise ValueError('Reported annotation must be text')
        keys(row['assessments'], ASSESSMENTS, 'assessments')
        annotation_basis = strings(row['annotation_basis_ids'], 'annotation basis', True)
        if not set(annotation_basis) <= set(sources) or (row['reported_annotation'] and not annotation_basis):
            raise ValueError('Reported annotations need archived basis')
        effective = {}
        for field, value in row['assessments'].items():
            try:
                effective[field] = assess(value, field, sources)
            except ValueError as error:
                raise ValueError(f'Case {key}, assessment {field}: {error}') from error
        if effective['eligibility'] == 'ineligible':
            stage = 'ineligible-matched' if row['owner_label'] == 'matched' else 'ineligible'
        elif row['owner_label'] == 'matched':
            stage = 'owner-matched'
        elif row['owner_label'] == 'unknown' or effective['eligibility'] == 'unknown':
            stage = 'unknown'
        elif effective['delivery'] == 'missing':
            stage = 'delivery-missing'
        elif effective['delivery'] != 'delivered':
            stage = 'unknown'
        elif effective['provisional_presence'] == 'absent':
            stage = 'before-provisional'
        elif effective['provisional_presence'] == 'present':
            stage = 'after-provisional-unlocalized'
        else:
            stage = 'unknown'
        disposition = {'id': key, 'included': expected[key]['included'], 'owner_label': row['owner_label'],
                       'effective_assessments': effective, 'loss_stage': stage,
                       'deferred_human_assessments': {field: dict(value) for field, value in row['assessments'].items() if value['authority'] == 'human' and value['status'] != 'unknown' and effective[field] == 'unknown'},
                       'reported_assessments': {field: dict(value) for field, value in row['assessments'].items() if value['authority'] == 'reported'}}
        dispositions.append(disposition)
        grouped[(expected[key]['cohort'], expected[key]['reference_severity'])].append(disposition)
    summary = []
    for (cohort, severity), all_rows in sorted(grouped.items()):
        rows = [row for row in all_rows if row['included']]
        eligibility = Counter(row['effective_assessments']['eligibility'] for row in rows)
        eligible = [row for row in rows if row['effective_assessments']['eligibility'] == 'eligible']
        unknown = eligibility['unknown']
        reconciliations = sum(row['effective_assessments']['grading'] in {'unknown', 'unresolved', 'insufficient-match', 'severity-error'} for row in eligible if row['owner_label'] == 'matched')
        label_unknown = sum(row['owner_label'] == 'unknown' for row in eligible)
        summary.append({'cohort': cohort, 'reference_severity': severity, 'offered_cases': len(rows),
                        'excluded_cases': len(all_rows) - len(rows),
                        'eligible_matched_cases': sum(row['owner_label'] == 'matched' for row in eligible),
                        'delivery_status_counts': dict(sorted(Counter(row['effective_assessments']['delivery'] for row in rows).items())),
                        'provisional_presence_counts': dict(sorted(Counter(row['effective_assessments']['provisional_presence'] for row in rows).items())),
                        'grading_status_counts': dict(sorted(Counter(row['effective_assessments']['grading'] for row in rows).items())),
                        'closure_status_counts': dict(sorted(Counter(row['effective_assessments']['closure'] for row in rows).items())),
                        'owner_matches': sum(row['owner_label'] == 'matched' for row in rows),
                        'eligible_cases': eligibility['eligible'], 'ineligible_cases': eligibility['ineligible'],
                        'eligibility_unknown': unknown, 'eligible_label_unknown': label_unknown,
                        'eligible_match_reconciliation_pending': reconciliations,
                        'eligible_recall': None if unknown or label_unknown or reconciliations or not eligible else sum(row['owner_label'] == 'matched' for row in eligible) / len(eligible),
                        'loss_stage_counts': dict(sorted(Counter(row['loss_stage'] for row in rows).items()))})
    return {'ok': True, 'observation_unit': payload['observation_unit'], 'inventory_sha256': inventory_sha256,
            'case_count': len(dispositions), 'summary': summary, 'dispositions': dispositions,
            'limitation': 'Structural checks of declared human/reported assessments only. No authentication, semantic adjudication, target execution or measured improvement.'}
