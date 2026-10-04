# Full audit

Run this when you have a target codebase and want a contest-grade review of it, not a quick lookup.

## Start it

```
/agent audit-orchestrator <codebase-path> [protocol-hint] [--static-only] [--judge=sherlock|cantina|code4rena] [--discovery-rounds=N]
```

Flags:

- `--static-only` skips PoC execution and formal verification. Findings come out with code-level evidence only. Use it when the target has no test framework or you want speed.
- `--judge=X` runs one platform judge instead of all three. Default is Sherlock, Cantina, and Code4rena in parallel with a 2-of-3 consensus.
- `--discovery-rounds=N` sets how many discovery passes run. Default 2, max 5. Later rounds attack surface the earlier rounds missed.

Everything lands in `audit-output/`. Each phase writes its own file there, and `pipeline-state.md` tracks what ran.

## What happens, phase by phase

**Phase 0, graph foundation.** The orchestrator builds a code graph with graphify and, for Solidity, the blockchain AST extractor. Soft gate: if graph tools are missing, the audit continues without graph features and logs the skip.

**Phase 1, recon.** `recon-specialist` detects the protocol type, decides which files are in scope and why, maps the external surface (oracles, deployed addresses, privileged roles), and writes `00-scope.md`. The machine-readable JSON block at the bottom of that file is a contract: `grep_prune.py` and `partition_shards.py` consume it through `--scope-file` so later scans skip out-of-scope files. With `--diff=<base-ref>`, only the changed code and its blast radius count as scope.

**Phase 2, context.** `audit-context-building` fans out one `function-analyzer` sub-agent per contract, then `system-synthesizer` merges their notes into `01-context.md`. You get an actor model, trust boundaries, and an inventory of what every function does.

**Phase 3, invariants.** `invariant-writer` drafts the properties the protocol must hold (`02-invariants.md`), then `invariant-reviewer` hardens them into `02-invariants-reviewed.md`. Discovery in phase 4 tries to break these.

**Phase 4, discovery.** This is the widest part of the run. Four lanes run in parallel each round:

| Lane | Skill or agent | Finds |
|---|---|---|
| 4A | `invariant-catcher` | Known patterns from the DB, matched by grep |
| 4B | `protocol-reasoning` | Novel bugs by domain reasoning, seeded from DB root causes |
| 4C | `multi-persona-orchestrator` | Six personas attack the same code from different angles |
| 4D | `missing-validation-reasoning` | Missing checks in constructors, setters, and input paths |

Before round 1, `prior-art-matcher` fingerprints the target against known forks (Aave, Uniswap, Curve, and others) and pulls incidents that already happened in that lineage. Hits become high-priority seeds.

Three more lanes run when scope calls for them: `tokenomics-auditor` (4E) for token, vesting, and treasury contracts, `risk-parameter-reviewer` (4F) for lending parameters, and `manipulation-feasibility-analyst` (4G) for anything reading a price feed. 4G checks whether "manipulation is too expensive" claims hold up against real pool depth, with numbers.

Between rounds, `attack-coverage-tracker` writes `attack-coverage.json` and a `round-N-targets.md` file so the next round attacks functions nobody has touched yet instead of re-reading the hot paths.

**Phase 5, triage.** `finding-merger` clusters findings by root cause, re-reads the cited code to try to disprove each one, and writes `05-findings-triaged.md`. Every input finding is accounted for: it lands in a cluster or is recorded as dismissed with a reason. The count must balance to zero unaccounted.

**Phase 6, PoCs.** For CRITICAL and HIGH findings, `poc-writing` writes exploit tests and runs them. A passing PoC is mechanical proof. Phase 6a runs `economic-attack-simulator` on high-severity economic findings: it models flash-loan cost, slippage, gas, and MEV competition, and returns PROFITABLE, CONDITIONAL, or UNPROFITABLE with the binding constraint named. UNPROFITABLE findings skip PoC spend.

**Phase 7, verification.** `medusa-fuzzing`, `halmos-verification`, and `certora-verification` build harnesses from the reviewed invariants and run them. Violations map back to findings or create new ones.

**Phases 8 to 10, judging.** Judges screen the triaged findings for validity (phase 8), `issue-writer` polishes the survivors into submission-ready write-ups (phase 9), and the same judges re-review the polished issues line by line (phase 10). Profitability verdicts from 6a count as impact evidence here: an UNPROFITABLE verdict with a named constraint is grounds to downgrade an economic-loss finding.

**Phase 10b, remediation safety.** Before the report ships, `remediation-safety-checker` verifies every fix the report itself recommends. Each one gets SAFE, RISKY, or UNSAFE across six checks, including whether the fix pattern is itself a known-vulnerable pattern in the DB. The report cannot ship an UNSAFE remediation.

**Phase 11, report.** `report-aggregator` assembles `CONFIRMED-REPORT.md` from judge-verified findings only, with code citations checked against the target.

**Phase 12, optional flywheel.** `findings-db-synthesizer` turns the confirmed findings into new DB entries and invariants so the next audit starts stronger. Opt-in because it writes to the DB.

## What you get

`audit-output/CONFIRMED-REPORT.md` plus the full artifact trail: scope, context, invariants, per-lane findings, PoCs, verdicts, and coverage numbers.
