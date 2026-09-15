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
solodit_id: 47306
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

Reward Distribution Inconsistency

### Overview


The report describes a bug where updating the reward configuration with a new reward amount causes the reward per share value to not be adjusted correctly. This means that users will receive rewards based on the new amount instead of the old one. The suggested solution is to update the farm timestamp before updating the reward configuration. The bug has been fixed in the latest version.

### Original Finding Content

## Update Reward Configuration

When updating the reward configuration with a new `reward_per_day`, the `reward_per_share` value, which represents the reward per share, should be adjusted to reflect the new configuration. However, the `update_reward_config` function fails to calculate the previous unclaimed rewards and update the `farm.timestamp` based on the old `reward_per_day` prior to updating the `reward_per_share` before applying the new configuration.

```rust
> _reserve_farm.move_rust
public fun update_reward_config(
    farm: &mut ReserveFarm,
    type_info: TypeInfo,
    new_config: RewardConfig
) {
    let reward = borrow_reward_mut(farm, type_info);
    reward.reward_config = new_config;
}
```

This oversight means that users will receive rewards based on the new `reward_per_day` rather than the old one for the `time_diff` since the last update.

## Remediation

Update the value of `farm.timestamp` by invoking `self_update` prior to updating the `reward_config` in `update_reward_config`.

## Patch

Fixed in `9d25e65`.

© 2024 Otter Audits LLC. All Rights Reserved. 10/16

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

