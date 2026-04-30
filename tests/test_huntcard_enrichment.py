#!/usr/bin/env python3
"""Unit tests for huntcard_enrichment parser adapters."""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import huntcard_enrichment as enrichment  # noqa: E402


class TestHuntcardEnrichmentParsing(unittest.TestCase):

    def test_extract_frontmatter_uses_yaml_and_normalizes_keys(self):
        text = (
            "---\n"
            "Audit Firm: Trail of Bits\n"
            "protocol: Example\n"
            "tags:\n"
            "  - oracle\n"
            "  - stale-price\n"
            "---\n"
            "# Body\n"
        )

        frontmatter, body = enrichment.extract_frontmatter(text)

        self.assertEqual(frontmatter["audit_firm"], "Trail of Bits")
        self.assertEqual(frontmatter["protocol"], "Example")
        self.assertEqual(frontmatter["tags"], ["oracle", "stale-price"])
        self.assertEqual(body, "# Body\n")

    def test_read_db_section_uses_document_parser(self):
        tmpdir = Path(tempfile.mkdtemp())
        original_root = enrichment.ROOT
        try:
            enrichment.ROOT = tmpdir
            db_file = tmpdir / "DB" / "oracle" / "sample.md"
            db_file.parent.mkdir(parents=True)
            db_file.write_text(
                "---\n"
                "protocol: Example\n"
                "Audit Firm: Sherlock\n"
                "---\n"
                "# Title\n"
                "## Vulnerable Pattern\n"
                "Line A\n"
                "Line B\n",
                encoding="utf-8",
            )

            section, frontmatter = enrichment.read_db_section(
                "DB/oracle/sample.md",
                [6, 8],
            )
        finally:
            enrichment.ROOT = original_root
            shutil.rmtree(tmpdir)

        self.assertEqual(frontmatter["protocol"], "Example")
        self.assertEqual(frontmatter["audit_firm"], "Sherlock")
        self.assertEqual(section, "## Vulnerable Pattern\nLine A\nLine B")


if __name__ == "__main__":
    unittest.main(verbosity=2)
