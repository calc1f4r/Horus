---
# Core Classification
protocol: ReyaNetwork-April
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37833
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-April.md
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

[M-03] Bypassing collateral cap check

### Overview


The report is about a bug in the CollateralPool.merge function where it merges two collateral pools, parent and child, without checking the cap limit in the updateCollateralShares function. This can lead to exceeding the cap limit if the parent pool has a balance before the merge. The severity of this bug is high and the likelihood of it occurring is low. The recommendation is to add a check for the collateral cap in the merge function.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The `CollateralPool.merge` merges collateral pool `child` into collateral pool `parent` bypassing cap check in `updateCollateralShares` function since it directly invokes `_updateCollateralShares` function.

```solidity
    function merge(Data storage parent, Data storage child) internal {
<...>
            // transfer funds from the child collateral pool to the parent
            {
                address[] storage collaterals = GlobalCollateralConfiguration.load().collaterals;

                for (uint256 i = 0; i < collaterals.length; i++) {
                    address collateral = collaterals[i];
                    int256 amount = child.collateralShares[collateral].toInt();

                    if (amount == 0) {
                        continue;
                    }

                    CollateralConfiguration.exists(parentId, collateral);
                    _updateCollateralShares(child, collateral, -amount);
>>                  _updateCollateralShares(parent, collateral, amount);
                }
            }
```

In case the `parent` pool balance before the merge is not empty the `collateralConfig.baseConfig.cap` can be exceeded.

## Recommendations

Consider checking the collateral cap in the `merge` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | ReyaNetwork-April |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-April.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

