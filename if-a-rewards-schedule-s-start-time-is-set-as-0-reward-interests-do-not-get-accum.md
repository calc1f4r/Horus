---
# Core Classification
protocol: Dahlia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46375
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443
source_link: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - kankodu
  - Yorke Rhodes
---

## Vulnerability Title

If a rewards schedule 's start time is set as 0, reward interests do not get accumulated 

### Overview


This bug report discusses an issue in the code for WrappedVault.sol, specifically in the function _calculateRewardsPerToken. The problem arises when a reward schedule is created with a start time of 0, as the interest accumulation process is skipped, causing user rewards to not be updated. This is due to the assumption that a start time of 0 means there are no active reward schedules, which is not always true. The report includes a proof of concept and recommends changing the code to check for the non-zeroness of the rate instead of the start time. The bug has been fixed in a recent commit.

### Original Finding Content

## WrappedVault Reward Schedule Issue

## Context
WrappedVault.sol#L361-L362

## Description
When one creates a reward schedule, it is allowed to set the start to `0`. But in `_calculateRewardsPerToken`, the interest accumulation process is skipped, which causes the user rewards to not be updated:

```solidity
if (rewardsInterval_.start == 0) return rewardsPerTokenOut;
```

Perhaps this was due to the assumption that if the start time is `0`, then there couldn't be any active reward schedules. This, however, is not true. Here is a simple PoC that can be added to `test/core/integration/WrappedVaultTakeRewards.t.sol`:

```solidity
function testTakeRewardsWithStartIntervalZero() public {
    // !!!!!! change this params for checking rewards
    uint256 rewardAmount = 100_000 * 10 ** TestLib.rewardERC20decimals; // 1000 USDC rewards
    uint256 depositAmount = 500 * 10 ** TestLib.vaultERC20decimals; // 500 ETH
    uint32 start = 0; // <--- note the `0` start time
    uint32 duration = 30 days + uint32(block.timestamp);
    console.log("duration (seconds):", duration);
    testIncentivizedVault.addRewardsToken(address(rewardToken1));
    rewardToken1.mint(address(this), rewardAmount);
    rewardToken1.approve(address(testIncentivizedVault), rewardAmount);
    testIncentivizedVault.setRewardsInterval(address(rewardToken1), start, start + duration, rewardAmount, DEFAULT_FEE_RECIPIENT);
    
    RewardMockERC20(address(token)).mint($.alice, depositAmount);
    vm.startPrank($.alice);
    token.approve(address(testIncentivizedVault), depositAmount);
    uint256 d1 = testIncentivizedVault.deposit(depositAmount, $.alice);
    vm.stopPrank();
    console.log("user1 deposit: ", d1);
    console.log("undistributed rewards:", rewardToken1.balanceOf(address(testIncentivizedVault)));
    console.log("user1 rewards: ", rewardToken1.balanceOf($.alice));
    vm.warp(start + duration + 1);
    vm.startPrank($.alice);
    testIncentivizedVault.claim($.alice);
    vm.stopPrank();
    console.log("\n #### End of rewards period. Expecting DEFAULT_FRONTEND_FEE and DEFAULT_PROTOCOL_FEE to stay");
    console.log("undistributed rewards:", rewardToken1.balanceOf(address(testIncentivizedVault)));
    console.log("user1 rewards: ", rewardToken1.balanceOf($.alice));
}
```

## Recommendation
To check whether there is an active reward schedule or not, it is best to check the non-zeroness of the rate instead. When one creates a reward schedule, the non-zeroness of the final rate gets checked:

1. In `setRewardsInterval` (WrappedVault.sol#L318), the rate is checked to be non-zero.
2. In `extendRewardsInterval` (WrappedVault.sol#L272), the rate has been checked to ensure it does not decrease (if non-zero, it stays non-zero).

## Apply the Following Changes
```diff
diff --git a/src/royco/contracts/WrappedVault.sol b/src/royco/contracts/WrappedVault.sol
index 0578e04..c684483 100644
--- a/src/royco/contracts/WrappedVault.sol
+++ b/src/royco/contracts/WrappedVault.sol
@@ -358,8 +358,8 @@ contract WrappedVault is Owned, ERC20, IWrappedVault {
 // No changes if the program hasn't started
 if (block.timestamp < rewardsInterval_.start) return rewardsPerTokenOut;
- // No changes if the start value is zero
- if (rewardsInterval_.start == 0) return rewardsPerTokenOut;
+ // No changes if the rate is zero, i.e., there is no active reward schedule for the reward token in context.
+ if (rewardsInterval_.rate == 0) return rewardsPerTokenOut;
 // Stop accumulating at the end of the rewards interval
 uint256 updateTime = block.timestamp < rewardsInterval_.end ? block.timestamp : rewardsInterval_.end;
```

### Dahlia:
Fixed in commit `bb8ce8fa`.

### Cantina Managed:
Fixed by disallowing the start time to be `0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Dahlia |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, kankodu, Yorke Rhodes |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443

### Keywords for Search

`vulnerability`

