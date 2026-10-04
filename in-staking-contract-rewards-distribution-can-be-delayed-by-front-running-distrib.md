---
# Core Classification
protocol: Templedao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33578
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
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
  - Hans
---

## Vulnerability Title

In staking contract, rewards distribution can be delayed by front-running distributeGold function

### Overview


The TempleGoldStaking contract has a bug where the reward distribution is delayed. This is because the `distributeRewards` function, which mints TLGD tokens and updates the reward rate, can only be called after a certain cooldown period has passed. However, anyone can call the `distributeGold` function, which updates the `lastRewardNotificationTimestamp` and can prevent the distributor from updating the reward rate. This can also lead to the rewards distribution being prevented forever if `distributeGold` is called regularly before the cooldown period. The recommended solution is to either limit access to the `distributeGold` function or introduce a new variable that tracks the latest timestamp of rewards distribution and can only be updated in the `distributeRewards` function. The bug has been fixed in a recent pull request by TempleDAO and has been verified by Cyfrin. 

### Original Finding Content

**Description:** In `TempleGoldStaking` contract, the reward distributer calls `distributeRewards` to by minting available TLGD from the token contract and updates reward rate based on the minted amount.
However, the distribution works only after the distribution cooldown period is passed:
```Solidity
if (lastRewardNotificationTimestamp + rewardDistributionCoolDown > block.timestamp)
    { revert CannotDistribute(); }
```

It uses `lastRewardNotificationTimestamp` as latest updated timestamp, which can be also updated by anyone who calls a public function `distributeGold`.
By front-running this function, it prevents the distributor from updating reward rate.

More seriously, if `distributeGold` is called regularly before the distribution cooldown, rewards distribution can be prevented forever.

**Impact:** Reward distribution can be delayed.

**Recommended Mitigation:** Either making `distributeGold` permissioned or introduce other state variable that represents the latest timestamp of rewards distribution, which is only updated in `distributeRewards` function.

**TempleDAO:** Fixed in [PR 1028](https://github.com/TempleDAO/temple/pull/1028)

**Cyfrin:** Verified

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Templedao |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

