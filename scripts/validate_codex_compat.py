#!/usr/bin/env python3
"""Validate the generated Codex runtime surfaces."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from sync_codex_compat import check_outputs, generate, split_frontmatter


REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_ROOT = REPO_ROOT / ".claude"
SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"
CODEX_ROOT = REPO_ROOT / ".codex"
AGENTS_ROOT = CODEX_ROOT / "agents"


def iter_markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def resolve_local_link(base: Path, target: str) -> Path | None:
    if target.startswith(("http://", "https://", "mailto:")):
        return None
    if target.startswith("#"):
        return None

    target = target.split("#", 1)[0].strip()
    if not target:
        return None

    if target.startswith((".agents/", ".codex/", "DB/")):
        return (REPO_ROOT / target).resolve()
    if target.startswith("/"):
        return None

    return (base / target).resolve()


def validate_config(errors: list[str]) -> None:
    config_path = CODEX_ROOT / "config.toml"
    if not config_path.exists():
        errors.append("missing .codex/config.toml")
        return

    try:
        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        errors.append(f".codex/config.toml is invalid TOML: {exc}")
        return

    if data.get("web_search") != "live":
        errors.append(".codex/config.toml: web_search must be \"live\"")
    if data.get("tools", {}).get("web_search", {}).get("context_size") != "medium":
        errors.append(".codex/config.toml: tools.web_search.context_size must be \"medium\"")
    agents = data.get("agents", {})
    if agents.get("max_depth") != 2:
        errors.append(".codex/config.toml: agents.max_depth must be 2")
    if agents.get("max_threads") != 12:
        errors.append(".codex/config.toml: agents.max_threads must be 12")


def validate_skill_agent_mapping(errors: list[str]) -> None:
    expected_agents = {path.stem for path in (CLAUDE_ROOT / "agents").glob("*.md")}

    for skill_path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        text = skill_path.read_text(encoding="utf-8", errors="replace")
        meta, _, _, _ = split_frontmatter(text)
        name = meta.get("name")
        description = meta.get("description")
        if not name or not description:
            errors.append(f"{skill_path.relative_to(REPO_ROOT).as_posix()}: missing name/description frontmatter")
            continue
        if name not in expected_agents:
            errors.append(f"{skill_path.relative_to(REPO_ROOT).as_posix()}: no matching .claude agent for skill {name}")
            continue
        linked_agent = REPO_ROOT / ".codex" / "agents" / f"{name}.toml"
        if not linked_agent.exists():
            errors.append(f"{skill_path.relative_to(REPO_ROOT).as_posix()}: missing linked agent {linked_agent.relative_to(REPO_ROOT).as_posix()}")


def validate_agents(errors: list[str]) -> None:
    expected_agents = {path.stem for path in (CLAUDE_ROOT / "agents").glob("*.md")}
    actual_agents = set()

    for agent_path in sorted(AGENTS_ROOT.glob("*.toml")):
        actual_agents.add(agent_path.stem)
        try:
            data = tomllib.loads(agent_path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"{agent_path.relative_to(REPO_ROOT).as_posix()}: invalid TOML: {exc}")
            continue

        if data.get("name") != agent_path.stem:
            errors.append(f"{agent_path.relative_to(REPO_ROOT).as_posix()}: name must match filename stem")
        if data.get("web_search") != "live":
            errors.append(f"{agent_path.relative_to(REPO_ROOT).as_posix()}: web_search must be \"live\"")
        if data.get("tools", {}).get("web_search", {}).get("context_size") != "medium":
            errors.append(f"{agent_path.relative_to(REPO_ROOT).as_posix()}: tools.web_search.context_size must be \"medium\"")
        agents = data.get("agents", {})
        if agents.get("max_depth") != 2 or agents.get("max_threads") != 12:
            errors.append(f"{agent_path.relative_to(REPO_ROOT).as_posix()}: agents table must set max_depth=2 and max_threads=12")
        instructions = data.get("developer_instructions", "")
        if "Use live web search when external facts" not in instructions:
            errors.append(f"{agent_path.relative_to(REPO_ROOT).as_posix()}: missing web-search guidance")
        if "Delegate to narrower repo custom agents" not in instructions:
            errors.append(f"{agent_path.relative_to(REPO_ROOT).as_posix()}: missing delegation guidance")

    missing_agents = sorted(expected_agents - actual_agents)
    for agent in missing_agents:
        errors.append(f"missing generated agent: .codex/agents/{agent}.toml")


def validate_markdown_links(errors: list[str]) -> None:
    markdown_files = [path for path in SKILLS_ROOT.rglob("*.md") if path.is_file()]
    markdown_files.extend(path for path in (CODEX_ROOT / "resources").rglob("*.md") if path.is_file())
    markdown_files.extend(path for path in (CODEX_ROOT / "rules").rglob("*.md") if path.is_file())

    for path in sorted(markdown_files):
        text = path.read_text(encoding="utf-8", errors="replace")

        for link in iter_markdown_links(text):
            if link in {"link", "permalink"} or "{" in link or "}" in link or "..." in link:
                continue
            resolved = resolve_local_link(path.parent, link)
            if resolved is not None and not resolved.exists():
                errors.append(f"{path.relative_to(REPO_ROOT).as_posix()}: broken local link -> {link}")


def validate_counts(errors: list[str]) -> None:
    source_skill_count = len(list((CLAUDE_ROOT / "skills").glob("*/SKILL.md")))
    generated_skill_count = len(list(SKILLS_ROOT.glob("*/SKILL.md")))
    source_agent_count = len(list((CLAUDE_ROOT / "agents").glob("*.md")))
    generated_agent_count = len(list(AGENTS_ROOT.glob("*.toml")))

    if generated_skill_count != source_skill_count:
        errors.append(f"unexpected skill count: source={source_skill_count} generated={generated_skill_count}")
    if generated_agent_count != source_agent_count:
        errors.append(f"unexpected agent count: source={source_agent_count} generated={generated_agent_count}")


def main() -> int:
    outputs, _ = generate()
    errors: list[str] = []

    if check_outputs(outputs) != 0:
        errors.append("generated Codex runtime parity check failed")

    validate_config(errors)
    validate_skill_agent_mapping(errors)
    validate_agents(errors)
    validate_markdown_links(errors)
    validate_counts(errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    print("Codex runtime validation passed.")
    print(f"Generated files: {len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
