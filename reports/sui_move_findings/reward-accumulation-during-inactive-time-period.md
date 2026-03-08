---
# Core Classification
protocol: Bluefin Spot
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46822
audit_firm: OtterSec
contest_link: https://bluefin.io/
source_link: https://bluefin.io/
github_link: https://github.com/fireflyprotocol/bluefin-spot-contracts

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
  - Michał Bochnak
  - Robert Chen
  - Sangsoo Kang
---

## Vulnerability Title

Reward Accumulation During Inactive Time Period

### Overview


This bug report discusses a vulnerability in how reward calculations are handled for liquidity positions after a reward distribution has ended and then restarts. This results in inaccurate rewards for positions as the calculation incorrectly includes inactive time in the reward accumulation. The bug is caused by the functions update_reward_infos and update, which rely on the difference between the last updated timestamp and the current timestamp. This means that when a new distribution restarts, the function does not account for any time gap between the previous reward end and the new start time, resulting in extra rewards for liquidity providers. The report recommends that rewards should only accumulate while there is an active reward emission and provides a patch to resolve the issue.

### Original Finding Content

## Vulnerability in Reward Calculations for Liquidity Positions

There is a vulnerability in how reward calculations are handled for liquidity positions after a reward distribution has ended and then restarts. There is no way to correctly restart the distribution of the same type after a reward distribution has finished. Specifically, the calculation incorrectly includes inactive time (the time period after the distribution ended but before it restarts) in the reward accumulation, resulting in inaccurate rewards for positions.

## Code Snippet

```move
public(friend) fun update_reward_infos<CoinTypeA, CoinTypeB>(pool: &mut Pool<CoinTypeA, CoinTypeB>, current_timestamp_seconds: u64) : vector<u128> {
    let reward_growth_globals = vector::empty<u128>();
    let current_index = 0;
    while (current_index < vector::length<PoolRewardInfo>(&pool.reward_infos)) {
        [...]
        if (current_timestamp_seconds > reward_info.last_update_time) {
            [...]
            if (pool.liquidity != 0 && min_timestamp > reward_info.last_update_time) {
                let rewards_accumulated = full_math_u128::full_mul(((min_timestamp - reward_info.last_update_time) as u128),
                reward_info.reward_per_seconds);
                [...]
                reward_info.total_reward_allocated = reward_info.total_reward_allocated + ((rewards_accumulated / (constants::q64() as u256)) as u64);
            };
            reward_info.last_update_time = current_timestamp_seconds;
        };
        vector::push_back<u128>(&mut reward_growth_globals, reward_info.reward_growth_global);
    };
    reward_growth_globals
}
```

In both `pool::update_reward_infos` and `position::update`, reward growth is based on the difference between the `current_timestamp_seconds` and the last update time. When `pool::update_pool_reward_emission` is called to restart distribution, the function does not account for any time gap between the previous reward end and the new start time. As a result, liquidity providers may receive extra rewards that do not correspond to any actual activity.

For example, if reward distribution ends at time `t0`, and a new distribution restarts at time `t1`, the reward accumulation for liquidity positions incorrectly includes the inactive period \[t0, t1\]. Ideally, rewards should only accumulate while there is an active reward emission. However, because `update_reward_infos` and `update` rely on the difference between the last updated timestamp and the current timestamp, they end up counting this inactive interval in reward calculations.

## Remediation

When calculating rewards, ensure that only the time intervals where rewards were actively distributed are included.

## Patch

Resolved in `f9025e9`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Bluefin Spot |
| Report Date | N/A |
| Finders | Michał Bochnak, Robert Chen, Sangsoo Kang |

### Source Links

- **Source**: https://bluefin.io/
- **GitHub**: https://github.com/fireflyprotocol/bluefin-spot-contracts
- **Contest**: https://bluefin.io/

### Keywords for Search

`vulnerability`

