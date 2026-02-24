---
# Core Classification
protocol: Yeet Cup
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44198
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Yeet-Cup-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[C-01] Direct Loss of Rewards on Re-Staking

### Overview


The `reStake()` method in the `DiscreteStakingRewards` contract is not functioning correctly. When a user tries to re-stake their earned rewards, the rewards are instead being staked on behalf of the contract itself, resulting in the loss of the rewards. This also means that the re-staked rewards cannot be redeemed. The affected code is located in the `Stake.sol` file. The recommendation is to directly increase the user's staked balance instead of calling the `stake()` method. The team has responded that they have fixed the issue as suggested.

### Original Finding Content

## Severity

Critical Risk

## Description

The `reStake()` method of the `DiscreteStakingRewards` contract intends to add a user's (`msg.sender`) earned rewards to their staked balance instead of claiming those rewards. This is done by clearing the user's earned rewards and forwarding them to the contract's `stake()` method.  
However, the `stake()` method is called _externally_ and therefore the `msg.sender` will be the contract itself (`address(this)`) during the stake call.

Consequently, the user's earned rewards are re-staked on behalf of the contract instead of the user and are therefore lost. Furthermore, the re-staked rewards become stuck, since there is no way for the contract to redeem those "self-staked" amounts.

## Location of Affected Code

File: [src/Stake.sol#L163](https://github.com/0xKingKoala/contracts/blob/f43ad283290293e18e5d9ab0c9d56e29bffa3eb3/src/Stake.sol#L163)

```solidity
/// @notice The function used to re-stake the rewards without claiming them, bypassing the vesting period
/// @dev The rewards are staked again
function reStake() external {
    _updateRewards(msg.sender);
    uint reward = earned[msg.sender];
    require(reward > 0, "No rewards to claim");

    earned[msg.sender] = 0;
    this.stake(reward); // @audit msg.sender will be address(this) in stake call
}
```

## Recommendation

Directly increase the user's (`msg.sender`) staked balance:

```diff
function reStake() external {
    _updateRewards(msg.sender);
    uint reward = earned[msg.sender];
    require(reward > 0, "No rewards to claim");

    earned[msg.sender] = 0;

+   balanceOf[msg.sender] += reward;
+   totalSupply += reward;
-   this.stake(reward);
}
```

## Team Response

Fixed as suggested

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Yeet Cup |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Yeet-Cup-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

