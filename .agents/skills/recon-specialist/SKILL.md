---
name: "recon-specialist"
description: "Resolve audit scope before any hunting begins — protocol type detection and DB manifest routing, in-scope vs out-of-scope file resolution with rationale, external surface mapping, and diff scoping with blast radius against a base ref. Produces 00-scope.md with a machine-readable scope block. Use at the start of an audit or when scope must be established or re-established."
---
Use the [recon-specialist subagent](../../../.codex/agents/recon-specialist.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<codebase-path> [--diff=<base-ref>]`.

Resolve audit scope for `<codebase-path>`.

## Modes

| Mode | Trigger | Scope |
|------|---------|-------|
| Full | default | Source roots minus excluded-by-rule paths |
| Diff | `--diff=<ref>` | Changed files **plus blast radius** (callers, callees, shared state, depth 2) |

## What it produces

`audit-output/00-scope.md` — protocol classification with confidence, resolved DB manifests, in/out-of-scope tables with the rule for every exclusion, external surface (oracles, addresses, roles, tokens, fee receivers), dependency list, and a machine-readable JSON scope block consumed by `grep_prune.py` and `partition_shards.py` via `--scope-file`.

## Requirements

- Target codebase path readable; `git` available for diff mode
- `DB/index.json` present for manifest routing

## Related skills

- [audit-orchestrator](../audit-orchestrator/SKILL.md) — parent pipeline (Phase 1)
- [audit-context-building](../audit-context-building/SKILL.md) — downstream (Phase 2)
- [mitigation-reviewer](../mitigation-reviewer/SKILL.md) — consumes diff mode
