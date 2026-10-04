#!/usr/bin/env python3
"""Unit tests for scripts/db_quality_check.py"""
import os
import sys
import json
import io
import tempfile
import unittest
from contextlib import ExitStack, redirect_stdout
from pathlib import Path
from unittest import mock

# Allow importing from the scripts directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import db_quality_check as qc


VALID_FRONTMATTER = """---
protocol: ethereum
category: oracle
vulnerability_type: price_manipulation
attack_type: flash_loan
affected_component: PriceOracle
severity: high
impact: funds_at_risk
---
## Root Cause
Price is stale.

## Keywords
oracle, price, stale

## Detection Pattern
Check `block.timestamp`.

```solidity
// ❌ Vulnerable
uint price = oracle.getPrice();

// ✅ Secure
require(block.timestamp - oracle.updatedAt < MAX_DELAY);
```
"""

MISSING_FM = """# Just a heading

No frontmatter here.

```solidity
uint x = 1;
```
"""

INVALID_YAML_FM = """---
key: [unclosed bracket
---
## Root Cause
Bad yaml above.
"""

SCHEMA_STRUCTURED_ENTRY = """---
protocol: generic
category: oracle
vulnerability_type: price_manipulation
attack_type: economic_exploit
affected_component: oracle_logic
severity: high
impact: fund_loss
code_keywords:
  - slot0
  - observe
---
# Price Oracle Manipulation

**Root Cause Statement:** The protocol trusts a manipulable spot price for accounting.

#### False Positive Guards

- Safe if: price is only used for UI hints.
- Not this bug when: a long-window TWAP and independent sanity bound protect the sink.

## Vulnerable Pattern Examples

```solidity
// VULNERABLE: Direct spot price drives collateral valuation.
uint256 price = pool.slot0Price();
```
"""

COMPLETE_ENTRY = VALID_FRONTMATTER.replace('category: oracle', '''chain: ethereum
root_cause_family: missing_validation
pattern_key: missing freshness check | oracle | read | valuation
primitives: [timestamp, price_feed]
code_keywords: [updatedAt, MAX_DELAY]
category: oracle''') + '''
## References & Source Reports

Source references require factual verification separately.

#### Agent Quick View

The price is consumed without checking freshness.

#### Valid Bug Signals

The value reaches accounting logic.

#### False Positive Guards

Safe if: an upstream freshness check protects every consumer.
''' + '\n' * 10


def _write_tmp(content: str) -> str:
    """Write content to a temp .md file and return its path."""
    fd, path = tempfile.mkstemp(suffix='.md')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


class TestParseFrontmatter(unittest.TestCase):

    def test_valid_frontmatter_parsed(self):
        path = _write_tmp(VALID_FRONTMATTER)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_fm'])
            self.assertIsNone(r['fm_errors'] or None if not r['fm_errors'] else r['fm_errors'])
            self.assertEqual(r['fm']['severity'], 'high')
            self.assertEqual(r['fm']['category'], 'oracle')
        finally:
            os.unlink(path)

    def test_missing_frontmatter(self):
        path = _write_tmp(MISSING_FM)
        try:
            r = qc.parse_frontmatter(path)
            self.assertFalse(r['has_fm'])
            self.assertIsNone(r['fm'])
        finally:
            os.unlink(path)

    def test_invalid_yaml_records_error(self):
        path = _write_tmp(INVALID_YAML_FM)
        try:
            r = qc.parse_frontmatter(path)
            self.assertFalse(r['has_fm'])
            self.assertTrue(len(r['fm_errors']) > 0)
            self.assertIn('YAML parse error', r['fm_errors'][0])
        finally:
            os.unlink(path)

    def test_detects_vuln_and_secure_markers(self):
        path = _write_tmp(VALID_FRONTMATTER)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_vuln_ex'])
            self.assertTrue(r['has_secure'])
        finally:
            os.unlink(path)

    def test_detects_root_cause_section(self):
        path = _write_tmp(VALID_FRONTMATTER)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_root_cause'])
        finally:
            os.unlink(path)

    def test_detects_keywords_section(self):
        path = _write_tmp(VALID_FRONTMATTER)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_keywords'])
        finally:
            os.unlink(path)

    def test_detects_code_blocks(self):
        path = _write_tmp(VALID_FRONTMATTER)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_code_blocks'])
        finally:
            os.unlink(path)

    def test_no_code_blocks_when_absent(self):
        content = "---\nprotocol: eth\n---\n## Root Cause\nNo code here.\n"
        path = _write_tmp(content)
        try:
            r = qc.parse_frontmatter(path)
            self.assertFalse(r['has_code_blocks'])
        finally:
            os.unlink(path)

    def test_line_count_is_accurate(self):
        content = "line1\nline2\nline3\n"
        path = _write_tmp(content)
        try:
            r = qc.parse_frontmatter(path)
            self.assertEqual(r['lines'], 4)  # split('\n') on "a\nb\nc\n" gives 4 parts
        finally:
            os.unlink(path)

    def test_file_path_returned_in_result(self):
        path = _write_tmp(VALID_FRONTMATTER)
        try:
            r = qc.parse_frontmatter(path)
            self.assertEqual(r['file'], path)
        finally:
            os.unlink(path)

    def test_detects_detection_pattern_section(self):
        path = _write_tmp(VALID_FRONTMATTER)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_detection'])
        finally:
            os.unlink(path)

    def test_detects_structured_schema_without_emoji_markers(self):
        path = _write_tmp(SCHEMA_STRUCTURED_ENTRY)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_root_cause'])
            self.assertTrue(r['has_vuln_ex'])
            self.assertTrue(r['has_secure'])
            self.assertTrue(r['has_keywords'])
        finally:
            os.unlink(path)

    def test_detects_bullet_root_cause_statement(self):
        content = VALID_FRONTMATTER.replace(
            "## Root Cause\nPrice is stale.",
            "- Root cause statement: Price is stale.",
        )
        path = _write_tmp(content)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_root_cause'])
        finally:
            os.unlink(path)

    def test_detects_root_cause_categories_heading(self):
        content = VALID_FRONTMATTER.replace(
            "## Root Cause\nPrice is stale.",
            "#### Root Cause Categories\n1. Missing validation.",
        )
        path = _write_tmp(content)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_root_cause'])
        finally:
            os.unlink(path)

    def test_detects_vulnerable_code_patterns_heading(self):
        content = VALID_FRONTMATTER.replace(
            "```solidity\n// ❌ Vulnerable\nuint price = oracle.getPrice();",
            "## Vulnerable Code Patterns\n\n```solidity\nuint price = oracle.getPrice();",
        ).replace("❌", "VULNERABLE")
        path = _write_tmp(content)
        try:
            r = qc.parse_frontmatter(path)
            self.assertTrue(r['has_vuln_ex'])
        finally:
            os.unlink(path)


class TestFindEntries(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_db_root = qc.DB_ROOT
        qc.DB_ROOT = self.tmpdir + "/"

    def tearDown(self):
        qc.DB_ROOT = self.orig_db_root
        import shutil
        shutil.rmtree(self.tmpdir)

    def _touch(self, relpath: str):
        path = os.path.join(self.tmpdir, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write("# placeholder\n")
        return path

    def test_finds_md_files(self):
        self._touch("oracle/vuln1.md")
        self._touch("amm/vuln2.md")
        entries = qc.find_entries()
        names = [os.path.basename(e) for e in entries]
        self.assertIn("vuln1.md", names)
        self.assertIn("vuln2.md", names)

    def test_excludes_readme(self):
        self._touch("oracle/README.md")
        self._touch("oracle/real.md")
        entries = qc.find_entries()
        names = [os.path.basename(e) for e in entries]
        self.assertNotIn("README.md", names)
        self.assertIn("real.md", names)

    def test_excludes_artifact_index(self):
        self._touch("oracle/ARTIFACT_INDEX.md")
        entries = qc.find_entries()
        names = [os.path.basename(e) for e in entries]
        self.assertNotIn("ARTIFACT_INDEX.md", names)

    def test_excludes_search_guide(self):
        self._touch("oracle/SEARCH_GUIDE.md")
        entries = qc.find_entries()
        names = [os.path.basename(e) for e in entries]
        self.assertNotIn("SEARCH_GUIDE.md", names)

    def test_excludes_manifests_subdir(self):
        self._touch("manifests/oracle.json")
        # create a stray md inside manifests
        self._touch("manifests/stray.md")
        entries = qc.find_entries()
        names = [os.path.basename(e) for e in entries]
        self.assertNotIn("stray.md", names)

    def test_excludes_generated_graph_and_draft_dirs(self):
        self._touch("graphify-out/GRAPH_REPORT.md")
        self._touch("graphify-out/wiki/oracle.md")
        self._touch("_drafts/draft-oracle.md")
        self._touch("_telemetry/oracle-card.md")
        self._touch("oracle/real.md")
        entries = qc.find_entries()
        rel_entries = [os.path.relpath(e, self.tmpdir) for e in entries]
        self.assertEqual(rel_entries, ["oracle/real.md"])

    def test_results_sorted(self):
        self._touch("zzz/c.md")
        self._touch("aaa/a.md")
        self._touch("bbb/b.md")
        entries = qc.find_entries()
        self.assertEqual(entries, sorted(entries))

    def test_empty_db_returns_empty(self):
        entries = qc.find_entries()
        self.assertEqual(entries, [])


class TestValidSeverity(unittest.TestCase):

    def test_valid_severities_defined(self):
        for s in ['critical', 'high', 'medium', 'low']:
            self.assertIn(s, qc.VALID_SEVERITY)

    def test_unknown_severity_not_in_valid(self):
        self.assertNotIn('unknown', qc.VALID_SEVERITY)
        self.assertNotIn('info', qc.VALID_SEVERITY)
        self.assertNotIn('HIGH', qc.VALID_SEVERITY)  # case-sensitive


class TestRequiredFrontmatterFields(unittest.TestCase):

    def test_all_required_fields_present(self):
        expected = ['protocol', 'chain', 'category', 'vulnerability_type',
                    'root_cause_family', 'pattern_key', 'attack_type',
                    'affected_component', 'primitives', 'code_keywords', 'severity', 'impact']
        self.assertCountEqual(expected, qc.REQUIRED_FM_FIELDS)


class TestEntryCompliance(unittest.TestCase):

    def _check_entry(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'entry.md'
            path.write_text(content, encoding='utf-8')
            with mock.patch.object(qc, 'DB_ROOT', directory), redirect_stdout(io.StringIO()):
                return qc.skill1()

    def test_structurally_complete_entry_has_no_issues(self):
        result = self._check_entry(COMPLETE_ENTRY)
        self.assertEqual(result['full_compliance'], 1)
        self.assertEqual(result['entry_issues'], [])
        self.assertEqual(set(result['fm_field_coverage'].values()), {1})

    def test_each_required_field_is_checked(self):
        for field in qc.REQUIRED_FM_FIELDS:
            with self.subTest(field=field):
                content = '\n'.join(line for line in COMPLETE_ENTRY.split('\n')
                                    if not line.startswith(field + ':'))
                result = self._check_entry(content)
                issue = next(issue for issue in result['entry_issues'] if issue.get('field') == field)
                self.assertEqual(issue['level'], 'WARNING')
                self.assertEqual(issue['code'], 'missing_required_field')
                self.assertEqual(result['full_compliance'], 0)
                self.assertEqual(result['fm_field_coverage'][field], 0)

    def test_missing_frontmatter_is_a_migration_warning(self):
        result = self._check_entry(MISSING_FM)
        self.assertTrue(any(issue['code'] == 'missing_frontmatter' for issue in result['entry_issues']))
        self.assertFalse(any(issue['level'] == 'CRITICAL' for issue in result['entry_issues']))

    def test_invalid_yaml_is_critical(self):
        result = self._check_entry(INVALID_YAML_FM)
        self.assertTrue(any(issue['level'] == 'CRITICAL' and issue['code'] == 'invalid_frontmatter'
                            for issue in result['entry_issues']))
        self.assertEqual(result['full_compliance'], 0)

    def test_non_mapping_yaml_is_critical(self):
        for value in ('[one, two]', '[]', 'false', '42', 'some text'):
            with self.subTest(value=value):
                result = self._check_entry(f'---\n{value}\n---\n# Entry\n')
                self.assertTrue(any(issue['level'] == 'CRITICAL' and 'mapping/object' in issue['message']
                                    for issue in result['entry_issues']))

    def test_duplicate_yaml_keys_are_critical(self):
        content = COMPLETE_ENTRY.replace('severity: high', 'severity: low\nseverity: high')
        result = self._check_entry(content)
        self.assertTrue(any(issue['level'] == 'CRITICAL' and 'duplicate mapping key' in issue['message']
                            for issue in result['entry_issues']))

    def test_unterminated_frontmatter_is_critical(self):
        result = self._check_entry('---\nprotocol: generic\n# no closing delimiter\n')
        self.assertTrue(any(issue['level'] == 'CRITICAL' and 'closing delimiter' in issue['message']
                            for issue in result['entry_issues']))

    def test_invalid_field_types_are_critical(self):
        for field, value in (('protocol', '42'), ('chain', '[ethereum]'),
                             ('severity', 'true'), ('primitives', 'timestamp'),
                             ('primitives', '[timestamp, 42]'), ('code_keywords', '[""]'),
                             ('code_keywords', '{name: price}')):
            with self.subTest(field=field, value=value):
                content = '\n'.join(f'{field}: {value}' if line.startswith(field + ':') else line
                                    for line in COMPLETE_ENTRY.split('\n'))
                result = self._check_entry(content)
                issue = next(issue for issue in result['entry_issues'] if issue.get('field') == field)
                self.assertEqual(issue['level'], 'CRITICAL')
                self.assertEqual(issue['code'], 'invalid_field_type')
                self.assertEqual(result['full_compliance'], 0)

    def test_empty_required_fields_are_migration_warnings(self):
        for original, replacement in (('protocol: ethereum', 'protocol: "  "'),
                                      ('primitives: [timestamp, price_feed]', 'primitives: []'),
                                      ('severity: high', 'severity: null')):
            with self.subTest(replacement=replacement):
                result = self._check_entry(COMPLETE_ENTRY.replace(original, replacement))
                self.assertEqual(len(result['entry_issues']), 1)
                self.assertEqual(result['entry_issues'][0]['level'], 'WARNING')
                self.assertEqual(result['entry_issues'][0]['code'], 'missing_required_field')

    def test_invalid_severity_prevents_compliance(self):
        result = self._check_entry(COMPLETE_ENTRY.replace('severity: high', 'severity: urgent'))
        self.assertEqual(result['entry_issues'][0]['code'], 'invalid_severity')
        self.assertEqual(result['entry_issues'][0]['level'], 'CRITICAL')
        self.assertEqual(result['full_compliance'], 0)
        self.assertEqual(len(result['severity_issues']), 1)

    def test_severity_is_case_insensitive(self):
        result = self._check_entry(COMPLETE_ENTRY.replace('severity: high', 'severity: HIGH'))
        self.assertEqual(result['full_compliance'], 1)

    def test_missing_reference_and_agent_sections_are_reported(self):
        result = self._check_entry(VALID_FRONTMATTER)
        codes = {issue['code'] for issue in result['entry_issues']}
        self.assertTrue({'no_reference', 'no_quick_view', 'no_valid_signals',
                         'no_false_positive_guards'} <= codes)

    def test_heading_in_code_fence_does_not_satisfy_reference_section(self):
        content = COMPLETE_ENTRY.replace('## References & Source Reports',
                                         '```markdown\n## References & Source Reports\n```')
        result = self._check_entry(content)
        self.assertTrue(any(issue['code'] == 'no_reference' for issue in result['entry_issues']))

    def test_empty_database_is_critical_and_does_not_divide_by_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(qc, 'DB_ROOT', directory), redirect_stdout(io.StringIO()):
                result = qc.skill1()
        self.assertEqual(result['total'], 0)
        self.assertEqual(result['entry_issues'][0]['code'], 'empty_database')
        self.assertEqual(result['entry_issues'][0]['level'], 'CRITICAL')


class TestQualityReportCLI(unittest.TestCase):

    def _run_main(self, directory, content=COMPLETE_ENTRY, manifest_issues=None, manifest_error=None):
        entry_dir = Path(directory) / 'DB'
        entry_dir.mkdir(exist_ok=True)
        (entry_dir / 'entry.md').write_text(content, encoding='utf-8')
        output_path = Path(directory) / 'output' / 'report.json'
        stdout = io.StringIO()
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(qc, 'DB_ROOT', str(entry_dir)))
            for name in ('skill2', 'skill3', 'skill4', 'skill5', 'skill6_sample', 'skill7', 'skill8', 'skill9'):
                stack.enter_context(mock.patch.object(qc, name, return_value=[]))
            qc.skill2.return_value = manifest_issues or []
            qc.skill2.side_effect = manifest_error
            stack.enter_context(redirect_stdout(stdout))
            code = qc.main(['--json-output', str(output_path)])
        return code, json.loads(output_path.read_text(encoding='utf-8')), stdout.getvalue()

    def test_healthy_report_and_zero_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            code, report, stdout = self._run_main(directory)
        self.assertEqual(code, 0)
        self.assertEqual(report['summary']['status'], 'HEALTHY')
        self.assertEqual(report['summary']['totalIssues'], 0)
        self.assertIn('not factual', report['scope'])
        self.assertIn('Overall: HEALTHY', stdout)

    def test_single_warning_is_degraded_but_does_not_fail_ci(self):
        with tempfile.TemporaryDirectory() as directory:
            code, report, stdout = self._run_main(directory, manifest_issues=[('WARNING', 'Stale count')])
        self.assertEqual(code, 0)
        self.assertEqual(report['summary']['status'], 'DEGRADED')
        self.assertEqual(report['summary']['warnings'], 1)
        self.assertEqual(report['issues'][0]['check'], 'manifest_integrity')
        self.assertIn('Overall: DEGRADED', stdout)

    def test_entry_schema_error_fails_ci_and_is_in_json(self):
        with tempfile.TemporaryDirectory() as directory:
            code, report, _stdout = self._run_main(directory, content=INVALID_YAML_FM)
        self.assertEqual(code, 1)
        self.assertEqual(report['summary']['status'], 'BROKEN')
        self.assertEqual(report['summary']['criticalIssues'], 1)
        self.assertTrue(report['entryIssues'])
        self.assertTrue(any(issue['check'] == 'entry_compliance' and issue['code'] == 'invalid_frontmatter'
                            for issue in report['issues']))
        self.assertEqual(report['summary']['warnings'], sum(issue['level'] == 'WARNING' for issue in report['entryIssues']))

    def test_legacy_section_gap_is_in_summary(self):
        content = COMPLETE_ENTRY.replace('#### Valid Bug Signals', '#### Legacy guidance')
        with tempfile.TemporaryDirectory() as directory:
            code, report, _stdout = self._run_main(directory, content=content)
        self.assertEqual(code, 0)
        self.assertEqual(report['summary']['status'], 'DEGRADED')
        self.assertEqual(report['summary']['warnings'], 1)
        self.assertEqual(report['entryIssues'][0]['code'], 'no_valid_signals')

    def test_artifact_critical_fails_ci(self):
        with tempfile.TemporaryDirectory() as directory:
            code, report, _stdout = self._run_main(directory, manifest_issues=[('CRITICAL', 'Bad ref')])
        self.assertEqual(code, 1)
        self.assertEqual(report['summary']['criticalIssues'], 1)
        self.assertEqual(report['summary']['status'], 'BROKEN')

    def test_malformed_artifact_exception_is_reported_and_remaining_checks_run(self):
        with tempfile.TemporaryDirectory() as directory:
            code, report, stdout = self._run_main(directory, manifest_error=ValueError('bad JSON shape'))
        self.assertEqual(code, 1)
        self.assertEqual(report['summary']['status'], 'BROKEN')
        self.assertIn('bad JSON shape', report['issues'][0]['message'])
        self.assertIn('Overall: BROKEN', stdout)


class TestPartitionBundleValidation(unittest.TestCase):

    def test_valid_partition_bundle_passes(self):
        bundle = {
            "meta": {
                "totalCards": 3,
                "criticalCards": 1,
                "shardCount": 1,
                "criticalCardIds": ["critical-1"],
            },
            "shards": [
                {
                    "id": "shard-1-oracle",
                    "cardCount": 2,
                    "regularCardCount": 2,
                    "criticalCardCount": 1,
                    "effectiveCardCount": 3,
                    "categories": ["oracle"],
                    "cardIds": ["regular-1", "regular-2"],
                    "criticalCardIds": ["critical-1"],
                }
            ],
        }

        self.assertEqual(qc.validate_partition_bundle_data(bundle), [])

    def test_partition_bundle_requires_critical_ids_on_each_shard(self):
        bundle = {
            "meta": {
                "totalCards": 2,
                "criticalCards": 1,
                "shardCount": 1,
                "criticalCardIds": ["critical-1"],
            },
            "shards": [
                {
                    "id": "shard-1-oracle",
                    "cardCount": 1,
                    "regularCardCount": 1,
                    "criticalCardCount": 1,
                    "effectiveCardCount": 2,
                    "categories": ["oracle"],
                    "cardIds": ["regular-1"],
                    "criticalCardIds": [],
                }
            ],
        }

        issues = qc.validate_partition_bundle_data(bundle)

        self.assertTrue(any("does not carry the full criticalCardIds set" in msg for _level, msg in issues))

    def test_partition_bundle_rejects_duplicate_regular_ids(self):
        bundle = {
            "meta": {
                "totalCards": 2,
                "criticalCards": 0,
                "shardCount": 2,
                "criticalCardIds": [],
            },
            "shards": [
                {
                    "id": "shard-1",
                    "cardCount": 1,
                    "regularCardCount": 1,
                    "criticalCardCount": 0,
                    "effectiveCardCount": 1,
                    "categories": ["oracle"],
                    "cardIds": ["regular-1"],
                    "criticalCardIds": [],
                },
                {
                    "id": "shard-2",
                    "cardCount": 1,
                    "regularCardCount": 1,
                    "criticalCardCount": 0,
                    "effectiveCardCount": 1,
                    "categories": ["defi"],
                    "cardIds": ["regular-1"],
                    "criticalCardIds": [],
                },
            ],
        }

        issues = qc.validate_partition_bundle_data(bundle)

        self.assertTrue(any("duplicate regular card IDs" in msg for _level, msg in issues))

    def test_partition_bundle_rejects_non_actionable_total(self):
        bundle = {
            "meta": {
                "totalCards": 1,
                "criticalCards": 0,
                "shardCount": 0,
                "criticalCardIds": [],
            },
            "shards": [],
        }

        issues = qc.validate_partition_bundle_data(bundle)

        self.assertTrue(any("no shards are actionable" in msg for _level, msg in issues))


if __name__ == '__main__':
    unittest.main(verbosity=2)
