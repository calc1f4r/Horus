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
solodit_id: 44202
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Yeet-Cup-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-01] Missing Vesting Period Verification in `unstake()` Method Puts Users at Risk

### Overview


The bug report describes a problem with the `DiscreteStakingRewards` contract where users are at risk of losing their stake when using the `unstake()` method. This method is intended to only be used after the vesting period has ended, but it is currently equivalent to the `rageQuit()` method which allows users to unstake before the vesting period has ended. The affected code is located in the `Stake.sol` file and the recommendation is to add a vesting period check to the `unstake()` method. The team has responded that they have fixed the issue as suggested.

### Original Finding Content

## Severity

Medium Risk

## Description

The `DiscreteStakingRewards` contract has a `rageQuit()` method which allows users to unstake before the vesting period has ended. Thereby, the user is at a (partial) loss which is intended and expected on a "rage quit".  
However, the `unstake()` method, which can be reasonably assumed to only allow unstaking once the vesting period has ended, is equivalent to the `rageQuit()` method and neglects to check the vesting period.

Consequently, users are at risk of having their stake (partially) burnt when calling `unstake()` which is not expected and therefore cannot be considered a careless user error.

```solidity
/// @notice The function used to unstake tokens
/// @param index The index of the vesting to unstake
function unstake(uint256 index) external {
    _unstake(index);
}

/// @notice The function used to rage quit
/// @notice Rage quit is used to unstake before the vesting period ends, will be called in the dApp
/// @param index The index of the vesting to unstake
function rageQuit(uint256 index) external {
    _unstake(index);
}
```

## Location of Affected Code

File: [src/Stake.sol#L101](https://github.com/0xKingKoala/contracts/blob/f43ad283290293e18e5d9ab0c9d56e29bffa3eb3/src/Stake.sol#L101)

```solidity
/// @notice The function used to unstake tokens
/// @param index The index of the vesting to unstake
function unstake(uint256 index) external {
    _unstake(index);
}
```

## Recommendation

Consider adding a vesting period check:

```diff
function unstake(uint256 index) external {
+   require(block.timestamp >= vestings[msg.sender][index].end, "Vesting period has not ended");
    _unstake(index);
}
```

## Team Response

Fixed as suggested

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

