#!/usr/bin/env python3
"""Keep generated evidence claims faithful to local synthetic source metadata."""

import copy
import sys
import unittest
from pathlib import Path

import yaml


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from archive.generate_cosmos_v2 import generate_entry_content  # noqa: E402
from migrate_to_new_template import generate_agent_quick_view  # noqa: E402
from solodit_fetcher import finding_to_markdown  # noqa: E402


def frontmatter(markdown):
    return yaml.safe_load(markdown.split("---", 2)[1])


class TestSourceClaims(unittest.TestCase):
    def test_quality_score_is_preserved_without_becoming_exploitability(self):
        for score in (0, 2.5, 5):
            with self.subTest(score=score):
                finding = {
                    "id": "synthetic-17",
                    "title": "Synthetic source record",
                    "quality_score": score,
                    "content": "Local fixture content, preserved verbatim.",
                    "source_link": "https://example.invalid/source-record",
                }
                original = copy.deepcopy(finding)
                markdown = finding_to_markdown(finding)
                metadata = frontmatter(markdown)
                self.assertEqual(metadata["quality_score"], score)
                self.assertNotIn("exploitability", metadata)
                self.assertEqual(metadata["solodit_id"], finding["id"])
                self.assertEqual(metadata["source_link"], finding["source_link"])
                self.assertIn(finding["content"], markdown)
                self.assertEqual(finding, original)

    def test_missing_or_null_quality_does_not_invent_exploitability(self):
        for finding in ({}, {"quality_score": None}):
            with self.subTest(finding=finding):
                self.assertNotIn("exploitability", frontmatter(finding_to_markdown(finding)))

    def test_migration_does_not_assign_source_validation_strength(self):
        metadata = {
            "root_cause_family": "synthetic_family",
            "pattern_key": "synthetic_pattern",
            "code_keywords": ["FixtureMarker"],
            "references": ["synthetic-a", "synthetic-b", "synthetic-c"],
        }
        original = copy.deepcopy(metadata)
        result = generate_agent_quick_view(metadata)
        self.assertIn("Validation strength: `unassessed`", result)
        self.assertIn("migration does not validate source evidence", result)
        self.assertNotIn("Validation strength: `moderate`", result)
        self.assertIn("`FixtureMarker`", result)
        self.assertEqual(metadata, original)

    @staticmethod
    def generate_cosmos_fixture(firms):
        reports = [
            {
                "file": f"synthetic-{number}.md",
                "title": f"Synthetic source record {number}",
                "severity": "MEDIUM",
                "audit_firm": firm,
                "protocol": "FixtureProtocol",
                "code_blocks": [],
                "finding": "",
                "overview": "Local synthetic evidence metadata.",
            }
            for number, firm in enumerate(firms)
        ]
        pattern_id = "fixture-pattern"
        metadata = {
            pattern_id: {
                "title": "Synthetic Pattern",
                "root_cause": "Synthetic classification without a reviewed implementation",
                "impact": "Unassessed fixture impact",
            }
        }
        return generate_entry_content(
            "fixture/synthetic-entry", [pattern_id], {pattern_id: reports}, metadata
        )[0]

    def test_cosmos_firm_counts_do_not_become_validation_strength(self):
        for firms, expected_count in (
            (["unknown"], 0),
            (["Firm A", "Firm A", "unknown"], 1),
            (["Firm A", "Firm B"], 2),
            (["Firm A", "Firm B", "Firm C"], 3),
        ):
            with self.subTest(firms=firms):
                markdown = self.generate_cosmos_fixture(firms)
                self.assertIn(f"**Distinct Source Firm Labels**: {expected_count} ", markdown)
                self.assertIn(f"**Frequency**: Found in {len(firms)} audit reports", markdown)
                self.assertIn("**Validation Strength**: `unassessed`", markdown)
                self.assertIn("independence not assessed", markdown)
                self.assertNotIn("Strong (", markdown)
                self.assertNotIn("Moderate (", markdown)
                self.assertNotIn("exploitability", frontmatter(markdown))
                for number in range(len(firms)):
                    self.assertIn(f"reports/cosmos_cometbft_findings/synthetic-{number}.md", markdown)

    def test_cosmos_noop_example_is_labeled_incomplete(self):
        markdown = self.generate_cosmos_fixture(["Firm A"])
        section = markdown.split("### Secure Implementation\n", 1)[1].split(
            "### Impact Analysis", 1
        )[0]
        self.assertIn("incomplete illustrative skeleton", section)
        self.assertIn("No validated remediation is provided", section)
        self.assertIn("This skeleton implements no validation or remediation", section)
        self.assertIn("return nil", section)
        self.assertNotIn("✅ SECURE", section)
        self.assertNotIn("func secure", section)


if __name__ == "__main__":
    unittest.main(verbosity=2)
