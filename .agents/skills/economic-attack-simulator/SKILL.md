---
name: "economic-attack-simulator"
description: "Answer the question poc-writing cannot — is the attack profitable, and by how much? Builds an attacker profit model per candidate covering flash-loan fees, gas, slippage on the real AMM curve, achievable oracle deviation and MEV competition, then returns PROFITABLE / CONDITIONAL / UNPROFITABLE with the binding constraint named. Use as a Phase 6 gate before spending PoC budget, or to give judges dollar-quantified impact."
---
Use the [economic-attack-simulator subagent](../../../.codex/agents/economic-attack-simulator.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `[audit-output-dir]`.

Model attacker profitability for findings in `<arguments>`.

## Verdicts

| Verdict | Required output |
|---------|-----------------|
| `PROFITABLE (validated)` | Net USD figure with full cost/gain breakdown |
| `CONDITIONAL` | The exact market regime that flips it profitable, and how reachable it is |
| `UNPROFITABLE` | **The binding constraint, named** — which term dominates |
| `N/A` | Non-economic impact (griefing / DoS / brick) — severity unaffected |

## Model

```
net_profit = gain - (flash_fee + gas + slippage_in + slippage_out + holding_cost + mev_discount)
```

Slippage uses the actual curve (constant product, concentrated-liquidity tick depth, or StableSwap invariant) — never a linear approximation. Every number is sourced on-chain/config or explicitly labelled `ASSUMED`.

## Calibration

Replay a `DeFiHackLabs/` exploit through the model; net profit must land within 2× of the reported loss. The calibration case and its error are recorded in the output.

## Output

- `audit-output/06-profitability.md` + per-finding profit sections for judges

## Related skills

- [manipulation-feasibility-analyst](../manipulation-feasibility-analyst/SKILL.md) — supplies manipulation cost
- [poc-writing](../poc-writing/SKILL.md) — proves executability; this proves profitability
- [attack-graph-synthesizer](../attack-graph-synthesizer/SKILL.md) — supplies attack chains
