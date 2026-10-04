---
# Core Classification
protocol: Bond Options
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20733
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/99
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-bond-judging/issues/108

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

protocol_categories:
  - services

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - TrungOre
  - Yuki
  - bin2chen
  - berndartmueller
  - Delvir0
---

## Vulnerability Title

M-9: stake() missing set lastEpochClaimed when userBalance equal 0

### Overview


This bug report is about an issue in the `stake()` function of the OTLM contract. The issue is that when a user balance is equal to 0, the `lastEpochClaimed[user]` is not set. This means that when a new user stakes, they have to loop from 0 to the last epoch in order to claim rewards, which wastes a lot of GAS and may eventually lead to a GAS_OUT. The code snippet provided in the report shows that in the `stake()` function, the `rewardsPerTokenClaimed[msg.sender]` is set, but not the `lastEpochClaimed[msg.sender]`. 

The impact of this is that when the epoch increases, the new stake will waste a lot of GAS, and when it is very large, it will cause GAS_OUT. The recommendation for this issue is to set the `lastEpochClaimed[msg.sender]` in the `stake()` function. 

The discussion in the report shows that the proposed solution was agreed upon and a fix was implemented. The fix set the `lastEpochClaimed[msg.sender]` to `epoch - 1` to make the user state appear like they have claimed everything before the epoch they started staking on. The fix was reviewed and approved.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-bond-judging/issues/108 

## Found by 
Delvir0, TrungOre, Yuki, berndartmueller, bin2chen, ctf\_sec
## Summary
because `stake()` don't  set ` lastEpochClaimed[user] = last epoch` if `userBalance` equal 0
So all new stake user must loop from 0 to `last epoch` for `_claimRewards()`
As the epoch gets bigger and bigger it will waste a lot of GAS, which may eventually lead to `GAS_OUT`

## Vulnerability Detail
in `stake()`,  when the first-time stake() only `rewardsPerTokenClaimed[msg.sender]`
but don't set `lastEpochClaimed[msg.sender]`

```solidity
    function stake(
        uint256 amount_,
        bytes calldata proof_
    ) external nonReentrant requireInitialized updateRewards tryNewEpoch {
...
        uint256 userBalance = stakeBalance[msg.sender];
        if (userBalance > 0) {
            // Claim outstanding rewards, this will update the rewards per token claimed
            _claimRewards();
        } else {
            // Initialize the rewards per token claimed for the user to the stored rewards per token
@>          rewardsPerTokenClaimed[msg.sender] = rewardsPerTokenStored;
        }

        // Increase the user's stake balance and the total balance
        stakeBalance[msg.sender] = userBalance + amount_;
        totalBalance += amount_;

        // Transfer the staked tokens from the user to this contract
        stakedToken.safeTransferFrom(msg.sender, address(this), amount_);
    }
```

so every new staker , needs claims from 0 
```solidity
    function _claimRewards() internal returns (uint256) {
        // Claims all outstanding rewards for the user across epochs
        // If there are unclaimed rewards from epochs where the option token has expired, the rewards are lost

        // Get the last epoch claimed by the user
@>      uint48 userLastEpoch = lastEpochClaimed[msg.sender];

        // If the last epoch claimed is equal to the current epoch, then only try to claim for the current epoch
        if (userLastEpoch == epoch) return _claimEpochRewards(epoch);

        // If not, then the user has not claimed all rewards
        // Start at the last claimed epoch because they may not have completely claimed that epoch
        uint256 totalRewardsClaimed;
@>     for (uint48 i = userLastEpoch; i <= epoch; i++) {
            // For each epoch that the user has not claimed rewards for, claim the rewards
            totalRewardsClaimed += _claimEpochRewards(i);
        }

        return totalRewardsClaimed;
    }
```
With each new addition of epoch, the new stake must consumes a lot of useless loops, from loop 0 to `last epoch`
When `epoch` reaches a large size, it will result in GAS_OUT and the method cannot be executed

## Impact
When the `epoch` gradually increases, the new take will waste a lot of GAS
When it is very large, it will cause GAS_OUT

## Code Snippet
https://github.com/sherlock-audit/2023-06-bond/blob/main/options/src/fixed-strike/liquidity-mining/OTLM.sol#L324-L327

## Tool used

Manual Review

## Recommendation
```solidity
    function stake(
        uint256 amount_,
        bytes calldata proof_
    ) external nonReentrant requireInitialized updateRewards tryNewEpoch {
...
        if (userBalance > 0) {
            // Claim outstanding rewards, this will update the rewards per token claimed
            _claimRewards();
        } else {
            // Initialize the rewards per token claimed for the user to the stored rewards per token
            rewardsPerTokenClaimed[msg.sender] = rewardsPerTokenStored;
+           lastEpochClaimed[msg.sender] = epoch;
        }
```




## Discussion

**Oighty**

Agree with the proposed solution.

**ctf-sec**

Great finding, agree with medium severity

**Oighty**

Fix implemented at https://github.com/Bond-Protocol/options/pull/5

**ctf-sec**

Will look into this, seems all the duplicate suggest the fix:

```solidity
 lastEpochClaimed[msg.sender] = epoch;
```

but the implemented fix is 

```solidity
 lastEpochClaimed[msg.sender] = epoch -1
```

maybe testing can help as well, just want to make sure there is no off-by-one issue o(╥﹏╥)o

**Oighty**

> Will look into this, seems all the duplicate suggest the fix:
> 
> ```solidity
>  lastEpochClaimed[msg.sender] = epoch;
> ```
> 
> but the implemented fix is
> 
> ```solidity
>  lastEpochClaimed[msg.sender] = epoch -1
> ```
> 
> maybe testing can help as well, just want to make sure there is no off-by-one issue o(╥﹏╥)o

The reason to set lastEpochClaimed to `epoch - 1` is that you want the user state to appear like they have claimed everything before the epoch they started staking on. They haven't claimed any tokens for the current epoch yet, so that would be inaccurate.

**Oighty**

@ctf-sec did you have a chance to review this more?

**ctf-sec**

Yes, fix looks good

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Bond Options |
| Report Date | N/A |
| Finders | TrungOre, Yuki, bin2chen, berndartmueller, Delvir0, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-bond-judging/issues/108
- **Contest**: https://app.sherlock.xyz/audits/contests/99

### Keywords for Search

`vulnerability`

