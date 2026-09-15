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
solodit_id: 37830
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-April.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

[H-02] Ignoring withdrawal limits during accounts merging

### Overview



This bug report discusses a problem with the `CollateralPool.merge` function, which is used to combine two collateral pools. The bug allows for funds to be withdrawn from the merged pool without following the withdrawal limits set for the original pool. This bug has a high impact and medium likelihood of occurring. The report recommends transferring all withdrawal limits from the original pool to the merged pool to prevent this issue.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The `CollateralPool.merge` merges collateral pool `child` into the collateral pool `parent` ignoring withdrawal limits of the `child` pool.

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
>>                  _updateCollateralShares(child, collateral, -amount);
                    _updateCollateralShares(parent, collateral, amount);
                }
            }
```

Funds can be withdrawn directly after `merge` since `child` pool withdrawal limits are not transferred to the `parent` pool.

## Recommendations

Consider transferring all withdrawal limits from the `child` pool to the `parent` pool.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

