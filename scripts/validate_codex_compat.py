#!/usr/bin/env python3
"""Validate the generated Codex compatibility layer."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from sync_codex_compat import check_outputs, generate, sha256_text, split_frontmatter


REPO_ROOT = Path(__file__).resolve().parent.parent
CODEX_ROOT = REPO_ROOT / "codex"
CLAUDE_ROOT = REPO_ROOT / ".claude"


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

    if target.startswith(("codex/", "DB/")):
        return (REPO_ROOT / target).resolve()
    if target.startswith("/"):
        # Repo-local docs in this mirror use relative links, so an absolute-like
        # path here is intentionally ignored rather than treated as filesystem root.
        return None

    return (base / target).resolve()


def validate_source_map(errors: list[str]) -> None:
    source_map_path = CODEX_ROOT / "source-map.json"
    if not source_map_path.exists():
        errors.append("missing codex/source-map.json")
        return

    data = json.loads(source_map_path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    if not isinstance(entries, list):
        errors.append("codex/source-map.json has invalid entries format")
        return

    mapped_destinations = set()
    for entry in entries:
        source = REPO_ROOT / entry["source"]
        dest = REPO_ROOT / entry["dest"]
        mapped_destinations.add(dest.resolve())

        if not source.exists():
            errors.append(f"source-map missing source file: {entry['source']}")
            continue
        if not dest.exists():
            errors.append(f"source-map missing mirrored file: {entry['dest']}")
            continue

        actual_source_hash = sha256_text(source.read_text(encoding="utf-8", errors="replace"))
        actual_dest_hash = sha256_text(dest.read_text(encoding="utf-8", errors="replace"))
        if actual_source_hash != entry["source_sha256"]:
            errors.append(f"source hash mismatch for {entry['source']}")
        if actual_dest_hash != entry["dest_sha256"]:
            errors.append(f"dest hash mismatch for {entry['dest']}")

    generated_helpers = {
        (CODEX_ROOT / "README.md").resolve(),
        (CODEX_ROOT / "CATALOG.md").resolve(),
        (CODEX_ROOT / "FLOWS.md").resolve(),
        (CODEX_ROOT / "agents" / "CATALOG.md").resolve(),
        (CODEX_ROOT / "skills" / "CATALOG.md").resolve(),
        (CODEX_ROOT / "resources" / "CATALOG.md").resolve(),
        (CODEX_ROOT / "rules" / "CATALOG.md").resolve(),
    }

    for path in CODEX_ROOT.rglob("*"):
        if (
            path.is_file()
            and path.name != "source-map.json"
            and path.resolve() not in mapped_destinations
            and path.resolve() not in generated_helpers
        ):
            errors.append(f"codex file missing from source-map: {path.relative_to(REPO_ROOT).as_posix()}")


def validate_skill_agent_mapping(errors: list[str]) -> None:
    for skill_path in sorted((CODEX_ROOT / "skills").glob("*/SKILL.md")):
        text = skill_path.read_text(encoding="utf-8", errors="replace")
        meta, _, _, _ = split_frontmatter(text)
        agent = meta.get("agent")
        if not agent:
            errors.append(f"{skill_path.relative_to(REPO_ROOT).as_posix()}: missing agent metadata")
            continue
        agent_path = CODEX_ROOT / "agents" / f"{agent}.md"
        if not agent_path.exists():
            errors.append(
                f"{skill_path.relative_to(REPO_ROOT).as_posix()}: missing mapped agent {agent_path.relative_to(REPO_ROOT).as_posix()}"
            )


def validate_markdown_links(errors: list[str]) -> None:
    markdown_files = [path for path in CODEX_ROOT.rglob("*.md") if path.is_file()]
    concrete_ref_pattern = re.compile(r"codex/(?:skills|agents|resources|rules)/[A-Za-z0-9._/-]+\.(?:md|ql|yaml)")

    for path in sorted(markdown_files):
        text = path.read_text(encoding="utf-8", errors="replace")

        for link in iter_markdown_links(text):
            if link in {"link", "permalink"} or "{" in link or "}" in link or "..." in link:
                continue
            resolved = resolve_local_link(path.parent, link)
            if resolved is not None and not resolved.exists():
                errors.append(
                    f"{path.relative_to(REPO_ROOT).as_posix()}: broken local link -> {link}"
                )

        for match in concrete_ref_pattern.findall(text):
            ref_path = REPO_ROOT / match
            if not ref_path.exists():
                errors.append(
                    f"{path.relative_to(REPO_ROOT).as_posix()}: missing concrete codex path reference {match}"
                )


def validate_counts(errors: list[str]) -> None:
    source_counts = {
        "skills": len([p for p in (CLAUDE_ROOT / "skills").rglob("*") if p.is_file()]),
        "agents": len(list((CLAUDE_ROOT / "agents").glob("*.md"))),
        "resources": len([p for p in (CLAUDE_ROOT / "resources").rglob("*") if p.is_file()]),
        "rules": len(list((CLAUDE_ROOT / "rules").glob("*.md"))),
    }
    mirror_counts = {
        "skills": len([p for p in (CODEX_ROOT / "skills").rglob("*") if p.is_file()]),
        "agents": len(list((CODEX_ROOT / "agents").glob("*.md"))),
        "resources": len([p for p in (CODEX_ROOT / "resources").rglob("*") if p.is_file()]),
        "rules": len(list((CODEX_ROOT / "rules").glob("*.md"))),
    }

    if mirror_counts["agents"] != source_counts["agents"] + 1:
        errors.append(
            f"unexpected codex agent count: source={source_counts['agents']} mirror={mirror_counts['agents']}"
        )
    if mirror_counts["rules"] != source_counts["rules"] + 1:
        errors.append(
            f"unexpected codex rule count: source={source_counts['rules']} mirror={mirror_counts['rules']}"
        )
    if mirror_counts["resources"] != source_counts["resources"] + 1:
        errors.append(
            f"unexpected codex resource count: source={source_counts['resources']} mirror={mirror_counts['resources']}"
        )
    if mirror_counts["skills"] != source_counts["skills"] + 1:
        errors.append(
            f"unexpected codex skill file count: source={source_counts['skills']} mirror={mirror_counts['skills']}"
        )


def main() -> int:
    outputs, _ = generate()
    errors: list[str] = []

    parity_status = check_outputs(outputs)
    if parity_status != 0:
        errors.append("codex mirror parity check failed")

    validate_source_map(errors)
    validate_skill_agent_mapping(errors)
    validate_markdown_links(errors)
    validate_counts(errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    print("Codex compatibility validation passed.")
    print(f"Mirrored files: {len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
