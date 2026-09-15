#!/usr/bin/env python3
"""Regression tests for DB severity and report-evidence parsing."""

import os
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.documents import (  # noqa: E402
    extract_report_references,
    extract_severity_from_context,
)
from horus_retrieval.manifests import build_file_manifest  # noqa: E402
from generate_micro_directives import _extract_report_evidence  # noqa: E402


class TestEvidenceParsing(unittest.TestCase):

    def test_plain_prose_does_not_supply_severity(self):
        lines = [
            "This allows the middleware to emit a high-signal event.\n",
            "Critical state changes still require authorization.\n",
        ]

        self.assertEqual(extract_severity_from_context(lines, 0, len(lines)), [])

    def test_explicit_markers_supply_severity(self):
        lines = ["## Stale price [HIGH]\n", "Severity: medium\n"]

        self.assertEqual(
            extract_severity_from_context(lines, 0, len(lines)),
            ["HIGH", "MEDIUM"],
        )

    def test_report_filename_does_not_supply_severity(self):
        evidence = extract_report_references(
            ["| finding | reports/oracle/high-quality-report.md | LOW | auditor |\n"]
        )

        self.assertEqual(evidence["severityConsensus"], "LOW")

    def test_repeated_report_does_not_outvote_unique_sources(self):
        evidence = extract_report_references(
            [
                "| a | reports/a.md | HIGH | firm |\n",
                "| a duplicate | reports/a.md | HIGH | firm |\n",
                "| b | reports/b.md | LOW | firm |\n",
                "| c | reports/c.md | LOW | firm |\n",
            ]
        )

        self.assertEqual(evidence["count"], 3)
        self.assertEqual(evidence["severityConsensus"], "LOW")

    def test_micro_directive_requires_a_report_for_consensus(self):
        evidence = _extract_report_evidence(["Severity: CRITICAL\n"])

        self.assertEqual(evidence, {})

    def test_numbered_keywords_section_is_not_a_pattern(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_root = root / "DB"
            entry = db_root / "oracle" / "sample.md"
            entry.parent.mkdir(parents=True)
            entry.write_text(
                "---\nprotocol: test\ncategory: oracle\nseverity: high\n---\n"
                "## 1. Actual Vulnerability [HIGH]\n\n"
                "A sufficiently detailed vulnerability description.\n\n"
                "### Root Cause\n\nMissing validation at a trusted boundary.\n\n"
                "## 10. Keywords for Search\n\n"
                "Critical state-changing operations and high-signal middleware terms.\n\n"
                "More keyword prose so the section is long enough to pass length filters.\n",
                encoding="utf-8",
            )

            manifest = build_file_manifest(entry, "oracle", db_root=db_root)

        self.assertEqual(manifest["patternCount"], 1)
        self.assertEqual(manifest["patterns"][0]["title"], "1. Actual Vulnerability [HIGH]")


if __name__ == "__main__":
    unittest.main(verbosity=2)
