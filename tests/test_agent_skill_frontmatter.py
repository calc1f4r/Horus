#!/usr/bin/env python3
"""Frontmatter contract for .claude/agents/*.md and .claude/skills/*/SKILL.md.

Regression guard: 33 SKILL.md files once shipped without their opening `---`,
so the whole frontmatter block was parsed as body text and every skill showed
a literal "name: <slug>" as its description in the skill picker.
"""
from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"


def split_frontmatter(path: Path) -> dict[str, str]:
    """Parse the leading `---` block. Raises AssertionError when malformed."""
    lines = path.read_text(encoding="utf-8").split("\n")
    assert lines and lines[0].strip() == "---", (
        f"{path.relative_to(REPO_ROOT)}: missing opening '---' delimiter"
    )
    try:
        end = lines.index("---", 1)
    except ValueError:  # pragma: no cover - guarded by the assert message
        raise AssertionError(
            f"{path.relative_to(REPO_ROOT)}: missing closing '---' delimiter"
        ) from None

    fields: dict[str, str] = {}
    key = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if raw[:1] not in (" ", "\t") and ":" in raw:
            key, _, value = raw.partition(":")
            fields[key.strip()] = value.strip()
        elif key is not None:
            fields[key] += " " + raw.strip()
    return fields


class TestAgentFrontmatter(unittest.TestCase):
    def test_agents_exist(self):
        self.assertTrue(list(AGENTS_DIR.glob("*.md")), "no agent files found")

    def test_every_agent_has_valid_frontmatter(self):
        for path in sorted(AGENTS_DIR.glob("*.md")):
            with self.subTest(agent=path.name):
                fm = split_frontmatter(path)
                for field in ("name", "description", "tools"):
                    self.assertIn(field, fm, f"{path.name}: missing '{field}'")
                self.assertEqual(
                    fm["name"],
                    path.stem,
                    f"{path.name}: frontmatter name must match filename",
                )
                self.assertNotEqual(fm["description"], "", f"{path.name}: empty description")


class TestSkillFrontmatter(unittest.TestCase):
    def test_skills_exist(self):
        self.assertTrue(list(SKILLS_DIR.glob("*/SKILL.md")), "no skill files found")

    def test_every_skill_has_valid_frontmatter(self):
        for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            with self.subTest(skill=path.parent.name):
                fm = split_frontmatter(path)
                for field in ("name", "description", "agent"):
                    self.assertIn(field, fm, f"{path.parent.name}: missing '{field}'")
                self.assertEqual(
                    fm["name"],
                    path.parent.name,
                    f"{path.parent.name}: frontmatter name must match directory",
                )

    def test_description_is_not_a_leaked_name_field(self):
        """A missing opening delimiter makes 'description' read as 'name: <slug>'."""
        for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            with self.subTest(skill=path.parent.name):
                fm = split_frontmatter(path)
                self.assertFalse(
                    fm["description"].startswith("name:"),
                    f"{path.parent.name}: description leaked the name field — "
                    "frontmatter delimiters are malformed",
                )

    def test_every_skill_targets_an_existing_agent(self):
        agents = {p.stem for p in AGENTS_DIR.glob("*.md")}
        for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            with self.subTest(skill=path.parent.name):
                target = split_frontmatter(path)["agent"]
                self.assertIn(
                    target, agents, f"{path.parent.name}: agent '{target}' does not exist"
                )


class TestAgentSkillParity(unittest.TestCase):
    def test_every_agent_has_a_skill(self):
        agents = {p.stem for p in AGENTS_DIR.glob("*.md")}
        skills = {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}
        self.assertEqual(
            agents - skills, set(), "agents without a corresponding skill"
        )
        self.assertEqual(
            skills - agents, set(), "skills without a corresponding agent"
        )


if __name__ == "__main__":
    unittest.main()
