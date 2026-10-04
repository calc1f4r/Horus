---
# Core Classification
protocol: Synthetix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19686
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/synthetix/unipool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/synthetix/unipool/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Gap Between Periods Can Lead to Erroneous Rewards

### Overview


A bug was discovered in the SNX rewards system, which was resulting in the contract outputting more rewards than it received. This was due to the fact that lastUpdateTime included the time between periods, which meant that if there was a gap between periods, the rewards distributed would be greater than the reward amount specified in the notifyRewardAmount() function. This meant that if all stakers called getReward(), the contract would not have enough SNX balance to transfer out all the rewards and some stakers may not receive any rewards. To fix this issue, the recommendation was to enforce each period start exactly at the end of the previous period, which was implemented in commit df79f70.

### Original Finding Content

## Description

The SNX rewards are earned each period based on reward and duration as specified in the `notifyRewardAmount()` function.

The "rate per second" at which rewards are distributed is given by:

```
rewardRate = reward / duration
```

Rewards are paid out for all stakers following the formula:

```
rewards_distributed = rewardRate * (lastTimeRewardApplicable - lastUpdateTime)
```

However, `lastUpdateTime` includes the time between periods and therefore, if there is a gap between periods:

```
(lastTimeRewardApplicable - lastUpdateTime) > duration
```

Therefore, resulting in:

```
rewards_distributed > reward
```

Where `reward` is the amount from `notifyRewardAmount()` and `rewards_distributed` is the total amount earned by all stakers. The result is that the contract will output more rewards than it receives. Therefore, if all stakers call `getReward()`, the contract will not have enough SNX balance to transfer out all the rewards and some stakers may not receive any rewards.

For a proof-of-concept, see `test_get_reward.py/test_get_rewards_slippage()`.

## Recommendations

We recommend enforcing each period to start exactly at the end of the previous period.

## Resolution

The above recommendation has been implemented in commit `df79f70`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Synthetix |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/synthetix/unipool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/synthetix/unipool/review.pdf

### Keywords for Search

`vulnerability`

