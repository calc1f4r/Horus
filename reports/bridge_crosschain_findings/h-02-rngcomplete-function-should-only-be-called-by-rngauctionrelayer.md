---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25960
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-pooltogether
source_link: https://code4rena.com/reports/2023-08-pooltogether
github_link: https://github.com/code-423n4/2023-08-pooltogether-findings/issues/82

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

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 16
finders:
  - 0xStalin
  - josephdara
  - D\_Auditor
  - 0xbepresent
  - bin2chen
---

## Vulnerability Title

[H-02] `rngComplete` function should only be called by `rngAuctionRelayer`

### Overview


This bug report is about an issue that occurs in the `rngComplete` function in the PoolTogether smart contract. The function is supposed to be called by the relayer to complete the Rng relay auction and send auction rewards to the recipient, but because the function doesn't have any access control it can be called by anyone. This means that an attacker can call the function before the relayer and give a different `_rewardRecipient` address, thus collecting all the rewards and the true auction reward recipient will not get any.

The recommended mitigation steps for this issue is to add a check in the `rngComplete` function to make sure that only the relayer can call it. This can be done by adding a check on the `msg.sender` and reverting if it is not the relayer.

This bug has been assessed as an Access Control issue.

### Original Finding Content


The `rngComplete` function is supposed to be called by the relayer to complete the Rng relay auction and send auction rewards to the recipient, but because the function doesn't have any access control it can be called by anyone, an attacker can call the function before the relayer and give a different `_rewardRecipient` and thus he can collect all the rewards and the true auction reward recipient will not get any.

### Proof of Concept

The issue occurs in the `rngComplete` function below:

```solidity
function rngComplete(
    uint256 _randomNumber,
    uint256 _rngCompletedAt,
    address _rewardRecipient, // @audit can set any address
    uint32 _sequenceId,
    AuctionResult calldata _rngAuctionResult
) external returns (bytes32) {
    // @audit should only be callable by rngAuctionRelayer
    if (_sequenceHasCompleted(_sequenceId)) revert SequenceAlreadyCompleted();
    uint64 _auctionElapsedSeconds = uint64(
        block.timestamp < _rngCompletedAt ? 0 : block.timestamp - _rngCompletedAt
    );
    if (_auctionElapsedSeconds > (_auctionDurationSeconds - 1)) revert AuctionExpired();
    // Calculate the reward fraction and set the draw auction results
    UD2x18 rewardFraction = _fractionalReward(_auctionElapsedSeconds);
    _auctionResults.rewardFraction = rewardFraction;
    _auctionResults.recipient = _rewardRecipient;
    _lastSequenceId = _sequenceId;

    AuctionResult[] memory auctionResults = new AuctionResult[](2);
    auctionResults[0] = _rngAuctionResult;
    auctionResults[1] = AuctionResult({
        rewardFraction: rewardFraction,
        recipient: _rewardRecipient
    });

    uint32 drawId = prizePool.closeDraw(_randomNumber);

    uint256 futureReserve = prizePool.reserve() + prizePool.reserveForOpenDraw();
    uint256[] memory _rewards = RewardLib.rewards(auctionResults, futureReserve);

    emit RngSequenceCompleted(
        _sequenceId,
        drawId,
        _rewardRecipient,
        _auctionElapsedSeconds,
        rewardFraction
    );

    for (uint8 i = 0; i < _rewards.length; i++) {
        uint104 _reward = uint104(_rewards[i]); 
        if (_reward > 0) {
            prizePool.withdrawReserve(auctionResults[i].recipient, _reward);
            emit AuctionRewardDistributed(_sequenceId, auctionResults[i].recipient, i, _reward);
        }
    }

    return bytes32(uint(drawId));
}
```

As we can see the function does not have any access control (modifier or check on the msg.sender), so any user can call it and you can also notice that the `_rewardRecipient` (the address that receives the rewards) is given as argument to the function and there is no check to verify that it is the correct auction reward receiver.

Hence an attacker can call the function before the relayer does, he can thus complete the auction and give another address for `_rewardRecipient` which will receive all the rewards.

The result is in the end that the true auction reward recipient will get his reward stolen by other users.

### Recommended Mitigation Steps

Add a check in the `rngComplete` function to make sure that only the relayer can call it, the function can be modified as follows:

```solidity
function rngComplete(
    uint256 _randomNumber,
    uint256 _rngCompletedAt,
    address _rewardRecipient, 
    uint32 _sequenceId,
    AuctionResult calldata _rngAuctionResult
) external returns (bytes32) {
    // @audit only called by rngAuctionRelayer
    if (msg.sender != rngAuctionRelayer) revert NotRelayer();
    ...
}
```

### Assessed type

Access Control

**[asselstine (PoolTogether) confirmed](https://github.com/code-423n4/2023-08-pooltogether-findings/issues/82#issuecomment-1673781082)**



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | 0xStalin, josephdara, D\_Auditor, 0xbepresent, bin2chen, 1, T1MOH, shirochan, Aymen0909, Jorgect, dirk\_y, 2, ptsanev, trachev, rvierdiiev, Arz |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-pooltogether
- **GitHub**: https://github.com/code-423n4/2023-08-pooltogether-findings/issues/82
- **Contest**: https://code4rena.com/reports/2023-08-pooltogether

### Keywords for Search

`vulnerability`

