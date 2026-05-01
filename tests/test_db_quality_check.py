#!/usr/bin/env python3
"""Unit tests for scripts/db_quality_check.py"""
import os
import sys
import json
import tempfile
import unittest

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
        expected = ['protocol', 'category', 'vulnerability_type', 'attack_type',
                    'affected_component', 'severity', 'impact']
        for field in expected:
            self.assertIn(field, qc.REQUIRED_FM_FIELDS)


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
