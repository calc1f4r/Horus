#!/usr/bin/env python3
"""Fixture-level tests for manifest generation."""

import os
import sys
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import generate_manifests as gm  # noqa: E402


class TestGenerateManifestFixture(unittest.TestCase):

    def test_build_file_manifest_uses_document_model_without_output_drift(self):
        repo_root = Path(__file__).resolve().parents[1]
        fixture = repo_root / "tests" / "fixtures" / "db" / "sample-vulnerability.md"

        manifest_entry = gm.build_file_manifest(fixture, "oracle")

        self.assertEqual(manifest_entry["file"], "tests/fixtures/db/sample-vulnerability.md")
        self.assertEqual(manifest_entry["patternCount"], 1)
        self.assertEqual(manifest_entry["frontmatter"]["protocol"], "ethereum")

        pattern = manifest_entry["patterns"][0]
        self.assertEqual(pattern["title"], "Stale Oracle Price [HIGH]")
        self.assertEqual(pattern["severity"], ["HIGH"])
        self.assertEqual(pattern["lineStart"], 20)
        self.assertEqual(pattern["lineEnd"], 39)
        self.assertIn("getPrice", pattern["codeKeywords"])
        self.assertIn("updatedAt", pattern["codeKeywords"])
        self.assertIn("oracle", pattern["searchKeywords"])
        self.assertEqual(pattern["reportEvidence"]["count"], 1)
        self.assertEqual(pattern["reportEvidence"]["severityConsensus"], "HIGH")


if __name__ == "__main__":
    unittest.main(verbosity=2)
