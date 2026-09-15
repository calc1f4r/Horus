---
# Core Classification
protocol: Tokemak
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27080
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/101
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/379

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
finders_count: 24
finders:
  - duc
  - bulej93
  - Kalyan-Singh
  - p0wd3r
  - 0xvj
---

## Vulnerability Title

H-4: When `queueNewRewards` is called, caller could transfer tokens more than it should be

### Overview


A bug has been reported in the function `queueNewRewards` of the project '2023-06-tokemak-judging'. This function is used to queue rewards for distribution to stakers. When this function tried to pull funds from sender via `safeTransferFrom`, it used `newRewards` amount, which already added  by `startingQueuedRewards`. This could make the caller transfer tokens more than it should be. 

This bug was found by 0xVolodya, 0xbepresent, 0xvj, 1nc0gn170, Angry\_Mustache\_Man, Aymen0909, BPZ, Kalyan-Singh, berndartmueller, bin2chen, bitsurfer, bulej93, caelumimperium, chaduke, duc, l3r0ux, lemonmon, lil.eth, p0wd3r, pengun, saidam017, shaka, wangxx2026, and xiaoming90. The bug was identified through manual review. 

The bug can have two possible impacts. Firstly, if the previously `queuedRewards` is not 0, and the caller doesn't have enough funds or approval, the call will revert due to this logic error. Secondly, if the previously `queuedRewards` is not 0, and the caller has enough funds and approval, the caller funds will be pulled more than it should (reward param + `queuedRewards`). 

The recommended solution is to update the transfer to use `startingNewRewards` instead of `newRewards`. This would ensure that the caller only transfers the correct amount of tokens.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/379 

## Found by 
0xVolodya, 0xbepresent, 0xvj, 1nc0gn170, Angry\_Mustache\_Man, Aymen0909, BPZ, Kalyan-Singh, berndartmueller, bin2chen, bitsurfer, bulej93, caelumimperium, chaduke, duc, l3r0ux, lemonmon, lil.eth, p0wd3r, pengun, saidam017, shaka, wangxx2026, xiaoming90

`queueNewRewards` is used for Queues the specified amount of new rewards for distribution to stakers. However, it used wrong calculated value when pulling token funds from the caller, could make caller transfer tokens more that it should be.

## Vulnerability Detail

Inside `queueNewRewards`, irrespective of whether we're near the start or the end of a reward period, if the accrued rewards are too large relative to the new rewards (`queuedRatio` is greater than `newRewardRatio`), the new rewards will be added to the queue (`queuedRewards`) rather than being immediately distributed.

https://github.com/sherlock-audit/2023-06-tokemak/blob/main/v2-core-audit-2023-07-14/src/rewarders/AbstractRewarder.sol#L235-L261

```solidity
    function queueNewRewards(uint256 newRewards) external onlyWhitelisted {
        uint256 startingQueuedRewards = queuedRewards;
        uint256 startingNewRewards = newRewards;

        newRewards += startingQueuedRewards;

        if (block.number >= periodInBlockFinish) {
            notifyRewardAmount(newRewards);
            queuedRewards = 0;
        } else {
            uint256 elapsedBlock = block.number - (periodInBlockFinish - durationInBlock);
            uint256 currentAtNow = rewardRate * elapsedBlock;
            uint256 queuedRatio = currentAtNow * 1000 / newRewards;

            if (queuedRatio < newRewardRatio) {
                notifyRewardAmount(newRewards);
                queuedRewards = 0;
            } else {
                queuedRewards = newRewards;
            }
        }

        emit QueuedRewardsUpdated(startingQueuedRewards, startingNewRewards, queuedRewards);

        // Transfer the new rewards from the caller to this contract.
        IERC20(rewardToken).safeTransferFrom(msg.sender, address(this), newRewards);
    }
```

However, when this function tried to pull funds from sender via `safeTransferFrom`, it used `newRewards` amount, which already added  by `startingQueuedRewards`. If previously `queuedRewards` already have value, the processed amount will be wrong.


## Impact

There are two possible issue here : 

1. If previously `queuedRewards` is not 0, and the caller don't have enough funds or approval, the call will revert due to this logic error.
2. If previously `queuedRewards` is not 0,  and the caller have enough funds and approval, the caller funds will be pulled more than it should (reward param + `queuedRewards` )

## Code Snippet

https://github.com/sherlock-audit/2023-06-tokemak/blob/main/v2-core-audit-2023-07-14/src/rewarders/AbstractRewarder.sol#L236-L239
https://github.com/sherlock-audit/2023-06-tokemak/blob/main/v2-core-audit-2023-07-14/src/rewarders/AbstractRewarder.sol#L260

## Tool used

Manual Review

## Recommendation

Update the transfer to use `startingNewRewards` instead of `newRewards`  : 

```diff
    function queueNewRewards(uint256 newRewards) external onlyWhitelisted {
        uint256 startingQueuedRewards = queuedRewards;
        uint256 startingNewRewards = newRewards;

        newRewards += startingQueuedRewards;

        if (block.number >= periodInBlockFinish) {
            notifyRewardAmount(newRewards);
            queuedRewards = 0;
        } else {
            uint256 elapsedBlock = block.number - (periodInBlockFinish - durationInBlock);
            uint256 currentAtNow = rewardRate * elapsedBlock;
            uint256 queuedRatio = currentAtNow * 1000 / newRewards;

            if (queuedRatio < newRewardRatio) {
                notifyRewardAmount(newRewards);
                queuedRewards = 0;
            } else {
                queuedRewards = newRewards;
            }
        }

        emit QueuedRewardsUpdated(startingQueuedRewards, startingNewRewards, queuedRewards);

        // Transfer the new rewards from the caller to this contract.
-        IERC20(rewardToken).safeTransferFrom(msg.sender, address(this), newRewards);
+        IERC20(rewardToken).safeTransferFrom(msg.sender, address(this), startingNewRewards);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Tokemak |
| Report Date | N/A |
| Finders | duc, bulej93, Kalyan-Singh, p0wd3r, 0xvj, xiaoming90, berndartmueller, shaka, lil.eth, lemonmon, wangxx2026, saidam017, Angry\_Mustache\_Man, 0xbepresent, Aymen0909, chaduke, BPZ, bitsurfer, 0xVolodya, bin2chen, pengun, caelumimperium, 1nc0gn170, l3r0ux |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/379
- **Contest**: https://app.sherlock.xyz/audits/contests/101

### Keywords for Search

`vulnerability`

