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
solodit_id: 44200
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

[H-01] Re-staking Mechanism Can Lead to Contract Insolvency

### Overview


This bug report is about a high-risk issue in the `DiscreteStakingRewards` contract. The contract pays staking rewards in `BERA` tokens, but the locked staking tokens are `YEET`. The problem is that the re-staking mechanism allows users to increase their staked `YEET` with `BERA` instead of claiming it as a reward. This can lead to an incorrect `totalSupply` of `YEET` tokens in the contract, potentially causing insolvency. Additionally, treating `BERA` and `YEET` as equal during re-staking can create an economic imbalance. The affected code is located in the `Stake.sol` file. The recommended solution is to buy `YEET` tokens with the `BERA` rewards before re-staking to prevent misaccounting and resolve the economic imbalance. The team has responded by temporarily removing the re-staking functionality and planning to re-design it.

### Original Finding Content

## Severity

High Risk

## Description

In the `DiscreteStakingRewards` contract, the staking rewards are paid in `BERA` (native has a token on [Berachain](https://docs.berachain.com/learn) while the locked staking tokens are `YEET`.  
However, the current re-staking mechanism allows to increase the staked `YEET` with `BERA` instead of claiming it as a reward.

As a consequence of re-staking, the `totalSupply` of `YEET` tokens in the contract will be higher than the _actual supply_ which can potentially lead to insolvency of the contract in terms of `YEET` tokens.  
Furthermore, treating `BERA` equivalently to `YEET` on re-staking comes with an economic disbalance since their respective prices are likely not equal at all times.

## Location of Affected Code

File: [src/Stake.sol#L157](https://github.com/0xKingKoala/contracts/blob/f43ad283290293e18e5d9ab0c9d56e29bffa3eb3/src/Stake.sol#L157)

```solidity
/// @notice The function used to re-stake the rewards without claiming them, bypassing the vesting period
/// @dev The rewards are staked again
function reStake() external {
    _updateRewards(msg.sender);
    uint reward = earned[msg.sender];
    require(reward > 0, "No rewards to claim");

    earned[msg.sender] = 0;
    this.stake(reward);
}
```

## Recommendation

`YEET` tokens should be bought with the `BERA` rewards before re-staking to prevent misaccounting of `BERA` as `YEET` and resolve the economic disbalance.

## Team Response

Fixed by temporarily removing the re-staking functionality that will be re-designed

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

