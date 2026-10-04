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

    def test_hunt_card_quality_gate_rejects_invalid_regexes(self):
        text = (WORKFLOWS / "validate-hunt-card-quality.yml").read_text(encoding="utf-8")

        self.assertIn("import json, os, re, sys", text)
        self.assertIn("invalid_grep", text)
        self.assertIn("re.compile(grep)", text)

    def test_retrieval_pipeline_workflow_runs_full_validator_on_script_changes(self):
        text = (WORKFLOWS / "validate-retrieval-pipeline.yml").read_text(encoding="utf-8")

        self.assertIn("scripts/**/*.py", text)
        self.assertIn("tests/**", text)
        self.assertIn("python3 scripts/validate_retrieval_pipeline.py", text)

    def test_regeneration_workflows_rebuild_and_commit_graph_artifacts(self):
        workflow_paths = [
            WORKFLOWS / "regenerate-manifests.yml",
            WORKFLOWS / "scheduled-regenerate.yml",
        ]

        for workflow in workflow_paths:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                self.assertIn("python3 scripts/generate_manifests.py", text)
                self.assertIn("python3 scripts/build_db_graph.py", text)
                self.assertIn("DB/graphify-out/", text)
                self.assertIn("git add DB/index.json DB/manifests/ DB/graphify-out/", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
