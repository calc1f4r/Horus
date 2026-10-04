---
# Core Classification
protocol: Aries Markets
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47305
audit_firm: OtterSec
contest_link: https://ariesmarkets.xyz/
source_link: https://ariesmarkets.xyz/
github_link: https://github.com/aries-markets/aries-markets

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
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Missing Timestamp Update

### Overview


The bug report states that when adding or removing rewards in the liquidity farming contract, the update_reward function is called to adjust the reward per share based on the elapsed time. However, the function does not update the farm's timestamp after invoking update_reward. This can lead to double-claimed rewards if subsequent distribution actions occur without updating the timestamp. The report recommends updating the timestamp in the add_reward and remove_reward functions to fix this issue. The bug has been patched in the latest version of the contract. 

### Original Finding Content

## Reward Updating in Liquidity Farming Contract

When adding or removing rewards in the liquidity farming contract, the `update_reward` function is called to adjust the reward per share based on the elapsed time (`time_diff`). However, these functions currently do not update the `farm.timestamp` after invoking `update_reward`. Consequently, if subsequent reward distribution actions occur without updating the timestamp, the rewards for the same time period will be double-claimed.

> _reserve_farm.moverust_

```rust
public fun add_reward(farm: &mut ReserveFarm, type_info: TypeInfo, amount: u128) {
    [...]
    update_reward(reward, time_diff, farm.share);
    reward.remaining_reward = reward.remaining_reward + amount;
}

public fun remove_reward(farm: &mut ReserveFarm, type_info: TypeInfo, amount: u128) {
    [...]
    update_reward(reward, time_diff, share);
    assert!(reward.remaining_reward >= amount, ERESERVE_FARM_NEGATIVE_REWARD_BALANCE);
    reward.remaining_reward = reward.remaining_reward - amount;
}
```

## Proof of Concept

1. A reward is added or removed from the contract using `reserve_farm::add_reward` or `reserve_farm::remove_reward`, which internally calls `update_reward` to calculate and update the reward per share based on the elapsed time since the last update (`time_diff`).
2. After the `update_reward` call, the `farm.timestamp` remains unchanged, indicating that no new rewards have been distributed at the current time.
3. However, rewards for the `time_diff` are already factored into the reward per share calculation.
4. If additional reward distribution actions occur without updating the `farm.timestamp`, the rewards for the same `time_diff` period will be double-claimed.

## Remediation

Update the value of `farm.timestamp` by invoking `self_update` in `reserve_farm::add_reward` and `reserve_farm::remove_reward`.

© 2024 Otter Audits LLC. All Rights Reserved. 8/16

## Aries Market Audit 04 — Vulnerabilities
## Patch

Fixed in `9d25e65`.

© 2024 Otter Audits LLC. All Rights Reserved. 9/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aries Markets |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://ariesmarkets.xyz/
- **GitHub**: https://github.com/aries-markets/aries-markets
- **Contest**: https://ariesmarkets.xyz/

### Keywords for Search

`vulnerability`

