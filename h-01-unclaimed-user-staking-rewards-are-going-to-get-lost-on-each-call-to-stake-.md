---
# Core Classification
protocol: Csx
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44005
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/CSX-Security-Review.md
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

[H-01] Unclaimed User Staking Rewards Are Going to Get Lost on Each Call to `stake()` Function in `StakedCSX` Contract

### Overview


The `stake()` function in `StakedCSX.sol` is causing users to lose their unclaimed rewards when they stake additional `CSX` tokens. This is because the function is incorrectly calling `_updateRewardRate()` for all three reward tokens, which only resets the reward rates for the caller. To fix this, the team recommends replacing the `_updateRewardRate()` calls with a single `_claimToCredit()` call, which both updates the reward rates and saves the rewards for later claiming. The team has already fixed this issue by changing the reward logic and removing the `_claimToCredit()` function.

### Original Finding Content

## Severity

High Risk

## Description

The current implementation of the `stake()` function in `StakedCSX.sol` calls `_updateRewardRate()` internally for all three reward tokens. This is incorrect as it will just reset the reward rates of the caller, leading to the loss of all of their unclaimed staking rewards.

## Impact

Users are going to lose all of their unclaimed rewards whenever they stake additional `CSX` tokens.

## Location of Affected Code

File: [StakedCSX.sol#L92-L94](https://github.com/csx-protocol/csx-contracts/blob/4a066ae2229756518bfa3da1455c2ac646523a88/contracts/CSX/StakedCSX.sol#L92-L94)

```solidity
/**
* @notice Stakes the user's CSX tokens
* @dev Mints sCSX & Sends the user's CSX to this contract.
* @param _amount The amount of tokens to be staked
*/
function stake(uint256 _amount) external nonReentrant {
  if (_amount == 0) {
    revert AmountMustBeGreaterThanZero();
  }
  _updateRewardRate(msg.sender, address(TOKEN_WETH));
  _updateRewardRate(msg.sender, address(TOKEN_USDC));
  _updateRewardRate(msg.sender, address(TOKEN_USDT));
  _mint(msg.sender, _amount);
  TOKEN_CSX.safeTransferFrom(msg.sender, address(this), _amount);
  emit Stake(msg.sender, _amount);
}
```

## Recommendation

Replace the `_updateRewardRate()` calls with a single `_claimToCredit()` call, which both updates the reward rates of the user and saves their rewards to the credit mapping for later claiming:

```diff
function stake(uint256 _amount) external nonReentrant {
  if (_amount == 0) {
    revert AmountMustBeGreaterThanZero();
  }
- _updateRewardRate(msg.sender, address(TOKEN_WETH));
- _updateRewardRate(msg.sender, address(TOKEN_USDC));
- _updateRewardRate(msg.sender, address(TOKEN_USDT));
+ _claimToCredit(msg.sender);
  _mint(msg.sender, _amount);
  TOKEN_CSX.safeTransferFrom(msg.sender, address(this), _amount);
  emit Stake(msg.sender, _amount);
}
```

## Team Response

Fixed by changing the reward logic and removing the `_claimToCredit()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Csx |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/CSX-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

