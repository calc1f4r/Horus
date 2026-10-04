---
name: "db-quality-monitor"
description: "Monitor and fix the Horus pipeline: 4-tier architecture integrity, manifest generation, hunt card alignment, TEMPLATE.md compliance, line-range accuracy, protocolContext routing, keyword index fidelity, and duplicate detection. Use for periodic DB health checks, CI validation after entry changes, or diagnosing why an audit agent received wrong context."
---
Use the [db-quality-monitor subagent](../../../.codex/agents/db-quality-monitor.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `[--fix] [--check=manifests|huntcards|entries|all]`.

Run quality checks on Horus. <arguments>

## What this checks

| Check | What it validates |
|-------|-------------------|
| **4-tier integrity** | index.json → manifests → hunt cards → .md entries all link correctly |
| **Line ranges** | Manifest `lineStart`/`lineEnd` match actual content in .md files |
| **Hunt card alignment** | Every manifest pattern has a matching hunt card |
| **TEMPLATE.md compliance** | Entries follow required frontmatter and section structure |
| **Keyword index** | `keywords.json` covers all codeKeywords from manifests |
| **protocolContext routing** | Protocol types map to correct manifests |
| **Duplicate review** | Similar entries are reviewed against source identity and distinct pattern context; shared root cause alone is not duplication |
| **Script health** | `scripts/generate_manifests.py` runs without errors |

## Auto-fix mode

With `--fix`, spawns sub-agents to:
- Regenerate manifests from source .md files
- Patch frontmatter using verified source evidence; retain uncertainty when evidence is missing
- Correct line ranges through the generator and regenerate manifests
- Report duplicate candidates with source references; preserve entries and distinct variants

Do not change severity from marker frequency or similarity alone. Preserve source
ratings and verify unique supporting findings before applying the documented
consensus rule. Generated hints and linked report counts are not verified evidence.

For a reproducible quality backlog, optionally run:

```bash
python3 scripts/db_quality_check.py --json-output audit-output/db-quality.json
```

Report checks run, sample sizes, unresolved issues, and checks not run. Structural
success does not establish factual completeness or independent source validation.

## Related skills

- [variant-template-writer](../variant-template-writer/SKILL.md) — Creates entries this skill validates
- [audit-orchestrator](../audit-orchestrator/SKILL.md) — Pipeline that depends on DB quality
- [invariant-catcher](../invariant-catcher/SKILL.md) — Consumer of hunt cards this skill validates
