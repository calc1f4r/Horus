---
# Core Classification
protocol: Mysten Deepbook
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47058
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/deepbookv3

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
  - Robert Chen
  - Sangsoo Kang
  - MichałBochnak
---

## Vulnerability Title

Volume Overflow Risk

### Overview


The report states that there is a bug in the code that is causing a shortage of fees in the white listed pool. This can be exploited by attackers using self-trading and flash loans to artificially inflate volume metrics. The lack of trading fees makes it easy for attackers to engage in high-frequency trading without incurring significant costs. The bug is caused by an overflow in the total volume and total staked volume variables, which can also affect the maker_volume variable. The suggested solution is to change these variables to a larger data type to prevent overflows. The bug has been resolved in a recent update.

### Original Finding Content

## Current Situation

Currently, there is a lack of fees in the whitelisted pool, which may be exploited by utilizing self-trading and flash loans to artificially inflate volume metrics. In the absence of trading fees, attackers face minimal cost barriers to engaging in high-frequency trading activities. This situation makes it feasible to execute a large number of trades rapidly without incurring significant costs. An attacker may create multiple accounts and trade between them, generating a large volume of trades without actually changing their net position.

## History

> _his tory. mover ust_

### Function: add_volume

/// Add volume to the current epoch's volume data.  
/// Increments the total volume and total staked volume.  
```rust
public(package) fun add_volume(self: &mut History, maker_volume: u64, account_stake: u64) {
    if (maker_volume == 0) return;
    self.volumes.total_volume = self.volumes.total_volume + maker_volume;
    if (account_stake >= self.volumes.trade_params.stake_required()) {
        self.volumes.total_staked_volume = self.volumes.total_staked_volume + maker_volume;
    };
}
```

In `history::add_volume`, each trade increases `self.volumes.total_volume` by `maker_volume`. With enough trades, this value will exceed the maximum value that a `u64` may hold, resulting in an overflow. If the `account_stake` meets the required threshold, `self.volumes.total_staked_volume` is also increased by `maker_volume`. This value will similarly overflow if enough trades are executed. Similar to the Volumes structure, if the `Account.maker_volume` is stored as a `u64`, it will overflow when subjected to the same self-trading and flash loan attacks. 

## Remediation

Change `Volumes.total_volume`, `Volumes.total_staked_volume`, and `Account.maker_volume` to `u128`. This increases the maximum value that these variables may hold, significantly reducing the possibility of overflows.

## Patch

Resolved in PR #187.

© 2024 Otter Audits LLC. All Rights Reserved. 12/27

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Deepbook |
| Report Date | N/A |
| Finders | Robert Chen, Sangsoo Kang, MichałBochnak |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/deepbookv3
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

