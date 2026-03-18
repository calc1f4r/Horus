#!/usr/bin/env python3
"""Generate a Codex/GPT compatibility mirror from the Claude playbook tree.

The Claude files remain the source of truth. This script creates a repo-local
`codex/` mirror that keeps the original instructions intact while adding thin
Codex/GPT usage notes and rewriting `.claude/...` links to `codex/...`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_ROOT = REPO_ROOT / ".claude"
CODEX_ROOT = REPO_ROOT / "codex"

MIRROR_DIRS = ("agents", "skills", "resources", "rules")

TOOL_MAP = [
    ("Agent", "spawn a Codex sub-agent when available, otherwise execute the same workflow directly"),
    ("Bash", "run the equivalent shell command"),
    ("Read", "read the referenced file or exact line range"),
    ("Write", "create the required file or artifact"),
    ("Edit", "modify the existing file in place"),
    ("Glob", "search paths/files matching the pattern"),
    ("Grep", "search text patterns in the repo or target codebase"),
    ("WebFetch", "use direct web retrieval when available"),
    ("WebSearch", "use web search when needed"),
]

FLOW_GROUPS = {
    "Full Audit": [
        "audit-orchestrator",
        "audit-context-building",
        "function-analyzer",
        "system-synthesizer",
    ],
    "Invariants": [
        "invariant-writer",
        "invariant-reviewer",
        "invariant-indexer",
    ],
    "Discovery": [
        "invariant-catcher",
        "protocol-reasoning",
        "missing-validation-reasoning",
        "multi-persona-orchestrator",
        "persona-bfs",
        "persona-dfs",
        "persona-working-backward",
        "persona-state-machine",
        "persona-mirror",
        "persona-reimplementer",
    ],
    "PoC And Reporting": [
        "poc-writing",
        "issue-writer",
        "report-aggregator",
        "judge-orchestrator",
        "sherlock-judging",
        "cantina-judge",
        "code4rena-judge",
    ],
    "Formal Verification": [
        "chimera-setup",
        "medusa-fuzzing",
        "halmos-verification",
        "certora-verification",
        "certora-mutation-testing",
        "certora-sui-move-verification",
        "sui-prover-verification",
    ],
    "DB Maintenance": [
        "variant-template-writer",
        "defihacklabs-indexer",
        "solodit-fetching",
        "db-quality-monitor",
    ],
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_frontmatter(text: str) -> tuple[dict, str, str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.DOTALL)
    if match:
        raw = match.group(1)
        body = text[match.end() :]
        try:
            data = yaml.safe_load(raw) or {}
        except yaml.YAMLError:
            data = {}
        if not isinstance(data, dict):
            data = {}
        return data, raw, body, "fenced"

    simple_match = re.match(r"^((?:[A-Za-z0-9_-]+:\s*.*\n)+)---(?:\s*\n|$)", text)
    if simple_match:
        raw = simple_match.group(1).rstrip("\n")
        body = text[simple_match.end() :]
        try:
            data = yaml.safe_load(raw) or {}
        except yaml.YAMLError:
            data = {}
        if not isinstance(data, dict):
            data = {}
        return data, raw, body, "simple"

    return {}, "", text, "none"


def map_claude_path_to_codex(path: Path) -> Path:
    rel = path.relative_to(CLAUDE_ROOT)
    return CODEX_ROOT / rel


def infer_repo_target_from_basename(basename: str, label: str = "") -> Path | None:
    basename = unquote(basename)
    label_lower = label.lower()
    root_file = REPO_ROOT / basename
    if root_file.exists():
        return root_file

    agent = CLAUDE_ROOT / "agents" / basename
    if agent.exists():
        return agent

    resource = CLAUDE_ROOT / "resources" / basename
    if resource.exists():
        return resource

    rule = CLAUDE_ROOT / "rules" / basename
    if rule.exists():
        return rule

    candidates = []
    for skill in (CLAUDE_ROOT / "skills").glob("*/SKILL.md"):
        if skill.name == basename:
            candidates.append(skill)
        if skill.parent.name == basename.replace(".md", "") and "agent" not in label_lower:
            candidates.append(skill)

    if len(candidates) == 1:
        return candidates[0]
    return None


def rewrite_markdown_links(text: str, src_path: Path, dest_path: Path) -> str:
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def _replace(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        if target in {"link", "permalink"} or "{" in target or "}" in target:
            return match.group(0)

        anchor = ""
        path_part = target
        if "#" in target:
            path_part, anchor = target.split("#", 1)
            anchor = "#" + anchor

        resolved_target: Path | None = None
        if path_part.startswith(".claude/"):
            candidate = REPO_ROOT / path_part
            if candidate.exists():
                resolved_target = candidate
        elif path_part.startswith(("codex/", "DB/")):
            candidate = REPO_ROOT / path_part
            if candidate.exists():
                resolved_target = candidate
        else:
            candidate = (src_path.parent / path_part).resolve()
            if candidate.exists():
                resolved_target = candidate
            else:
                inferred = infer_repo_target_from_basename(Path(path_part).name, label=label)
                if inferred is not None:
                    resolved_target = inferred

        if resolved_target is None:
            return match.group(0)

        if resolved_target.is_relative_to(CLAUDE_ROOT):
            resolved_target = map_claude_path_to_codex(resolved_target)

        rewritten = Path(__import__("os").path.relpath(resolved_target, dest_path.parent.resolve())).as_posix()
        return f"[{label}]({rewritten}{anchor})"

    return pattern.sub(_replace, text)


def replace_claude_paths(text: str) -> str:
    replacements = {
        ".claude/resources/": "codex/resources/",
        ".claude/agents/": "codex/agents/",
        ".claude/skills/": "codex/skills/",
        ".claude/rules/": "codex/rules/",
        "`/.claude/": "`/codex/",
        "(/.claude/": "(/codex/",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def format_source_note(src_rel: str, source_hash: str, lines: list[str]) -> str:
    note_lines = [
        f"<!-- AUTO-GENERATED from `{src_rel}`; source_sha256={source_hash} -->",
        "",
        "> Codex/GPT compatibility layer.",
        f"> Source of truth: `{src_rel}`.",
    ]
    note_lines.extend(f"> {line}" for line in lines)
    note_lines.append("")
    return "\n".join(note_lines) + "\n"


def render_frontmatter(raw_frontmatter: str, style: str) -> str:
    if not raw_frontmatter:
        return ""
    if style == "fenced":
        return f"---\n{raw_frontmatter}\n---\n\n"
    if style == "simple":
        return f"{raw_frontmatter}\n---\n\n"
    return raw_frontmatter + "\n\n"


def build_agent_content(src_rel: str, dest_rel: str, text: str) -> tuple[str, dict]:
    meta, raw_frontmatter, body, style = split_frontmatter(text)
    source_hash = sha256_text(text)
    mapped_tools = [
        f"`{tool}` -> {meaning}" for tool, meaning in TOOL_MAP if tool in str(meta.get("tools", ""))
    ]
    note = format_source_note(
        src_rel,
        source_hash,
        [
            "The original agent metadata below is preserved verbatim.",
            "Interpret Claude-specific tool names as workflow intent rather than required syntax.",
            *mapped_tools,
            "If a Claude-only runtime feature is unavailable, follow the same procedure directly and produce the same on-disk artifacts.",
            "All `.claude/...` references in the mirrored body are rewritten to `codex/...`.",
        ],
    )
    src_path = REPO_ROOT / src_rel
    dest_path = REPO_ROOT / dest_rel
    transformed = rewrite_markdown_links(body, src_path, dest_path)
    transformed = replace_claude_paths(transformed)
    content = render_frontmatter(raw_frontmatter, style) + note + transformed.lstrip("\n")
    return content, meta


def build_skill_content(src_rel: str, dest_rel: str, text: str) -> tuple[str, dict]:
    meta, raw_frontmatter, body, style = split_frontmatter(text)
    source_hash = sha256_text(text)
    agent_name = meta.get("agent", "unknown")
    note = format_source_note(
        src_rel,
        source_hash,
        [
            "The original skill metadata below is preserved verbatim.",
            f"For Codex/GPT use, load `codex/agents/{agent_name}.md` as the implementation playbook.",
            "Follow any linked `codex/resources/*` references from that agent file.",
            "Relative skill links remain mirrored under `codex/skills/*`.",
        ],
    )
    src_path = REPO_ROOT / src_rel
    dest_path = REPO_ROOT / dest_rel
    transformed = rewrite_markdown_links(body, src_path, dest_path)
    transformed = replace_claude_paths(transformed)
    content = render_frontmatter(raw_frontmatter, style) + note + transformed.lstrip("\n")
    return content, meta


def build_markdown_mirror(src_rel: str, dest_rel: str, text: str, heading: str) -> str:
    source_hash = sha256_text(text)
    note = format_source_note(
        src_rel,
        source_hash,
        [
            f"This mirrored {heading} preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.",
        ],
    )
    src_path = REPO_ROOT / src_rel
    dest_path = REPO_ROOT / dest_rel
    transformed = rewrite_markdown_links(text, src_path, dest_path)
    transformed = replace_claude_paths(transformed)
    return note + transformed


def build_catalog(title: str, intro: str, rows: list[tuple[str, ...]], headers: tuple[str, ...]) -> str:
    lines = [f"# {title}", "", intro, ""]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join("-" * (len(header) + 2) for header in headers) + "|")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    return "\n".join(lines)


def discover_files() -> dict[str, list[Path]]:
    files: dict[str, list[Path]] = {name: [] for name in MIRROR_DIRS}
    for name in MIRROR_DIRS:
        root = CLAUDE_ROOT / name
        if not root.exists():
            continue
        files[name] = sorted(path for path in root.rglob("*") if path.is_file())
    return files


def build_root_readme(skill_count: int, agent_count: int, resource_count: int, rule_count: int) -> str:
    return "\n".join(
        [
            "# Codex Compatibility Layer",
            "",
            "This directory is a generated Codex/GPT-facing mirror of the Claude playbook tree in `.claude/`.",
            "",
            "It exists so the repository can preserve the original Claude skills, agents, resources, and rules unchanged while also giving Codex/GPT a portable, repo-local instruction surface.",
            "",
            "## What Is Mirrored",
            "",
            f"- `skills/`: {skill_count} mirrored skill wrappers",
            f"- `agents/`: {agent_count} mirrored agent playbooks",
            f"- `resources/`: {resource_count} mirrored reference files",
            f"- `rules/`: {rule_count} mirrored rule files",
            "",
            "## How To Use",
            "",
            "1. Start with `CATALOG.md` or `FLOWS.md` to pick the right skill/flow.",
            "2. Open the relevant file under `skills/`.",
            "3. Follow the linked implementation playbook under `agents/`.",
            "4. Load any referenced files from `resources/` or `rules/` as needed.",
            "",
            "## Sync",
            "",
            "Regenerate this layer after changing `.claude/` content:",
            "",
            "```bash",
            "python3 scripts/sync_codex_compat.py",
            "```",
            "",
            "Validate that the committed mirror is up to date:",
            "",
            "```bash",
            "python3 scripts/sync_codex_compat.py --check",
            "```",
            "",
        ]
    )


def build_flows(skill_meta: list[dict[str, str]]) -> str:
    skill_by_name = {item["name"]: item for item in skill_meta}
    lines = [
        "# Codex Flows",
        "",
        "These are task-level entry points for Codex/GPT. Each flow maps to one or more mirrored skills and agents under `codex/`.",
        "",
    ]
    for group_name, skill_names in FLOW_GROUPS.items():
        lines.append(f"## {group_name}")
        lines.append("")
        for skill_name in skill_names:
            item = skill_by_name.get(skill_name)
            if not item:
                continue
            lines.append(
                f"- `{skill_name}`: {item['description']} "
                f"See `codex/skills/{skill_name}/SKILL.md`."
            )
        lines.append("")
    return "\n".join(lines)


def generate() -> tuple[dict[str, str], dict[str, list[dict[str, str]]]]:
    outputs: dict[str, str] = {}
    manifest_entries: list[dict[str, str]] = []
    discovered = discover_files()

    skill_meta_rows: list[dict[str, str]] = []
    agent_meta_rows: list[dict[str, str]] = []
    resource_rows: list[tuple[str, str]] = []
    rule_rows: list[tuple[str, str]] = []

    for src_path in discovered["agents"]:
        src_rel = src_path.relative_to(REPO_ROOT).as_posix()
        dst_rel = src_path.relative_to(CLAUDE_ROOT).as_posix()
        dst_rel = f"codex/{dst_rel}"
        text = src_path.read_text(encoding="utf-8", errors="replace")
        content, meta = build_agent_content(src_rel, dst_rel, text)
        outputs[dst_rel] = content
        manifest_entries.append(
            {
                "source": src_rel,
                "dest": dst_rel,
                "source_sha256": sha256_text(text),
                "dest_sha256": sha256_text(content),
            }
        )
        agent_meta_rows.append(
            {
                "name": str(meta.get("name", src_path.stem)),
                "description": str(meta.get("description", "")).replace("\n", " ").strip(),
                "source": src_rel,
                "dest": dst_rel,
            }
        )

    for src_path in discovered["skills"]:
        src_rel = src_path.relative_to(REPO_ROOT).as_posix()
        dst_rel = src_path.relative_to(CLAUDE_ROOT).as_posix()
        dst_rel = f"codex/{dst_rel}"
        if src_path.name == "SKILL.md":
            text = src_path.read_text(encoding="utf-8", errors="replace")
            content, meta = build_skill_content(src_rel, dst_rel, text)
            outputs[dst_rel] = content
            manifest_entries.append(
                {
                    "source": src_rel,
                    "dest": dst_rel,
                    "source_sha256": sha256_text(text),
                    "dest_sha256": sha256_text(content),
                }
            )
            skill_meta_rows.append(
                {
                    "name": str(meta.get("name", src_path.parent.name)),
                    "description": str(meta.get("description", "")).replace("\n", " ").strip(),
                    "agent": str(meta.get("agent", "")),
                    "source": src_rel,
                    "dest": dst_rel,
                }
            )
        else:
            data = src_path.read_bytes()
            outputs[dst_rel] = data.decode("utf-8", errors="replace")
            manifest_entries.append(
                {
                    "source": src_rel,
                    "dest": dst_rel,
                    "source_sha256": sha256_bytes(data),
                    "dest_sha256": sha256_text(outputs[dst_rel]),
                }
            )

    for src_path in discovered["resources"]:
        src_rel = src_path.relative_to(REPO_ROOT).as_posix()
        dst_rel = src_path.relative_to(CLAUDE_ROOT).as_posix()
        dst_rel = f"codex/{dst_rel}"
        if src_path.suffix == ".md":
            text = src_path.read_text(encoding="utf-8", errors="replace")
            content = build_markdown_mirror(src_rel, dst_rel, text, "resource")
            outputs[dst_rel] = content
            manifest_entries.append(
                {
                    "source": src_rel,
                    "dest": dst_rel,
                    "source_sha256": sha256_text(text),
                    "dest_sha256": sha256_text(content),
                }
            )
        else:
            data = src_path.read_bytes()
            outputs[dst_rel] = data.decode("utf-8", errors="replace")
            manifest_entries.append(
                {
                    "source": src_rel,
                    "dest": dst_rel,
                    "source_sha256": sha256_bytes(data),
                    "dest_sha256": sha256_text(outputs[dst_rel]),
                }
            )
        resource_rows.append((src_path.relative_to(CLAUDE_ROOT / "resources").as_posix(), src_rel))

    for src_path in discovered["rules"]:
        src_rel = src_path.relative_to(REPO_ROOT).as_posix()
        dst_rel = src_path.relative_to(CLAUDE_ROOT).as_posix()
        dst_rel = f"codex/{dst_rel}"
        text = src_path.read_text(encoding="utf-8", errors="replace")
        content = build_markdown_mirror(src_rel, dst_rel, text, "rule")
        outputs[dst_rel] = content
        manifest_entries.append(
            {
                "source": src_rel,
                "dest": dst_rel,
                "source_sha256": sha256_text(text),
                "dest_sha256": sha256_text(content),
            }
        )
        rule_rows.append((src_path.relative_to(CLAUDE_ROOT / "rules").as_posix(), src_rel))

    skill_rows = [
        (
            item["name"],
            item["agent"],
            item["description"],
            f"`{item['source']}`",
        )
        for item in sorted(skill_meta_rows, key=lambda item: item["name"])
    ]
    agent_rows = [
        (
            item["name"],
            item["description"],
            f"`{item['source']}`",
        )
        for item in sorted(agent_meta_rows, key=lambda item: item["name"])
    ]
    resource_catalog_rows = [
        (f"`{name}`", f"`{source}`") for name, source in sorted(resource_rows)
    ]
    rule_catalog_rows = [
        (f"`{name}`", f"`{source}`") for name, source in sorted(rule_rows)
    ]

    outputs["codex/README.md"] = build_root_readme(
        skill_count=len(skill_meta_rows),
        agent_count=len(agent_meta_rows),
        resource_count=len(resource_rows),
        rule_count=len(rule_rows),
    )
    outputs["codex/CATALOG.md"] = "\n".join(
        [
            "# Codex Catalog",
            "",
            "Entry points for the generated Codex/GPT compatibility layer:",
            "",
            "- `README.md` — how to use the mirror",
            "- `FLOWS.md` — task-oriented entry points",
            "- `skills/CATALOG.md` — mirrored skills",
            "- `agents/CATALOG.md` — mirrored agent playbooks",
            "- `resources/CATALOG.md` — mirrored references",
            "- `rules/CATALOG.md` — mirrored rule files",
            "- `source-map.json` — source-to-mirror mapping with hashes",
            "",
        ]
    )
    outputs["codex/FLOWS.md"] = build_flows(skill_meta_rows)
    outputs["codex/skills/CATALOG.md"] = build_catalog(
        "Codex Skills Catalog",
        "Mirrored skill wrappers generated from `.claude/skills/*/SKILL.md`.",
        skill_rows,
        ("Skill", "Agent", "Description", "Source"),
    )
    outputs["codex/agents/CATALOG.md"] = build_catalog(
        "Codex Agents Catalog",
        "Mirrored agent playbooks generated from `.claude/agents/*.md`.",
        agent_rows,
        ("Agent", "Description", "Source"),
    )
    outputs["codex/resources/CATALOG.md"] = build_catalog(
        "Codex Resources Catalog",
        "Mirrored resources generated from `.claude/resources/**`.",
        resource_catalog_rows,
        ("Resource", "Source"),
    )
    outputs["codex/rules/CATALOG.md"] = build_catalog(
        "Codex Rules Catalog",
        "Mirrored rule files generated from `.claude/rules/*.md`.",
        rule_catalog_rows,
        ("Rule", "Source"),
    )
    outputs["codex/source-map.json"] = json.dumps(
        {
            "generatedFrom": ".claude",
            "entries": sorted(manifest_entries, key=lambda item: item["dest"]),
        },
        indent=2,
    ) + "\n"

    meta = {
        "skills": skill_meta_rows,
        "agents": agent_meta_rows,
        "resources": [{"path": row[0], "source": row[1]} for row in resource_rows],
        "rules": [{"path": row[0], "source": row[1]} for row in rule_rows],
    }
    return outputs, meta


def write_outputs(outputs: dict[str, str]) -> None:
    if CODEX_ROOT.exists():
        shutil.rmtree(CODEX_ROOT)
    CODEX_ROOT.mkdir(parents=True, exist_ok=True)
    for rel_path, content in sorted(outputs.items()):
        path = REPO_ROOT / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def check_outputs(outputs: dict[str, str]) -> int:
    mismatches: list[str] = []
    expected_paths = {path for path in outputs}
    actual_paths = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in CODEX_ROOT.rglob("*")
        if path.is_file()
    } if CODEX_ROOT.exists() else set()

    missing = sorted(expected_paths - actual_paths)
    unexpected = sorted(actual_paths - expected_paths)

    for path in missing:
        mismatches.append(f"missing: {path}")
    for path in unexpected:
        mismatches.append(f"unexpected: {path}")

    for rel_path, expected in sorted(outputs.items()):
        path = REPO_ROOT / rel_path
        if not path.exists():
            continue
        actual = path.read_text(encoding="utf-8", errors="replace")
        if actual != expected:
            mismatches.append(f"outdated: {rel_path}")

    if mismatches:
        for mismatch in mismatches:
            print(mismatch)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync the Codex compatibility mirror from .claude/")
    parser.add_argument("--check", action="store_true", help="Verify the committed codex/ mirror is up to date")
    args = parser.parse_args()

    outputs, _ = generate()
    if args.check:
        return check_outputs(outputs)

    write_outputs(outputs)
    print(f"Wrote {len(outputs)} files under {CODEX_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
