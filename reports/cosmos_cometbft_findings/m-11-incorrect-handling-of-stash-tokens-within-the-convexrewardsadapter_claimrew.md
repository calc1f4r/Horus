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
solodit_id: 27103
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/101
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/632

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
finders_count: 2
finders:
  - duc
  - nobody2018
---

## Vulnerability Title

M-11: Incorrect handling of Stash Tokens within the `ConvexRewardsAdapter._claimRewards()`

### Overview


This bug report is about an incorrect handling of Stash Tokens within the `ConvexRewardsAdapter._claimRewards()` function. The primary task of this function revolves around claiming rewards for Convex/Aura staked LP tokens. The bug lies in the check to identify whether `rewardToken[i]` is a stash token. It involves attempting to invoke `IERC20(rewardTokens[i]).totalSupply()`. If the returned total supply value is `0`, the implementation assumes the token is a stash token and bypasses it. However, this check is flawed since the total supply of stash tokens can indeed be non-zero. This misstep in checking can potentially lead to a Denial-of-Service (DOS) situation when calling the `claimRewards()` function. This can hamper the destination vault's ability to claim rewards from AURA staking, resulting in protocol losses. The bug was found by duc and nobody2018 and it was manually reviewed. The recommendation is to accurately determine whether a token is a stash token by performing a low-level `balanceOf()` call to the token and subsequently validate the call's success.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/632 

## Found by 
duc, nobody2018
The `ConvexRewardsAdapter._claimRewards()` function incorrectly handles Stash tokens, leading to potential vulnerabilities.

## Vulnerability Detail
The primary task of the `ConvexRewardAdapter._claimRewards()` function revolves around claiming rewards for Convex/Aura staked LP tokens.

```solidity=
function _claimRewards(
    address gauge,
    address defaultToken,
    address sendTo
) internal returns (uint256[] memory amounts, address[] memory tokens) {
    ... 

    // Record balances before claiming
    for (uint256 i = 0; i < totalLength; ++i) {
        // The totalSupply check is used to identify stash tokens, which can
        // substitute as rewardToken but lack a "balanceOf()"
        if (IERC20(rewardTokens[i]).totalSupply() > 0) {
            balancesBefore[i] = IERC20(rewardTokens[i]).balanceOf(account);
        }
    }

    // Claim rewards
    bool result = rewardPool.getReward(account, /*_claimExtras*/ true);
    if (!result) {
        revert RewardAdapter.ClaimRewardsFailed();
    }

    // Record balances after claiming and calculate amounts claimed
    for (uint256 i = 0; i < totalLength; ++i) {
        uint256 balance = 0;
        // Same check for "stash tokens"
        if (IERC20(rewardTokens[i]).totalSupply() > 0) {
            balance = IERC20(rewardTokens[i]).balanceOf(account);
        }

        amountsClaimed[i] = balance - balancesBefore[i];

        if (sendTo != address(this) && amountsClaimed[i] > 0) {
            IERC20(rewardTokens[i]).safeTransfer(sendTo, amountsClaimed[i]);
        }
    }

    RewardAdapter.emitRewardsClaimed(rewardTokens, amountsClaimed);

    return (amountsClaimed, rewardTokens);
}
``` 

An intriguing aspect of this function's logic lies in its management of "stash tokens" from AURA staking. The check to identify whether `rewardToken[i]` is a stash token involves attempting to invoke `IERC20(rewardTokens[i]).totalSupply()`. If the returned total supply value is `0`, the implementation assumes the token is a stash token and bypasses it. However, this check is flawed since the total supply of stash tokens can indeed be non-zero. For instance, at this [address](https://etherscan.io/address/0x2f5c611420c8ba9e7ec5c63e219e3c08af42a926#readContract), the stash token has `totalSupply = 150467818494283559126567`, which is definitely not zero.

This misstep in checking can potentially lead to a Denial-of-Service (DOS) situation when calling the `claimRewards()` function. This stems from the erroneous attempt to call the `balanceOf` function on stash tokens, which lack the `balanceOf()` method. Consequently, such incorrect calls might incapacitate the destination vault from claiming rewards from AURA, resulting in protocol losses.

## Impact
* The `AuraRewardsAdapter.claimRewards()` function could suffer from a Denial-of-Service (DOS) scenario.
* The destination vault's ability to claim rewards from AURA staking might be hampered, leading to protocol losses.

## Code Snippet
https://github.com/sherlock-audit/2023-06-tokemak/blob/main/v2-core-audit-2023-07-14/src/destinations/adapters/rewards/ConvexRewardsAdapter.sol#L80-L86

## Tool used
Manual Review

## Recommendation
To accurately determine whether a token is a stash token, it is advised to perform a low-level `balanceOf()` call to the token and subsequently validate the call's success.



## Discussion

**sherlock-admin2**

> Escalate
> 
> #649 is a duplicate of this issue.

    You've deleted an escalation for this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Tokemak |
| Report Date | N/A |
| Finders | duc, nobody2018 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/632
- **Contest**: https://app.sherlock.xyz/audits/contests/101

### Keywords for Search

`vulnerability`

