---
# Core Classification
protocol: Guanciale Stake
chain: everychain
category: economic
vulnerability_type: flash_loan

# Attack Vector Details
attack_type: flash_loan
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45551
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Guanciale-Stake-Security-Review.md
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
  - flash_loan
  - vote

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[H-03] Users Can Use `Flashloan` to Increase Voting Power of Expired Positions and Execute Proposal for Their Benefits

### Overview


This bug report discusses a high-risk issue in the GUAN staking contracts. The issue involves a potential vulnerability in the `increaseAndStake()` function, which allows users to increase their stake without updating the lock duration. This could be exploited by a user who obtains a large amount of GUAN tokens through a flashloan and uses them to increase their stake and gain a significant amount of voting power. This could potentially allow them to execute a proposal and vote for it in one transaction, even if their lock duration has expired. The team has acknowledged this issue and recommends adding additional checks to prevent this attack. 

### Original Finding Content

## Severity

High Risk

## Description

If we assume the Medium-01 from the report is fixed in the `increaseAndStake()` function which allows users to add the amount to their stake without updating the lock duration then the below scenario might be executable:

- Assume Alice's `lockUntil` reached the current `block.timestamp`.

- Alice got a huge flashloan of GUAN token (can get another token as flashloan and then swap it to GUAN) and called the `increaseAndStake()` function with the flashloan amount.

- If we assume the Medium-01 issue is fixed then the transaction will be executed without reverting since Alice increased the stake amount only.

- The `veGUAN` core logic allows the stakes to have voting power depending on their stake amount even if the lock duration expired, this is clearly shown in the function below:

```solidity
function _calculateVotingPower(
  UD60x18 votingPowerCurveAFactorX18,
  UD60x18 remainingLockDurationX18,
  UD60x18 positionStakeX18
)
  internal
  pure
  returns (uint256 scalingFactor, uint256 votingPower)
{
  // calculate the lock multiplier as explained in the function's natspec
  UD60x18 scalingFactorX18 = votingPowerCurveAFactorX18.mul(remainingLockDurationX18).add(UNIT); // @audit 1e18 get added even if the calc = 0

  // return the scaling factor and voting power
  scalingFactor = scalingFactorX18.intoUint256();
  votingPower = positionStakeX18.mul(scalingFactorX18).intoUint256();
}
```

- This way Alice can have huge voting power due to her flashloan amount and she can execute a proposal and vote for it in one transaction and then unstake her GUAN token(the tx won't revert since `block.timestamp == lockUntil`):

```solidity
function unstake(uint256 tokenId, uint256 amount) external onlyTokenOwner(tokenId) {
  // load veGUAN storage slot
  VeGuanStorage storage $ = _getVeGuanStorage();

  // load the lock data storage pointer
  LockedPositionData storage lockedPosition = $.lockedPositions[tokenId];

  // revert if the position is still locked
  if (block.timestamp < lockedPosition.lockedUntil) {
      revert PositionIsLocked();
  }

  // deduct the unstake amount from the locked position's state, if there isn't enough stake in the position the
  // call will revert with an underflow
  lockedPosition.stake -= amount;

  // transfer the lp tokens to the `msg.sender`
  IERC20($.lpToken).safeTransfer(msg.sender, amount);

  // cache the veGUAN's voting power
  (, uint256 votingPower) = getVotingPowerOf(tokenId);

  // emit an event
  emit LogUnstake(msg.sender, tokenId, lockedPosition.stake, votingPower);
}
```

This issue could potentially occur based on the current small codebase. However, the GUAN documentation states that proposals are reviewed by the council, which may prevent this issue from being executed.

## Location of Affected Code

File: [src/veGUAN.sol#L283](https://github.com/GuancialeAI/guan-staking-contracts/blob/f1f9d252d30edd7e7f04cc536dadae90a9daa509/src/veGUAN.sol#L283)

```solidity
/// @notice Increases the stake value and/or lock duration of a veGUAN position.
/// @param tokenId The NFT identifier.
/// @param stakeIncrease The amount of LP tokens to be staked into the position.
/// @param lockIncrease The amount of time to add to the position's lock duration.
function increaseStakeAndLock(
  uint256 tokenId,
  uint256 stakeIncrease,
  uint256 lockIncrease
)
  external
  onlyTokenOwner(tokenId)
{
  // load veGUAN storage slot
  VeGuanStorage storage $ = _getVeGuanStorage();

  // load the lock data storage pointer
  LockedPositionData storage lockedPosition = $.lockedPositions[tokenId];

  // cache the new unlock timestamp value
  uint256 newUnlockTimestamp = lockedPosition.lockedUntil + lockIncrease;

  // compute the new lock duration based on the provided lockIncrease
  uint256 newLockDuration = newUnlockTimestamp - block.timestamp;

  // validate that the new lock duration is under the min and max requirements
  if (newLockDuration > $.maxLockDuration || newLockDuration < $.minLockDuration) {
      revert InvalidLockDuration();
  }

  uint256 newStakeValue = lockedPosition.stake + stakeIncrease;

  // updates the locked position data
  lockedPosition.stake = newStakeValue;
  lockedPosition.lockedUntil = newUnlockTimestamp;
  // finally, transfer the lp tokens from the `msg.sender`
  IERC20($.lpToken).safeTransferFrom(msg.sender, address(this), stakeIncrease);

  // cache the veGUAN's voting power
  (, uint256 votingPower) = getVotingPowerOf(tokenId);

  // emit an event
  emit LogIncreaseStakeAndLock(msg.sender, tokenId, newStakeValue, newUnlockTimestamp, votingPower);
}
```

File: [src/veGUAN.sol#L327](https://github.com/GuancialeAI/guan-staking-contracts/blob/f1f9d252d30edd7e7f04cc536dadae90a9daa509/src/veGUAN.sol#L327)

```solidity
/// @notice Unstakes a given amount of LP tokens from an unlocked veGUAN position.
/// @param tokenId The NFT identifier.
/// @param amount The amount of LP tokens to unstake from the veGUAN position.
function unstake(uint256 tokenId, uint256 amount) external onlyTokenOwner(tokenId) {
  // load veGUAN storage slot
  VeGuanStorage storage $ = _getVeGuanStorage();

  // load the lock data storage pointer
  LockedPositionData storage lockedPosition = $.lockedPositions[tokenId];

  // revert if the position is still locked
  if (block.timestamp < lockedPosition.lockedUntil) {
      revert PositionIsLocked();
  } // @audit

  // deduct the unstake amount from the locked position's state, if there isn't enough stake in the position the
  // call will revert with an underflow
  lockedPosition.stake -= amount;

  // transfer the lp tokens to the `msg.sender`
  IERC20($.lpToken).safeTransfer(msg.sender, amount);

  // cache the veGUAN's voting power
  (, uint256 votingPower) = getVotingPowerOf(tokenId);

  // emit an event
  emit LogUnstake(msg.sender, tokenId, lockedPosition.stake, votingPower);
}
```

## Impact

A malicious user can execute a flashloan attack to gain huge vote power to execute a proposal.

## Recommendation

If the check changed from the `unstake()` function then the attack can be prevented:

```solidity
if (block.timestamp <= lockedPosition.lockedUntil) {
```

Another check can be added in `increaseAndStake()` which prevents increasing stake amount for expired positions.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Guanciale Stake |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Guanciale-Stake-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Flash Loan, Vote`

