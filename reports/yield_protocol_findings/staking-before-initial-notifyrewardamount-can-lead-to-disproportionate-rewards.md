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
solodit_id: 19684
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/synthetix/unipool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/synthetix/unipool/review.pdf
github_link: none

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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Staking Before Initial notifyRewardAmount Can Lead to Disproportionate Rewards

### Overview


This bug report is about a user being able to call the get_reward() function after staking an amount of UNI tokens before the function notifyRewardAmount() is called for the first time. This can result in the user being paid out more funds than their share of the SNX rewards. The bug report recommends two solutions: preventing stake() from being called before notifyRewardAmount() is called for the first time, or setting lastUpdatetime to block.timestamp during the first execution of notifyRewardAmount(). The second recommendation has been implemented in the code.

### Original Finding Content

## Description

If a user successfully stakes an amount of UNI tokens before the function `notifyRewardAmount()` is called for the first time, their `initialuserRewardPerTokenPaid` will be set to zero. The first time `notifyRewardAmount()` is called, both `rewardRate` and `periodFinish` will be set; however, `lastUpdateTime` will remain zero.

The staker may then call the `earned()` function which will state their balance as:

```
earned = now * rewardRate * percent_of_stake
```

Since both `lastUpdateTime` and `userRewardPerTokenPaid` are zero, this can therefore allow a staker to call `get_reward()` at a later date when the contract has sufficient funds. The staker would be paid out funds greater than their share of the SNX rewards. For a proof-of-concept, see `test_get_reward.py/test_get_rewards_stake_early()`.

## Recommendations

We recommend preventing `stake()` from being called before `notifyRewardAmount()` is called for the first time. Alternatively, set `lastUpdateTime` to `block.timestamp` during the first execution of `notifyRewardAmount()`.

## Resolution

The second recommendation has been introduced in commit `df79f70`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

