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
solodit_id: 53529
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-07-22-Tokemak.md
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
  - Hexens
---

## Vulnerability Title

[TOKE-5] Immediate Reward for the First Staker if Time Has Passed

### Overview


The bug report discusses a problem with the `AbstractRewarder::_updateReward()` function in the code. This function updates the `lastUpdateBlock` variable only if the `rewardPerTokenStored` is greater than 0. This is done to prevent the loss of rewards when there are no stakes in the rewarder. However, this can lead to an unfair distribution of rewards among stakers. If a user stakes their tokens at the start of a reward program, they can trigger the function again and receive all the rewards for the time period, even though they should not receive any rewards. The report suggests adding the rewards accumulated during periods with no supply to the `queuedRewards` to fix this issue. The bug has been fixed. 

### Original Finding Content

**Severity:** Medium

**Path:** src/rewarders/AbstractRewarder.sol#L120-L135

**Description:**

In the function `AbstractRewarder::_updateReward()`, the `lastUpdateBlock` is only updated if `rewardPerTokenStored` is greater than 0. Consider a scenario where only the first reward program has been queued: this means that `lastUpdateBlock` is updated only when `totalSupply` is greater than 0. This condition is designed to prevent the loss of rewards when there are no stakes in the rewarder. However, it introduces a risk of unfair reward distribution among stakers.

Assume that X seconds have passed since the start of the reward program, and a user stakes their tokens. Since this user is the first staker, when the `_updateReward()` function is invoked, `lastUpdateBlock` remains unchanged and is set to the start of the reward program. After the staking is complete, `totalSupply` becomes non-zero. The first staker can then trigger the `_updateReward()` function again, and because `totalSupply` is now greater than 0, `_updateReward()` will distribute all the `X * rewardRate` reward tokens to the first staker.

In this situation, the first staker receives rewards that should not be distributed to anyone, leading to an unfair distribution of rewards.

```
function _updateReward(address account) internal {
    uint256 earnedRewards = 0;
    rewardPerTokenStored = rewardPerToken();


    // Do not update lastUpdateBlock if rewardPerTokenStored is 0, to prevent the loss of rewards when supply is 0
    if (rewardPerTokenStored > 0) {
        if (account != address(0)) {
            lastUpdateBlock = lastBlockRewardApplicable();
            earnedRewards = earned(account);
            rewards[account] = earnedRewards;
            userRewardPerTokenPaid[account] = rewardPerTokenStored;
        }
    }


    emit UserRewardUpdated(account, earnedRewards, rewardPerTokenStored, lastUpdateBlock);
}
```

**Remediation:**  Consider adding the rewards accumulated during periods with no supply to the `queuedRewards`.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Tokemak |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-07-22-Tokemak.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

