---
# Core Classification
protocol: Holder Incentive Program
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52242
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dynex/holder-incentive-program
source_link: https://www.halborn.com/audits/dynex/holder-incentive-program
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Missing Reward Duration Check

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `notifyRewardAmount` function performs integer division that truncates to zero when the reward amount is less than the reward duration. This leads to a complete loss of rewards.

```
function notifyRewardAmount(uint64 reward) external onlyRole(REWARDS_DISTRIBUTION_ROLE) updateReward(address(0)) {
    if (block.timestamp >= periodFinish) {
        rewardRate = reward / rewardsDuration;
```

  

When `reward < rewardsDuration`, the division `reward / rewardsDuration` truncates to 0. This behavior is demonstrated with:

* reward = 2,591,999
* rewardsDuration = 2,592,000
* resulting rewardRate = 0

  

A `rewardRate` of 0 leads to no rewards being distributed to stakers despite tokens being allocated for rewards.

```
function rewardPerToken() public view returns (uint256) {
    if (totalSupply == 0) return rewardPerTokenStored;
    return
        rewardPerTokenStored +
        (((lastTimeRewardApplicable() - lastUpdateTime) * rewardRate * 10 ** decimals) / totalSupply);
}
```

  

With `rewardRate` = 0, `rewardPerToken()` will not increase, resulting in no rewards' accumulation.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

It is recommended to implement a minimum reward amount check:

```
function notifyRewardAmount(uint64 reward) external onlyRole(REWARDS_DISTRIBUTION_ROLE) updateReward(address(0)) {
    if (reward < rewardsDuration) revert RewardTooLow();
    if (block.timestamp >= periodFinish) {
        rewardRate = reward / rewardsDuration;
    }
    // ... rest of the function
}
```

  

Add the error:

```
error RewardTooLow();
```

  

This ensures reward amounts will always result in a non-zero reward rate, preventing silent failures in the reward distribution mechanism.

##### Remediation

**SOLVED**: A check was added by **Dynex team** to ensure that `reward > rewardsDuration`.

##### Remediation Hash

<https://github.com/dynexcoin/DHIPSmartContracts/pull/2/commits/70a008227111cc8de8883bac502a5b28c7773331>

##### References

[dynexcoin/DHIPSmartContracts/contracts/DynexHolderIncentiveProgram.sol#L305](https://github.com/dynexcoin/DHIPSmartContracts/blob/audit/contracts/DynexHolderIncentiveProgram.sol#L305)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Holder Incentive Program |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dynex/holder-incentive-program
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dynex/holder-incentive-program

### Keywords for Search

`vulnerability`

