name: db-quality-monitor
description: "Monitor and fix the Vulnerability Database pipeline: 4-tier architecture integrity, manifest generation, hunt card alignment, TEMPLATE.md compliance, line-range accuracy, protocolContext routing, keyword index fidelity, and duplicate detection. Use for periodic DB health checks, CI validation after entry changes, or diagnosing why an audit agent received wrong context."
context: fork
agent: db-quality-monitor
argument-hint: "[--fix] [--check=manifests|huntcards|entries|all]"
disable-model-invocation: true
---

<!-- AUTO-GENERATED from `.claude/skills/db-quality-monitor/SKILL.md`; source_sha256=6a2e84346efe3bf0be716551f75217969b70bc72c592b99f6bba060609f0a067 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/db-quality-monitor/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/db-quality-monitor.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Run quality checks on the Vulnerability Database. $ARGUMENTS

## What this checks

| Check | What it validates |
|-------|-------------------|
| **4-tier integrity** | index.json → manifests → hunt cards → .md entries all link correctly |
| **Line ranges** | Manifest `lineStart`/`lineEnd` match actual content in .md files |
| **Hunt card alignment** | Every manifest pattern has a matching hunt card |
| **TEMPLATE.md compliance** | Entries follow required frontmatter and section structure |
| **Keyword index** | `keywords.json` covers all codeKeywords from manifests |
| **protocolContext routing** | Protocol types map to correct manifests |
| **Duplicate detection** | No two entries have the same root cause |
| **Script health** | `scripts/generate_manifests.py` runs without errors |

## Auto-fix mode

With `--fix`, spawns sub-agents to:
- Regenerate manifests from source .md files
- Patch frontmatter in non-compliant entries
- Update line ranges in manifests
- Remove duplicate entries

## Related skills

- [/variant-template-writer](../variant-template-writer/SKILL.md) — Creates entries this skill validates
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Pipeline that depends on DB quality
- [/invariant-catcher](../invariant-catcher/SKILL.md) — Consumer of hunt cards this skill validates
