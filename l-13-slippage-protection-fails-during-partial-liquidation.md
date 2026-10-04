---
# Core Classification
protocol: Tangent_2025-10-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63881
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-13] Slippage protection fails during partial liquidation

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The liquidation function uses maxUSGToBurn and minUSGOut parameters to protect the liquidator from excessive slippage. However, these protections can become ineffective if another partial liquidation occurs before the caller’s transaction executes. Specifically, the function adjusts the liquidation amount as follows:
```solidity
if (collatAmountToLiquidate >= liquidateInput._collateralBalance) {
    collatAmountToLiquidate = liquidateInput._collateralBalance;
    USGToRepay = liquidateInput.userDebt;
}

```
If the user’s collateral has already been reduced by a previous liquidation, collatAmountToLiquidate is capped to a smaller amount, while the caller’s maxUSGToBurn remains based on stale state (the pre-liquidation ratio).

As a result:
- maxUSGToBurn may no longer accurately bound the actual repayment amount per unit of collateral, failing to protect the liquidator from overpaying.

- minUSGOut may fail since less collateral is liquidated than expected, leading to smaller output amounts.

Implement slippage protection relative to collateral units, not just total USG amounts.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tangent_2025-10-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

