---
name: audit-orchestrator
description: "Run a full end-to-end smart contract security audit. Orchestrates 20+ sub-agents across 11 phases: reconnaissance, context building, invariant extraction, iterative discovery (DB hunting + reasoning + multi-persona + validation gaps), merge & triage, PoC generation, formal verification, judging, issue polishing, deep review, and report assembly. Use when auditing an unfamiliar codebase, running a contest-grade security review, or performing comprehensive vulnerability discovery."
context: fork
agent: audit-orchestrator
argument-hint: <codebase-path> [protocol-hint] [--static-only] [--judge=sherlock|cantina|code4rena] [--discovery-rounds=N]
---

Run a complete security audit on the codebase at `$ARGUMENTS`.

## Pipeline overview

| Phase | What happens |
|-------|-------------|
| 1. Reconnaissance | Protocol detection, scope definition, manifest resolution |
| 2. Context Building | Spawns `audit-context-building` for deep code analysis |
| 3. Invariant Extraction | Spawns `invariant-writer` → `invariant-reviewer` |
| 4. Iterative Discovery | N rounds of 4-way parallel fan-out (DB hunting, reasoning, multi-persona, validation gaps) |
| 5. Merge & Triage | Cross-source correlation, dedup, falsification, severity assignment |
| 6. PoC Generation | Spawns `poc-writing` per CRITICAL/HIGH finding (skip with `--static-only`) |
| 7. Formal Verification | Spawns `medusa-fuzzing`, `certora-verification`, `halmos-verification` (skip with `--static-only`) |
| 8. Pre-Judging | Judge(s) screen all triaged findings |
| 9. Issue Polishing | Spawns `issue-writer` for valid findings |
| 10. Deep Review | Judge(s) do line-by-line verification |
| 11. Report Assembly | Produces `audit-output/CONFIRMED-REPORT.md` |

## Flags

- `--static-only` — Skip Phases 6-7 (no PoC/FV). Findings confirmed through judging only.
- `--judge=X` — Use a single judge instead of all 3. Options: `sherlock`, `cantina`, `code4rena`.
- `--discovery-rounds=N` — Number of iterative discovery rounds (default: 2, max: 5).

## Output

All artifacts go to `audit-output/`:
- `CONFIRMED-REPORT.md` — Final report with only judge-verified findings
- `pipeline-state.md` — Pipeline progress tracker
- `00-scope.md` through `10-deep-review.md` — Phase artifacts

## Related skills

- [/audit-context-building](../audit-context-building/SKILL.md) — Deep codebase analysis (Phase 2)
- [/invariant-writer](../invariant-writer/SKILL.md) — Invariant extraction (Phase 3)
- [/poc-writing](../poc-writing/SKILL.md) — Exploit test generation (Phase 6)
- [/sherlock-judging](../sherlock-judging/SKILL.md) — Sherlock criteria validation (Phase 8/10)
- [/cantina-judge](../cantina-judge/SKILL.md) — Cantina criteria validation (Phase 8/10)
- [/code4rena-judge](../code4rena-judge/SKILL.md) — Code4rena criteria validation (Phase 8/10)
