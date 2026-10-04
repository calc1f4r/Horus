---
# Core Classification
protocol: Peapods
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52754
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/749
source_link: none
github_link: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/74

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
finders_count: 1
finders:
  - X77
---

## Vulnerability Title

M-2: Liquidations will revert incorrectly due to an out-of-sync leftover collateral value

### Overview


The bug report discusses an issue with liquidations on the Peapods Finance platform. The problem is caused by a miscalculation in the code, resulting in incorrect values for leftover collateral. This can lead to incorrect liquidations and potentially cause financial losses for the platform. The report suggests updating the code to fix this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/74 

## Found by 
X77

### Summary

Liquidations will revert incorrectly due to an out-of-sync value

### Root Cause

Upon liquidations, we have this code:
```solidity
_leftoverCollateral = (_userCollateralBalance.toInt256() - _optimisticCollateralForLiquidator.toInt256());

_collateralForLiquidator = _leftoverCollateral <= 0 ? _userCollateralBalance : (_liquidationAmountInCollateralUnits * (LIQ_PRECISION + dirtyLiquidationFee)) / LIQ_PRECISION;
```
We compute an optimistic collateral for the liquidator which is based on `cleanLiquidationFee`. If the leftover collateral is not below 0, we recompute the collateral for liquidator based on the `dirtyLiquidationFee` which is a value lower than the clean fee (if we take a look at [Fraxlend](https://etherscan.io/address/0x78bb3aec3d855431bd9289fd98da13f9ebb7ef15#code), it is 9000 vs 10000 for the clean fee).

Then, we have this code:
```solidity
if (_leftoverCollateral <= 0) {
                ...
} else if (_leftoverCollateral < minCollateralRequiredOnDirtyLiquidation.toInt256()) {
       revert BadDirtyLiquidation();
}
```
If the leftover collateral is <=, we end up in the first block where we compute shares to adjust. If it is above 0 however, we will revert if we are under `minCollateralRequiredOnDirtyLiquidation`. The issue is that the leftover collateral is still based on the optimistic calculation which results in a much lower leftover collateral, resulting in reverts when the actual leftover collateral is not even close to `minCollateralRequiredOnDirtyLiquidation`.

### Internal Pre-conditions

_No response_

### External Pre-conditions

_No response_

### Attack Path

1. Let's imagine the following state:
- userCollateralBalance = 2.3e18
- dirtyLiquidationFee = 9_000 (based on Fraxlend)
- cleanLiquidationFee = 10_000 (based on Fraxlend)
- `_liquidationAmountInCollateralUnits` is equal to 2e18 based on the shares to liquidate provided by the user
- `minCollateralRequiredOnDirtyLiquidation` is 1.1e17
2. `_optimisticCollateralForLiquidator` will equal `2e18 * (1e5 + 1e4) / 1e5 = 2.2e18`
3. `_leftoverCollateral` equals `2.3e18 - 2.2e18 = 1e17`
4. As it is above 0, we recompute the collateral for liquidator which will equal `2e18 * (1e5 + 9e3) / 1e5 = 2.18e18`
5. As the leftover collateral is 1e17 and the minimum required collateral is 1.1e17, we will revert
6. In reality, the actual leftover collateral is `2.3e18 - 2.18e18 = 1.2e17` as the collateral we will take out from the user is 2.18e18, not 2.2e18

### Impact

Liquidations will revert incorrectly which is an extremely time-sensitive operation, this can lead to bad debt for the protocol

### PoC

_No response_

### Mitigation

Update the leftover collateral based on the new collateral for the liquidator

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Peapods |
| Report Date | N/A |
| Finders | X77 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/74
- **Contest**: https://app.sherlock.xyz/audits/contests/749

### Keywords for Search

`vulnerability`

