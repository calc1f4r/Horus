---
# Core Classification
protocol: Lombard Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46738
audit_firm: OtterSec
contest_link: https://www.lombard.finance/
source_link: https://www.lombard.finance/
github_link: https://github.com/lombard-finance/sui-contracts

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

Lack of Configurable Delay Setting in Timelock

### Overview

The timelock_upgrade::authorize_upgrade function is using a fixed delay of 24 hours instead of referencing the configurable delay stored in timelock.delay_ms. This makes the customizable delay feature useless and inconsistent. To fix this, the function should use timelock.delay_ms instead of the fixed delay. This issue has been fixed in the latest patch, d2e3a5d.

### Original Finding Content

## Timelock Upgrade Authorization

The `timelock_upgrade::authorize_upgrade` function utilizes a fixed delay of `MS_24_HOURS` (24 hours) to enforce the time restriction on upgrades, rather than referencing the configurable delay stored in `timelock.delay_ms`. This introduces inconsistency and defeats the purpose of having a customizable delay feature.

> **File:** timelock_policy/sources/timelock_upgrade.move

```rust
public fun authorize_upgrade(
    timelock: &mut TimelockCap,
    policy: u8,
    digest: vector<u8>,
    ctx: &mut TxContext,
): UpgradeTicket {
    let epoch_start_time_ms = ctx.epoch_timestamp_ms();
    assert!(
        timelock.last_authorized_time == 0 || epoch_start_time_ms >=
        timelock.last_authorized_time + MS_24_HOURS,
        ENotEnoughTimeElapsed,
    );
    timelock.last_authorized_time = epoch_start_time_ms;
    timelock.upgrade_cap.authorize(policy, digest)
}
```

## Remediation

Utilize `timelock.delay_ms` instead of `MS_24_HOURS` for better customizability.

## Patch

Fixed in commit `d2e3a5d`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Lombard Finance |
| Report Date | N/A |
| Finders | Michał Bochnak, Robert Chen, Sangsoo Kang |

### Source Links

- **Source**: https://www.lombard.finance/
- **GitHub**: https://github.com/lombard-finance/sui-contracts
- **Contest**: https://www.lombard.finance/

### Keywords for Search

`vulnerability`

