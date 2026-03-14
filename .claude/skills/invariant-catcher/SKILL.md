---
name: invariant-catcher
description: "Hunt for known vulnerability patterns in smart contract codebases using the Vulnerability Database (DB/). Language-agnostic. Searches by vulnerability class, extracts detection patterns from DB entries, runs grep/ripgrep against target code, and generates structured findings. Use when performing variant analysis, systematically searching for known vulnerability classes, or doing DB-powered hunting during an audit."
context: fork
agent: invariant-catcher
argument-hint: <codebase-path> [vulnerability-topic]
---

Hunt for vulnerability patterns in the codebase. Arguments: `$ARGUMENTS`.

## What this does

1. **Load hunt cards** — Reads `DB/manifests/huntcards/all-huntcards.json` for detection patterns
2. **Grep pruning** — Runs each card's `grep` pattern against target code, discards zero-hit cards
3. **Shard partitioning** — Groups surviving cards into shards of 50-80 patterns by category
4. **Per-shard analysis** — For each shard, executes micro-directive `check` steps against matching code
5. **Evidence lookup** — For true/likely positives, reads the full DB entry via `card.ref` + `card.lines`
6. **Findings report** — Produces structured findings with root cause, impact, and code references

## Output

- `audit-output/03-findings-shard-<id>.md` — Per-shard findings

## Related skills

- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 4A)
- [/protocol-reasoning](../protocol-reasoning/SKILL.md) — Complementary reasoning-based discovery (Phase 4B)
- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Complementary persona-based discovery (Phase 4C)
- [/db-quality-monitor](../db-quality-monitor/SKILL.md) — Validates the DB hunt cards this skill depends on
