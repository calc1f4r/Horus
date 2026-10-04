---
# Core Classification
protocol: Ajna
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6303
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/32
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/122

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - validation
  - fund_lock

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - berndartmueller
  - Blockian
---

## Vulnerability Title

M-6: Claiming rewards from a future not yet existing epoch prevents claiming rewards for those epochs later on

### Overview


This bug report is about an issue in the smart contract code of the project "2023-01-ajna-judging". The issue is that if a user claims rewards for a future epoch, all epochs are marked as claimed up until that future epoch. This prevents the user from claiming rewards for those epochs later, leading to a loss of rewards.

The code snippet from the `RewardsManager.claimRewards` function shows that the current implementation does not prevent a user from accidentally claiming rewards for a future epoch. This would iterate through all epochs up until the future epoch and mark them all as claimed.

The impact of this is that if a user accidentally claims rewards for a future epoch, the rewards are lost and unclaimable.

The recommendation is to consider adding a check to the `RewardsManager.claimRewards` function to prevent claiming rewards for future epochs. This bug was found by berndartmueller and Blockian, using manual review. It has been marked as a duplicate of issue #151.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/122 

## Found by 
berndartmueller, Blockian

## Summary

If a user claims rewards for a future epoch, all epochs are marked as claimed up until that future epoch. This prevents the user from claiming rewards for those epochs later, leading to a loss of rewards.

## Vulnerability Detail

Already claimed rewards are tracked in the `isEpochClaimed` mapping and checked in the `RewardsManager.claimRewards` function to prevent claiming rewards multiple times. However, the current implementation does not prevent a user from accidentally claiming rewards for a future epoch. This would iterate through all epochs up until the future epoch and mark them all as claimed. This prevents the user from claiming rewards for those epochs later on, leading to a loss of rewards.

## Impact

If a user accidentally claims rewards for a future epoch, the rewards are lost and unclaimable.

## Code Snippet

[contracts/src/RewardsManager.sol#L112](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/RewardsManager.sol#L112)

```solidity
106: function claimRewards(
107:     uint256 tokenId_,
108:     uint256 epochToClaim_
109: ) external override {
110:     if (msg.sender != stakes[tokenId_].owner) revert NotOwnerOfDeposit();
111:
112:     if (isEpochClaimed[tokenId_][epochToClaim_]) revert AlreadyClaimed();
113:
114:     _claimRewards(tokenId_, epochToClaim_);
115: }
```

[contracts/src/RewardsManager.sol#L298](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/RewardsManager.sol#L298)

```solidity
272: function _calculateAndClaimRewards(
273:     uint256 tokenId_,
274:     uint256 epochToClaim_
275: ) internal returns (uint256 rewards_) {
276:
277:     address ajnaPool      = stakes[tokenId_].ajnaPool;
278:     uint256 lastBurnEpoch = stakes[tokenId_].lastInteractionBurnEpoch;
279:     uint256 stakingEpoch  = stakes[tokenId_].stakingEpoch;
280:
281:     uint256[] memory positionIndexes = positionManager.getPositionIndexes(tokenId_);
282:
283:     // iterate through all burn periods to calculate and claim rewards
284:     for (uint256 epoch = lastBurnEpoch; epoch < epochToClaim_; ) {
285:
286:         uint256 nextEpochRewards = _calculateNextEpochRewards(
287:             tokenId_,
288:             epoch,
289:             stakingEpoch,
290:             ajnaPool,
291:             positionIndexes
292:         );
293:
294:         uint256 nextEpoch = epoch + 1;
295:
296:         // update epoch token claim trackers
297:         rewardsClaimed[nextEpoch]           += nextEpochRewards;
298:         isEpochClaimed[tokenId_][nextEpoch] = true;
299:
300:         rewards_ += nextEpochRewards;
301:
302:         unchecked { ++epoch; }
303:     }
304: }
```

## Tool used

Manual Review

## Recommendation

Consider adding a check to the `RewardsManager.claimRewards` function to prevent claiming rewards for future epochs.

## Discussion

**grandizzy**

Has #151 as dupe

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna |
| Report Date | N/A |
| Finders | berndartmueller, Blockian |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/122
- **Contest**: https://app.sherlock.xyz/audits/contests/32

### Keywords for Search

`Validation, Fund Lock`

