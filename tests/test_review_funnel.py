"""Regression tests for honest unknowns and offline inventory conservation."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.horus_review.funnel import ASSESSMENTS, evaluate


class FunnelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        data = b'Archived record\nExamined scope\n'
        (self.root / 'record.txt').write_bytes(data)
        self.inventory = {'schema_version': 1, 'cases': [{'id': 'case-1', 'cohort': 'local', 'reference_severity': 'medium', 'included': True, 'exclusion_reason': '', 'exclusion_basis_ids': []}]}
        self.hash = hashlib.sha256(json.dumps(self.inventory).encode()).hexdigest()
        self.row = {'id': 'case-1', 'owner_label': 'unmatched', 'matched_candidate_ids': [],
                    'label_basis_ids': ['S1'], 'claimed_severities': [], 'reported_annotation': '', 'annotation_basis_ids': [],
                    'assessments': {field: {'status': 'unknown', 'authority': 'unknown', 'reviewer_id': None,
                                          'basis_ids': [], 'reason': 'Awaiting review', 'coverage': 'unknown',
                                          'scope': '', 'limitations': ''} for field in ASSESSMENTS}}
        self.payload = {'schema_version': 1, 'inventory_sha256': self.hash, 'observation_unit': 'saved-local-records',
                        'sources': [{'id': 'S1', 'path': 'record.txt', 'sha256': hashlib.sha256(data).hexdigest(),
                                     'revision': 'snapshot-1', 'line_start': 1, 'line_end': 2}], 'cases': [self.row]}

    def run_check(self):
        return evaluate(self.payload, self.inventory, self.hash, self.root)

    def assessment(self, field, status, authority='human', coverage='complete'):
        self.row['assessments'][field] = {'status': status, 'authority': authority, 'reviewer_id': 'reviewer-1',
                                        'basis_ids': ['S1'], 'reason': 'Scoped assessment', 'coverage': coverage,
                                        'scope': 'case-1 at snapshot-1', 'limitations': 'Partial evidence' if coverage == 'partial' else ''}

    def test_unmatched_output_does_not_establish_generation_failure(self):
        result = self.run_check()
        self.assertEqual(result['dispositions'][0]['loss_stage'], 'unknown')
        self.assertIsNone(result['summary'][0]['eligible_recall'])

    def test_reported_stage_remains_unverified(self):
        self.assessment('eligibility', 'eligible', 'reported')
        self.assessment('delivery', 'missing', 'reported')
        result = self.run_check()
        self.assertEqual(result['dispositions'][0]['loss_stage'], 'unknown')
        self.assertEqual(result['dispositions'][0]['reported_assessments']['delivery']['status'], 'missing')
        self.assertIsNone(result['summary'][0]['eligible_recall'])
        self.assertIn('limitations', result['dispositions'][0]['reported_assessments']['delivery'])

    def test_human_unresolved_retains_attribution_and_scope(self):
        self.assessment('eligibility', 'unresolved', coverage='partial')
        result = self.run_check()
        recorded = result['dispositions'][0]['deferred_human_assessments']['eligibility']
        self.assertEqual(recorded['reviewer_id'], 'reviewer-1')
        self.assertEqual(recorded['coverage'], 'partial')
        self.assertEqual(result['summary'][0]['eligibility_unknown'], 1)

    def test_matched_but_ineligible_is_visible_without_numerator_confusion(self):
        self.row.update(owner_label='matched', matched_candidate_ids=['candidate-1'])
        self.assessment('eligibility', 'ineligible')
        result = self.run_check()
        self.assertEqual(result['dispositions'][0]['loss_stage'], 'ineligible-matched')
        self.assertEqual(result['summary'][0]['owner_matches'], 1)
        self.assertEqual(result['summary'][0]['eligible_matched_cases'], 0)

    def test_exclusions_require_a_reason_and_archived_basis(self):
        self.inventory['cases'][0]['included'] = False
        with self.assertRaises(ValueError):
            self.run_check()

    def test_partial_absence_conclusion_is_rejected(self):
        for field, status in [('delivery', 'missing'), ('provisional_presence', 'absent')]:
            with self.subTest(field=field):
                self.assessment(field, status, coverage='partial')
                with self.assertRaises(ValueError):
                    self.run_check()
                self.row['assessments'][field]['coverage'] = 'complete'

    def test_partial_closure_requires_visible_limitations(self):
        self.assessment('closure', 'bounded', coverage='partial')
        self.row['assessments']['closure']['limitations'] = ''
        with self.assertRaises(ValueError):
            self.run_check()

    def test_partial_human_assessments_do_not_complete_metrics(self):
        self.assessment('eligibility', 'eligible', coverage='partial')
        result = self.run_check()
        self.assertEqual(result['dispositions'][0]['effective_assessments']['eligibility'], 'unknown')
        self.assertEqual(result['dispositions'][0]['deferred_human_assessments']['eligibility']['status'], 'eligible')
        self.assertIsNone(result['summary'][0]['eligible_recall'])

    def test_declared_delivery_loss_preserves_scope_failure(self):
        self.assessment('eligibility', 'eligible')
        self.assessment('delivery', 'missing')
        result = self.run_check()
        self.assertEqual(result['dispositions'][0]['loss_stage'], 'delivery-missing')
        self.assertEqual(result['summary'][0]['eligible_recall'], 0)

    def test_generation_and_post_generation_are_distinct(self):
        self.assessment('eligibility', 'eligible')
        self.assessment('delivery', 'delivered')
        for status, stage in [('absent', 'before-provisional'), ('present', 'after-provisional-unlocalized'), ('unknown', 'unknown')]:
            with self.subTest(status=status):
                if status == 'unknown':
                    self.row['assessments']['provisional_presence'] = deepcopy(FunnelTests.default_unknown())
                else:
                    self.assessment('provisional_presence', status)
                self.assertEqual(self.run_check()['dispositions'][0]['loss_stage'], stage)

    @staticmethod
    def default_unknown():
        return {'status': 'unknown', 'authority': 'unknown', 'reviewer_id': None, 'basis_ids': [],
                'reason': 'Awaiting review', 'coverage': 'unknown', 'scope': '', 'limitations': ''}

    def test_match_does_not_implicitly_verify_eligibility_or_grading(self):
        self.row.update(owner_label='matched', matched_candidate_ids=['candidate-1'])
        self.assertIsNone(self.run_check()['summary'][0]['eligible_recall'])
        self.assessment('eligibility', 'eligible')
        self.assertIsNone(self.run_check()['summary'][0]['eligible_recall'])
        self.assessment('grading', 'rubric-consistent')
        self.assertEqual(self.run_check()['summary'][0]['eligible_recall'], 1)

    def test_insufficient_match_keeps_original_label_and_defers_metric(self):
        self.row.update(owner_label='matched', matched_candidate_ids=['candidate-1'])
        self.assessment('eligibility', 'eligible')
        self.assessment('grading', 'insufficient-match')
        result = self.run_check()
        self.assertEqual(result['summary'][0]['owner_matches'], 1)
        self.assertIsNone(result['summary'][0]['eligible_recall'])

    def test_external_inventory_detects_deleted_and_added_cases(self):
        self.payload['cases'] = []
        with self.assertRaises(ValueError):
            self.run_check()
        self.row['id'] = 'case-2'; self.payload['cases'] = [self.row]
        with self.assertRaises(ValueError):
            self.run_check()

    def test_duplicate_case_or_source_ids_are_rejected(self):
        for field in ['cases', 'sources']:
            with self.subTest(field=field):
                self.payload[field].append(deepcopy(self.payload[field][0]))
                with self.assertRaises(ValueError):
                    self.run_check()
                self.payload[field].pop()

    def test_unknown_structural_fields_and_missing_assessments_fail(self):
        self.row['assessments']['eligiblity'] = self.row['assessments'].pop('eligibility')
        with self.assertRaises(ValueError):
            self.run_check()

    def test_stale_and_outside_sources_fail(self):
        (self.root / 'record.txt').write_text('Changed\n')
        with self.assertRaises(ValueError):
            self.run_check()
        self.payload['sources'][0]['path'] = '../outside.txt'
        with self.assertRaises(ValueError):
            self.run_check()

    def test_empty_snapshot_boolean_ranges_and_unicode_lines_fail(self):
        source = self.payload['sources'][0]
        for data, start, end in [(b'', 1, 1), (b'one\ntwo\n', True, 2), ('one\u2028two\n'.encode(), 1, 2)]:
            with self.subTest(data=data):
                (self.root / 'record.txt').write_bytes(data)
                source.update(sha256=hashlib.sha256(data).hexdigest(), line_start=start, line_end=end)
                with self.assertRaises(ValueError):
                    self.run_check()

    def test_excluded_cases_remain_in_inventory_but_not_summary(self):
        self.inventory['cases'][0].update(included=False, exclusion_reason='Recorded exclusion', exclusion_basis_ids=['S1'])
        result = self.run_check()
        self.assertEqual(result['case_count'], 1)
        self.assertEqual(result['summary'][0]['excluded_cases'], 1)
        self.assertEqual(result['summary'][0]['offered_cases'], 0)

    def test_versions_inventory_binding_and_empty_inventory_fail(self):
        for change in [lambda: self.payload.update(schema_version=True), lambda: self.payload.update(inventory_sha256='0'*64), lambda: self.inventory.update(cases=[])]:
            original = deepcopy(self.payload), deepcopy(self.inventory)
            change()
            with self.assertRaises(ValueError):
                self.run_check()
            self.payload, self.inventory = original

    def test_cli_rejects_duplicate_keys_and_writes_no_files(self):
        cli = Path(__file__).resolve().parents[1] / 'scripts/review_funnel.py'
        inventory = self.root / 'inventory.json'; ledger = self.root / 'ledger.json'
        inventory.write_text(json.dumps(self.inventory)); ledger.write_text('{"schema_version":1,"schema_version":1}')
        run = subprocess.run([sys.executable, str(cli), str(ledger), '--inventory', str(inventory), '--evidence-root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertFalse(json.loads(run.stdout)['ok'])
        self.assertEqual(set(x.name for x in self.root.iterdir()), {'inventory.json', 'ledger.json', 'record.txt'})


if __name__ == '__main__':
    unittest.main()
