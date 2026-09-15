---
name: risk-parameter-reviewer
description: Adversarially review protocol risk parameters — LTV, liquidation threshold and bonus, close factor, caps, interest-rate kink and slopes, oracle deviation config, and stablecoin peg mechanics. Extracts the parameter table with citations, runs named invariant checks, and sweeps market scenarios to find the breaking regime. Use in the Phase 4 economic lane when lending or stablecoin mechanics are in scope.
argument-hint: "<codebase-path>"
context: fork
agent: risk-parameter-reviewer
---

Review risk parameters in `$ARGUMENTS`.

## Named invariant checks

| ID | Check |
|----|-------|
| I1 | No self-liquidation profit |
| I2 | No riskless leverage loop |
| I3 | Non-negative spread (supply-side solvency) across all utilisation, including the kink |
| I4 | Peg arbitrage bounded, restorative, and unblockable |
| I5 | Bad-debt containment path exists and is bounded |

Each runs per asset with the arithmetic shown. A parameter finding without numbers will not survive judging.

## Scenario sweep

Parameter table × market moves (price −20/−35/−50%, liquidity −50/−80%, utilisation → 100%, correlated crash). Every violation names the parameter, the market move, and the loss mechanism.

## Output

- `audit-output/04f-risk-param-findings.md` + parameter risk table (asset × parameter × verdict × breaking scenario)

Skips fast with a logged reason when no lending or stablecoin mechanics are in scope.

## Related skills

- [/tokenomics-auditor](../tokenomics-auditor/SKILL.md) — supply, emission, vesting
- [/manipulation-feasibility-analyst](../manipulation-feasibility-analyst/SKILL.md) — oracle manipulation cost
- [/economic-attack-simulator](../economic-attack-simulator/SKILL.md) — profit modelling
