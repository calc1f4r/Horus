---
# Core Classification
protocol: Nexus_2024-11-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44979
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
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

[C-02] Incorrect reward calculation due to decimal handling

### Overview


The DSRStrategy contract's `getRewards` function has a bug that causes reward calculations to be inflated by a factor of 1e18. This leads to incorrect share price calculations and gives an unfair advantage to early depositors. To fix this, the `getRewards` function should be modified to properly handle decimals by dividing the asset balance by 1e18.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

In the DSRStrategy contract's `getRewards` function, there is a decimal handling error when calculating asset balances and rewards. The function multiplies the token balance by the conversion rate without accounting for decimals, leading to severely inflated reward calculations.

```solidity
    function getRewards(address receiver,IStrategyManager.StrategyStruct memory _strategyBalance) public override view returns(uint256){
        uint256 balance_strategy = _strategyBalance.valueDeposited
            + _strategyBalance.rewardsEarned -_strategyBalance.valueWithdrawn;
        uint256 assetBalance = IERC20(TOKEN_ADDRESS).balanceOf(receiver)
            * sDAI(TOKEN_ADDRESS).convertToAssets(1e18);
        if (assetBalance>balance_strategy){
            return assetBalance - balance_strategy;
        }
        else{
            return 0;
        }
    }
```

The impact is reward amount is inflated by a factor of 1e18. It causes incorrect share price calculations in the deposit contracts. And new depositors receive fewer shares than they should due to artificially high share prices. Early depositors gain an unfair advantage at the expense of later depositors.

## Recommendations

Modify the `getRewards` function to properly handle decimals:

````diff
- uint256 assetBalance = IERC20(TOKEN_ADDRESS).balanceOf(receiver)*sDAI(TOKEN_ADDRESS).convertToAssets(1e18);
+ uint256 assetBalance = IERC20(TOKEN_ADDRESS).balanceOf(receiver)*sDAI(TOKEN_ADDRESS).convertToAssets(1e18) / 1e18;

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nexus_2024-11-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

