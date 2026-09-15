---
# Core Classification
protocol: Cap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62172
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/990
source_link: none
github_link: https://github.com/sherlock-audit/2025-07-cap-judging/issues/638

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - ustas
  - montecristo
  - 0xzey
  - KrisRenZo
  - Drynooo
---

## Vulnerability Title

M-10: `ViewLogic::maxLiquidatable()` doesn't take the bonus into account, making the agent liquidatable again

### Overview


The bug report talks about a problem found in a code called "ViewLogic::maxLiquidatable()" which is used to calculate the maximum amount of debt that can be liquidated. This calculation is not accurate because it does not take into account a bonus that affects the final health of the system. This can lead to multiple liquidations and heavy losses for the agent. The bug report suggests including the bonus in the calculation to avoid this issue. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-07-cap-judging/issues/638 

## Found by 
0x73696d616f, 0xzey, Albert\_Mei, Drynooo, KrisRenZo, anirruth\_, maxim371, montecristo, ustas

### Summary

[ViewLogic::maxLiquidatable()](https://github.com/sherlock-audit/2025-07-cap/blob/main/cap-contracts/contracts/lendingPool/libraries/ViewLogic.sol#L91-L93) computes the maximum debt to liquidate such that the resulting target health is exactly the desired:
```solidity
maxLiquidatableAmount = (($.targetHealth * totalDebt) - (totalDelegation * liquidationThreshold)) * decPow
    / (($.targetHealth - liquidationThreshold) * assetPrice);
```
However, this is inaccurate due to the [bonus](https://github.com/sherlock-audit/2025-07-cap/blob/main/cap-contracts/contracts/lendingPool/libraries/ViewLogic.sol#L192), which affects the final health as it slashes more than the debt is repays.

Thus, it will trigger more than 1 liquidations in certain conditions and lead to heavy losses for the agent.

### Root Cause

In `ViewLogic.sol:91`, it doesn't include the bonus.

### Internal Pre-conditions

None

### External Pre-conditions

None

### Attack Path

1. Agent is liquidated twice in a row due to the `ViewLogic::maxLiquidatable()` calculation not taking into account the bonus.

### Impact

Agent suffers more losses than supposed.

### PoC

_No response_

### Mitigation

Include the bonus in the debt to repay so the health factor equals the target.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cap |
| Report Date | N/A |
| Finders | ustas, montecristo, 0xzey, KrisRenZo, Drynooo, 0x73696d616f, Albert\_Mei, anirruth\_, maxim371 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-07-cap-judging/issues/638
- **Contest**: https://app.sherlock.xyz/audits/contests/990

### Keywords for Search

`vulnerability`

