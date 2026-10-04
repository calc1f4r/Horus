---
name: "tokenomics-auditor"
description: "Review the value-flow layer — token supply and emission, vesting and unlocks, treasury and fee splits, and actor incentives — as code paths that move money over time. Verifies contract math against documented tokenomics with worked tables, finds emission drift, vesting rounding and wrong-bucket accounting, and proposes economic invariants. Use in the Phase 4 economic lane when token, emission, vesting, or treasury contracts are in scope."
---
Use the [tokenomics-auditor subagent](../../../.codex/agents/tokenomics-auditor.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<codebase-path>`.

Audit the value-flow layer of `<codebase-path>`.

## Coverage matrix

Recorded in the output so a run is verifiable, not vibe-based. Each cell marked `checked` / `not-applicable` / `blocked (reason)`.

| Dimension | Cells |
|-----------|-------|
| Supply | max supply, mint authority, mint paths, burn paths |
| Emission | rate curve, epoch decay, budget vs actual, rate-change authority |
| Vesting | cliff math, linear math, revocability, acceleration, beneficiary |
| Treasury | withdrawal authority, timelock, multisig thresholds |
| Fees | split correctness, recipient validity, rounding direction, FoT interaction |
| Incentives | deviation profit per actor, farm-and-dump, bribe economics, exit-scam threshold |

## Deliverable shape

Emission and vesting findings ship as **worked tables** (expected vs computed at sampled timestamps), not prose. Docs-vs-code drift is quantified, not described.

## Output

- `audit-output/04e-tokenomics-findings.md`
- At least one `invariants/tokenomics/` candidate per engagement

Skips fast with a logged reason when no value-flow surface is in scope.

## Related skills

- [risk-parameter-reviewer](../risk-parameter-reviewer/SKILL.md) — lending params & IRM
- [economic-attack-simulator](../economic-attack-simulator/SKILL.md) — profit modelling for deviations found here
- [invariant-writer](../invariant-writer/SKILL.md) — invariant conventions
