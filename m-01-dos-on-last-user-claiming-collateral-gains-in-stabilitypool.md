---
# Core Classification
protocol: Roots_2025-02-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55117
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
github_link: none

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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] DoS on last user claiming collateral gains in `StabilityPool`

### Overview


This bug report discusses a problem with the `StabilityPool` contract that can lead to incorrect calculations of collateral gains for depositors. The issue is caused by the value of `lastCollateralError_Offset` not being reset when a sunset collateral is overwritten, resulting in the new collateral inheriting the value of the previous one. This can cause the value of `collateralGainPerUnitStaked` to be higher than it should be, potentially leading to insufficient collateral in the pool to cover the overvalued gains. To fix this, it is recommended to reset the `lastCollateralError_Offset` value in the `_overwriteCollateral` function.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

When a sunset collateral is overwritten in the `StabilityPool` contract, the value of `lastCollateralError_Offset` is not reset, which means that the new collateral will inherit the value of the previous one. This can provoke the value of `collateralGainPerUnitStaked` to be higher than it should be:

```solidity
    function _computeRewardsPerUnitStaked(
(...)
        uint256 collateralNumerator = (_collToAdd * DECIMAL_PRECISION) + lastCollateralError_Offset[idx];
(...)
        collateralGainPerUnitStaked = collateralNumerator / _totalDebtTokenDeposits;
```

This value is stored in the `epochToScaleToSums` mapping and used later to calculate the collateral gains for depositors.

As a result, the last user to claim their collateral gains might not be able to do so, as there might not be enough collateral in the pool to cover the overvalued gains.

## Recommendations

Reset the `lastCollateralError_Offset` value for the index reassigned to the new collateral in the `_overwriteCollateral` function.

```diff
+       lastCollateralError_Offset[idx] = 0;
        indexByCollateral[_newCollateral] = idx + 1;
        emit CollateralOverwritten(collateralTokens[idx], _newCollateral);
        collateralTokens[idx] = _newCollateral;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Roots_2025-02-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

