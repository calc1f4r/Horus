---
# Core Classification
protocol: Surge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55145
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Surge-Security-Review.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.50
financial_impact: medium

# Scoring
quality_score: 2.5
rarity_score: 1

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[M-02] Staking and Reward Token Overlap Can Risk User Stakes

### Overview


This bug report is about a medium risk vulnerability in the `StakingVault.acceptPositionManagerRewards()` function. This function can be called by anyone and uses `transferFrom` with an arbitrary `from` value. This means that an attacker can use this function to transfer reward tokens from anyone who has given allowance to the `StakingVault`. This can be problematic if both the staking and reward tokens are the same, as an attacker can front-run a user's stake call and use their approved amount as a reward. The affected code can be found in the `StakingVault.sol` file. The impact of this bug is that a user could lose their tokens when trying to stake. The recommendation is to always use `transferFrom` with `msg.sender` as the `from` argument. The team has responded that the issue has been fixed.

### Original Finding Content

## Severity

Medium Risk

## Description

The `StakingVault.acceptPositionManagerRewards()` can be called by anybody and uses transferFrom with an arbitrary `from` value. This means that an attacker can use this function and transfer reward tokens from anybody that has given allowance to the `StakingVault`.

This is problematic since if the staking and the reward token are both $VOLT then users will first approve the `StakingVault` and then they will call `stake()`.

An attacker can front-run the stake call of the user and use this approved amount as a reward via the `acceptPositionManagerRewards()`.

## Location of Affected Code

File: [StakingVault.sol]()

```solidity
function acceptPositionManagerRewards(address manager, uint256 allowedAmount) external returns (uint256 amount) {
    endCycleIfNeeded();

    uint256 amountPerPool = allowedAmount / REWARD_POOL_COUNT;
    require(amountPerPool > 0, "Invalid amount"); // FIXME: either revert, or just ignore and do nothing

    // This can be different from original `amount` due to division rounding
    amount = amountPerPool * REWARD_POOL_COUNT;

@>  bool success = rewardsToken.transferFrom(manager, address(this), amount);
    require(success, "Transfer failed");

    for (uint256 i; i < REWARD_POOL_COUNT; i++) {
        uint256 poolId = _rewardPools[i].id;
        uint256 cycleId = _rewardPools[i].currentCycleId;

        _rewardPoolRewards[poolId][cycleId] += amountPerPool;
    }
}
```

## Impact

A user could lose their tokens when they attempt to stake.

## Recommendation

Always use `transferFrom` with a `msg.sender` as the `from` argument.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2.5/5 |
| Rarity Score | 1/5 |
| Audit Firm | Shieldify |
| Protocol | Surge |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Surge-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

