---
name: "manipulation-feasibility-analyst"
description: "Quantify the cost of market manipulation for every price and liquidity input in scope and map the MEV extraction surface. Inventories oracles with their consumers, computes required capital against real tick-level depth and the actual TWAP window constant, verifies \"manipulation is too expensive\" claims with numbers, and ranks user-facing flows by extractability. Use in the Phase 4 economic lane when any price feed or DEX interaction is in scope."
---
Use the [manipulation-feasibility-analyst subagent](../../../.codex/agents/manipulation-feasibility-analyst.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<codebase-path>`.

Quantify manipulation feasibility for `<codebase-path>`.

## The gap this closes

Oracle hunt cards detect manipulation **patterns**. This checks whether manipulation is **economically feasible against real liquidity depth** for this deployment — the difference between "uses TWAP, safe" and "TWAP window is 30 min over a $200k pool backing $8M of borrows".

## Feasibility table

| Column | Rule |
|--------|------|
| Depth | Tick-level / reserve data — **never nominal TVL** |
| Window | The constant read from the target's code — never assumed |
| Required capital | Computed on the pool's actual curve |
| Extractable gain | Summed across **all** consumers, traced transitively |
| Verdict | `FEASIBLE` / `MARGINAL` / `NOT FEASIBLE` / `UNVERIFIED (assumption)` |

Documented TWAP and manipulation-resistance claims in READMEs and NatSpec are checked against the deployed constants; a mismatch is a finding on its own.

## Output

- `audit-output/04g-manipulation-findings.md` — feasibility table, findings, MEV exposure map, and an "assumed-safe but unchecked" list
- `FEASIBLE` scenarios handed to `economic-attack-simulator`

## Related skills

- [economic-attack-simulator](../economic-attack-simulator/SKILL.md) — full profit modelling downstream
- [risk-parameter-reviewer](../risk-parameter-reviewer/SKILL.md) — oracle config coherence
- [invariant-catcher](../invariant-catcher/SKILL.md) — oracle pattern hunting
