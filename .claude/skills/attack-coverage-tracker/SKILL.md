---
name: attack-coverage-tracker
description: Meta-agent that finds no bugs and makes every other attacker find more. Maintains a cumulative ledger of which lane attacked which function in which round with what outcome, detects never-attacked, pattern-only, unexercised-invariant and untraversed-edge gaps, and emits round targets so later rounds explore new surface instead of re-attacking round-1 hits. Use between Phase 4 discovery rounds.
argument-hint: "[audit-output-dir] [round-number]"
context: fork
agent: attack-coverage-tracker
---

Track and steer attack coverage for `$ARGUMENTS`.

## Core accounting rule

`verified-clean` (a lane examined it and found nothing) is **coverage**. `never-attacked` is a gap. Conflating them is the failure mode this agent exists to prevent — DEAD_END entries in `memory-state.json` are the primary signal for the distinction.

## Four gap classes

1. **Never-attacked** — external/privileged functions with zero attacks
2. **Pattern-only** — hit by 4A hunt cards but never by a reasoning lane
3. **Unexercised invariants** — no finding and no DEAD_END ever tried to break them
4. **Untraversed edges** — cross-contract edges nobody walked *(skipped with a warning when `graph/graph.json` is absent)*

## Outputs

| File | When |
|------|------|
| `audit-output/attack-coverage.json` | Every invocation — **cumulative, never truncated** |
| `audit-output/round-N-targets.md` | Before each round > 1, includes a "Do Not Re-attack" list |
| `audit-output/coverage-report.md` | Before Phase 5, every percentage stating its denominator |

Emits no findings, ever.

## Related skills

- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — parent pipeline (between Phase 4 rounds)
- [/finding-merger](../finding-merger/SKILL.md) — Phase 5, consumes the coverage report
- [/attack-graph-synthesizer](../attack-graph-synthesizer/SKILL.md) — supplies the edge inventory
