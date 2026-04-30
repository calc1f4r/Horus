#!/usr/bin/env python3
"""Unit tests for Codex compatibility sync validation helpers."""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import sync_codex_compat as sync  # noqa: E402


def write_agent(path: Path, name: str, description: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
        "Read [guide](.claude/resources/guide.md).\n",
        encoding="utf-8",
    )


def write_resource(path: Path, content: str = "Resource\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class TestGithubAgentSurface(unittest.TestCase):

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.source_root = self.tmpdir / ".claude" / "agents"
        self.github_root = self.tmpdir / ".github" / "agents"

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_check_github_agent_surface_accepts_generated_mirror(self):
        write_agent(self.source_root / "audit.md", "audit", "Run audits")
        source = self.source_root / "audit.md"
        expected = sync.build_github_agent_content(
            source,
            source.read_text(encoding="utf-8"),
        )
        self.github_root.mkdir(parents=True, exist_ok=True)
        (self.github_root / "audit.md").write_text(expected, encoding="utf-8")

        issues = sync.check_github_agent_surface(
            source_root=self.source_root,
            github_root=self.github_root,
        )

        self.assertEqual(issues, [])

    def test_check_github_agent_surface_reports_missing_and_extra_files(self):
        write_agent(self.source_root / "audit.md", "audit", "Run audits")
        write_agent(self.github_root / "extra.md", "extra", "Extra agent")

        issues = sync.check_github_agent_surface(
            source_root=self.source_root,
            github_root=self.github_root,
        )

        self.assertIn("missing GitHub agent mirror: .github/agents/audit.md", issues)
        self.assertIn("unexpected GitHub agent mirror: .github/agents/extra.md", issues)

    def test_check_github_agent_surface_reports_outdated_mirror(self):
        write_agent(self.source_root / "audit.md", "audit", "Run audits")
        write_agent(self.github_root / "audit.md", "audit", "Different description")

        issues = sync.check_github_agent_surface(
            source_root=self.source_root,
            github_root=self.github_root,
        )

        self.assertEqual(issues, ["outdated GitHub agent mirror: .github/agents/audit.md"])

    def test_sync_github_agent_surface_writes_generated_mirror(self):
        write_agent(self.source_root / "audit.md", "audit", "Run audits")
        write_agent(self.github_root / "stale.md", "stale", "Old")

        count = sync.sync_github_agent_surface(
            source_root=self.source_root,
            github_root=self.github_root,
        )

        self.assertEqual(count, 1)
        self.assertFalse((self.github_root / "stale.md").exists())
        written = (self.github_root / "audit.md").read_text(encoding="utf-8")
        self.assertIn("tools: [vscode, execute, read, agent, edit, search, web, browser, todo]", written)
        self.assertIn("[guide](resources/guide.md)", written)


class TestGithubResourceSurface(unittest.TestCase):

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.source_root = self.tmpdir / ".claude" / "resources"
        self.github_root = self.tmpdir / ".github" / "agents" / "resources"

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_check_github_resource_surface_accepts_matching_files(self):
        write_resource(self.source_root / "guide.md", "same\n")
        write_resource(self.github_root / "guide.md", "same\n")

        issues = sync.check_github_resource_surface(
            source_root=self.source_root,
            github_root=self.github_root,
        )

        self.assertEqual(issues, [])

    def test_check_github_resource_surface_reports_missing_and_extra_files(self):
        write_resource(self.source_root / "guide.md")
        write_resource(self.github_root / "extra.md")

        issues = sync.check_github_resource_surface(
            source_root=self.source_root,
            github_root=self.github_root,
        )

        self.assertIn("missing GitHub resource mirror: .github/agents/resources/guide.md", issues)
        self.assertIn("unexpected GitHub resource mirror: .github/agents/resources/extra.md", issues)

    def test_check_github_resource_surface_reports_content_drift(self):
        write_resource(self.source_root / "guide.md", "source\n")
        write_resource(self.github_root / "guide.md", "mirror\n")

        issues = sync.check_github_resource_surface(
            source_root=self.source_root,
            github_root=self.github_root,
        )

        self.assertEqual(issues, ["content drift in .github/agents/resources/guide.md"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
