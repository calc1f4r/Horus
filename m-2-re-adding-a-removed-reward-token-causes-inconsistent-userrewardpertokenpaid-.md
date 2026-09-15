---
# Core Classification
protocol: Summer.fi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63464
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1176
source_link: none
github_link: https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2-judging/issues/23

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
finders_count: 25
finders:
  - ni8mare
  - cu5t0mPe0
  - 0xAlipede
  - 0xxAristos
  - makarov
---

## Vulnerability Title

M-2: Re-adding a removed reward token causes inconsistent userRewardPerTokenPaid accounting

### Overview


This bug report is about an issue found in the StakingRewardsManager contract, which is used for distributing rewards to users who stake their tokens. The issue was found by a group of people and has been acknowledged by the team, but it will not be fixed at this time.

The problem occurs when a reward token is removed from the staking contract. Users who deposit their tokens after the removal do not have their `userRewardPerTokenPaid` value updated for that token, so it remains at `0`. If the same token is later re-added, the `rewardPerTokenStored` for that token is not reset, which causes inconsistencies in the reward distribution among users.

The root cause of this issue is that when a reward token is removed, it is not properly removed from the `rewardTokensList` map. This leads to the `rewardTokenAlreadyExists` error when the same token is re-added. Additionally, the `updateReward` function does not update the `userRewardPerTokenPaid` value for users who have staked after the removal of the token.

The impact of this bug is that some users may receive excess rewards, while others may be unable to claim their rewards. In some cases, the entire `claimRewards` function may fail, preventing users from claiming their rewards. This makes the contract unusable for fair reward distribution after a reward token has been re-added.

There is currently no response from the team or a proof of concept for this issue. To mitigate this problem, the team should whitelist all reward tokens and ensure that users update their token stored on entry, especially for tokens that can be re-added after removal. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2-judging/issues/23 

This issue has been acknowledged by the team but won't be fixed at this time.

## Found by 
0x23r0, 0x37, 0xAlipede, 0xFlare, 0xShoonya, 0xxAristos, AestheticBhai, Bigsam, FalseGenius, MoonShadow, Olami\_ooo, PratRed, SafetyBytes, coffiasd, cu5t0mPe0, dimulski, farismaulana, makarov, n1ikh1l, ni8mare, radevweb3, silver\_eth, t.aksoy, theweb3mechanic, werulez99

### Summary

When a reward token is removed from the staking contract, users who deposit afterwards never have their `userRewardPerTokenPaid` value updated for that token, so it remains `0`. If the same token is later re-added, the `rewardPerTokenStored` for that token is not reset, since it retains its previous state.

### Root Cause

```solidity
   /// @notice Removes a reward token from the list of reward tokens
    /// @param rewardToken The address of the reward token to remove
    function removeRewardToken(address rewardToken) external onlyGovernor {
        if (!_isRewardToken(rewardToken)) {
            revert RewardTokenDoesNotExist();
        }

        if (block.timestamp <= rewardData[rewardToken].periodFinish) {
            revert RewardPeriodNotComplete();
        }

        // Check if all tokens have been claimed, allowing a small dust balance
        uint256 remainingBalance = IERC20(rewardToken).balanceOf(address(this));
        uint256 dustThreshold;

        try IERC20Metadata(address(rewardToken)).decimals() returns (
            uint8 decimals
        ) {
            // For tokens with 4 or fewer decimals, use a minimum threshold of 1
            // For tokens with more decimals, use 0.01% of 1 token
            if (decimals <= 4) {
                dustThreshold = 1;
            } else {
                dustThreshold = 10 ** (decimals - 4); // 0.01% of 1 token
            }
        } catch {
            dustThreshold = 1e14; // Default threshold for tokens without decimals
        }

        if (remainingBalance > dustThreshold) {                     // donstion attack
            revert RewardTokenStillHasBalance(remainingBalance);
        }

@auidt>>         // Remove the token from the rewardTokens map
@auidt>>        bool success = _rewardTokensList.remove(address(rewardToken));
@auidt>>         if (!success) revert RewardTokenDoesNotExist();

        emit RewardTokenRemoved(address(rewardToken));
    }

```

```solidity
    /**
     * @dev Internal implementation of notifyRewardAmount
     * @param rewardToken The token to distribute as rewards
     * @param reward The amount of reward tokens to distribute
     * @param newRewardsDuration The duration for new reward tokens (only used for first time)
     */
    function _notifyRewardAmount(
        address rewardToken,
        uint256 reward,
        uint256 newRewardsDuration
    ) internal {
        RewardData storage rewardTokenData = rewardData[rewardToken];
        if (newRewardsDuration == 0) {
            revert RewardsDurationCannotBeZero();
        }

        if (newRewardsDuration > MAX_REWARD_DURATION) {
            revert RewardsDurationTooLong();
        }

        // For existing reward tokens, check if current period is complete.  // bug no check.
        if (_isRewardToken(rewardToken)) {
            if (newRewardsDuration != rewardTokenData.rewardsDuration) {
                revert CannotChangeRewardsDuration();
            }
        } else {

            // First time setup for new reward token

@auidt>>             bool success = _rewardTokensList.add(rewardToken);
@auidt>>             if (!success) revert RewardTokenAlreadyExists();

@auidt>>             rewardTokenData.rewardsDuration = newRewardsDuration;
@auidt>>             emit RewardTokenAdded(rewardToken, rewardTokenData.rewardsDuration);
        }

        // Transfer exact amount needed for new rewards
        IERC20(rewardToken).safeTransferFrom(msg.sender, address(this), reward);

        // Calculate new reward rate
        rewardTokenData.rewardRate =
            (reward * Constants.WAD) /
            rewardTokenData.rewardsDuration;
        rewardTokenData.lastUpdateTime = block.timestamp;
        rewardTokenData.periodFinish =
            block.timestamp +
            rewardTokenData.rewardsDuration;

        emit RewardAdded(address(rewardToken), reward);
    }
}
```

```solidity

    struct RewardData {
        uint256 periodFinish;
        uint256 rewardRate;
        uint256 rewardsDuration;
        uint256 lastUpdateTime;
        uint256 rewardPerTokenStored;
    }
```


```solidity
    function _updateReward(address account) internal {
        uint256 rewardTokenCount = _rewardTokensList.length();
        for (uint256 i = 0; i < rewardTokenCount; i++) {
            address rewardTokenAddress = _rewardTokensList.at(i);
            RewardData storage rewardTokenData = rewardData[rewardTokenAddress];
            rewardTokenData.rewardPerTokenStored = rewardPerToken(
                rewardTokenAddress
            );
            rewardTokenData.lastUpdateTime = lastTimeRewardApplicable(
                rewardTokenAddress
            );
            if (account != address(0)) {

@audit>>                rewards[rewardTokenAddress][account] = earned(
                    account,
                    rewardTokenAddress
                );

@audit>>                  userRewardPerTokenPaid[rewardTokenAddress][
                    account
                ] = rewardTokenData.rewardPerTokenStored;
            }
        }
    }
```

### Internal Pre-conditions

https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2/blob/main/summer-earn-protocol/packages/rewards-contracts/src/contracts/StakingRewardsManagerBase.sol#L250-L288


https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2/blob/main/summer-earn-protocol/packages/rewards-contracts/src/contracts/StakingRewardsManagerBase.sol#L391-L431


### External Pre-conditions

........

### Attack Path

1.  User Stakes 
2. Rweard Notification
3. After a while, the Reward token removal
4. New Users Stake 
5. After a while 
6. Same token is readded

### Impact

If a reward token is re-added, the staking contract’s reward accounting becomes inconsistent across users:

* Some users can claim **excess rewards** they are not entitled to.
* Other users may be left with **stranded or unclaimable rewards**.
* In cases where underpaid users attempt to claim, the entire `claimRewards` function may revert, preventing them from claiming.
This makes the contract unusable for fair reward distribution after a reward token has been re-added.


### PoC

_No response_

### Mitigation

Whitelist all reward tokens, ensuring users update their token stored on entry, especially tokens that can be readded after removal.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Summer.fi |
| Report Date | N/A |
| Finders | ni8mare, cu5t0mPe0, 0xAlipede, 0xxAristos, makarov, silver\_eth, radevweb3, 0xShoonya, 0x23r0, Olami\_ooo, farismaulana, theweb3mechanic, 0x37, FalseGenius, 0xFlare, AestheticBhai, t.aksoy, SafetyBytes, Bigsam, PratRed, dimulski, n1ikh1l, MoonShadow, werulez99, coffiasd |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-09-summer-fi-governance-v2-judging/issues/23
- **Contest**: https://app.sherlock.xyz/audits/contests/1176

### Keywords for Search

`vulnerability`

