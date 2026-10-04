---
# Core Classification
protocol: Switchboard On-chain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47020
audit_firm: OtterSec
contest_link: https://switchboard.xyz/
source_link: https://switchboard.xyz/
github_link: https://github.com/switchboard-xyz/sbv3

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
finders_count: 2
finders:
  - Akash Gurugunti
  - Robert Chen
---

## Vulnerability Title

Flawed Implementation of Reward Score Calculation

### Overview


This bug report discusses a vulnerability in the OracleHeartbeat instruction system for calculating rewards. The current implementation is flawed, as a higher slash_score (which is supposed to result in a lower reward) actually increases the reward. Additionally, if the reward_score is 0, the formula simplifies to simply giving the oracle the maximum reward, even if they did not perform any attestations. This could be exploited by malicious oracles to receive full rewards without participating. The suggested solution is to update the rewards calculation to ensure that a higher reward_score results in a higher reward. The issue has been patched in version b597ec.

### Original Finding Content

## Vulnerability in OracleHeartbeat

The vulnerability in the OracleHeartbeat instructions stems from the incorrect design of the reward calculation, specifically in the way it handles the relationship between `reward_score` and `slash_score`. The current implementation of the formula for reward calculation is such that the final reward is proportional to `slash_score` and inversely proportional to `reward_score`. This is counterintuitive; a higher `slash_score` should result in a lower reward, but instead, it increases the reward.

> _oracle/oracle_heartbeat_action.rs_
```rust
pub fn calculate_slash(stats: &OracleStatsAccountData, reward: u64) -> u64 {
    let slash_score = stats.finalized_epoch.slash_score;
    if slash_score == 0 {
        return 0;
    }
    let reward_score = stats.finalized_epoch.reward_score;
    Decimal::from(reward)
        .saturating_mul(reward_score.into())
        .checked_div(slash_score.into())
        .unwrap()
        .to_u64()
        .unwrap_or(0)
}
```

As a result, Oracles that are supposed to be penalized (with a high `slash_score`) will end up receiving higher rewards, which is the opposite of the intended effect. Furthermore, if `reward_score = 0`, the formula simplifies to `reward = reward`. This implies the oracle would receive the maximum reward even if it did not perform any attestations, which is a severe flaw. Ideally, an oracle with `reward_score = 0` should receive no reward, as it indicates a complete lack of participation. Thus, malicious oracles may exploit this flaw by not performing any attestations (resulting in `reward_score = 0`) and still receive full rewards, compromising the security and reliability of the entire network.

## Remediation

Update the rewards calculation to ensure that a higher `reward_score` results in a higher reward.

## Patch

Resolved in bb597ec.

© 2024 Otter Audits LLC. All Rights Reserved. 11/39

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Switchboard On-chain |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen |

### Source Links

- **Source**: https://switchboard.xyz/
- **GitHub**: https://github.com/switchboard-xyz/sbv3
- **Contest**: https://switchboard.xyz/

### Keywords for Search

`vulnerability`

