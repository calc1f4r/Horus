#!/usr/bin/env python3
"""Regression tests for GitHub workflow path filters."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class TestWorkflowPaths(unittest.TestCase):

    def test_manifest_workflows_watch_canonical_generator(self):
        workflow_paths = [
            WORKFLOWS / "regenerate-manifests.yml",
            WORKFLOWS / "validate-hunt-card-quality.yml",
        ]

        for workflow in workflow_paths:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                self.assertIn("scripts/generate_manifests.py", text)
                self.assertNotIn("'generate_manifests.py'", text)
                self.assertNotIn("^generate_manifests\\.py$", text)

    def test_master_sync_does_not_expect_root_generator(self):
        text = (WORKFLOWS / "reusable-sync-to-master.yml").read_text(encoding="utf-8")

        self.assertIn("scripts", text)
        self.assertNotIn("\n            generate_manifests.py\n", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
