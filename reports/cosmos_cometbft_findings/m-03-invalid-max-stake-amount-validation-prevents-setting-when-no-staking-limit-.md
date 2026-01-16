---
# Core Classification
protocol: Kinetiq_2025-02-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58619
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
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

[M-03] Invalid max stake amount validation prevents setting when no staking limit exists

### Overview


The `StakingManager` contract allows users to stake a certain amount of cryptocurrency. There are three parameters that control the amount of cryptocurrency that can be staked: `stakingLimit`, `minStakeAmount`, and `maxStakeAmount`. These parameters can be changed by certain accounts with a special role. However, there is a problem with the `setMaxStakeAmount()` function that prevents the `maxStakeAmount` from being set correctly when there is no limit on the total amount that can be staked. This is because the function does not account for the case where the `stakingLimit` is set to 0 (unlimited). To fix this issue, the `setMaxStakeAmount()` function should be modified to only perform the validation check if a limit is actually set. This will allow the `maxStakeAmount` to be set correctly even when there is no limit on the total staking amount. 

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `StakingManager` contract implements staking limits through three key parameters:
- `stakingLimit`: Maximum total stake allowed (0 = unlimited)
- `minStakeAmount`: Minimum stake per transaction
- `maxStakeAmount`: Maximum stake per transaction (0 = unlimited)

These parameters can be configured by accounts with the `MANAGER_ROLE` through dedicated setter functions. However, there is a logical error in the `setMaxStakeAmount()` function that prevents setting a valid max stake amount when there is no staking limit configured.

```solidity
        if (newMaxStakeAmount > 0) {
            require(newMaxStakeAmount > minStakeAmount, "Max stake must be greater than min");
            require(newMaxStakeAmount < stakingLimit, "Max stake must be less than limit");
        }
```

The issue occurs in the validation logic of `setMaxStakeAmount()`, where it unconditionally requires that any non-zero `newMaxStakeAmount` must be less than `stakingLimit`. This check fails to account for the case where `stakingLimit` is 0 (unlimited), making it impossible to set a max stake amount when no total limit exists. 

### Proof of Concept

1. Initially `stakingLimit = 0` (unlimited total staking)
2. Manager attempts to set `maxStakeAmount = 100 ether` to limit individual transactions
3. The call to `setMaxStakeAmount(100 ether)` reverts because:
   - `newMaxStakeAmount > 0` triggers the validation checks
   - `require(newMaxStakeAmount < stakingLimit)` fails as `100 ether < 0` is false

## Recommendations

Modify the `setMaxStakeAmount()` function to only perform the staking limit validation when a limit is actually set:

```solidity
function setMaxStakeAmount(uint256 newMaxStakeAmount) external onlyRole(MANAGER_ROLE) {
    if (newMaxStakeAmount > 0) {
        require(newMaxStakeAmount > minStakeAmount, "Max stake must be greater than min");
        if (stakingLimit > 0) {
            require(newMaxStakeAmount < stakingLimit, "Max stake must be less than limit");
        }
    }
    maxStakeAmount = newMaxStakeAmount;
    emit MaxStakeAmountUpdated(newMaxStakeAmount);
}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Kinetiq_2025-02-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

