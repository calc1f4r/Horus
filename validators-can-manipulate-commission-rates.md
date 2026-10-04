---
# Core Classification
protocol: Tortuga
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48535
audit_firm: OtterSec
contest_link: https://tortuga.finance/
source_link: https://tortuga.finance/
github_link: https://github.com/MoveLabsXYZ/liquid-staking-ottersec

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
  - OtterSec
  - Harrison Green
  - Fineas Silaghi
---

## Vulnerability Title

Validators can Manipulate Commission Rates

### Overview


The bug report discusses an issue with registered validators being able to drastically increase their commission percentage at any time. This can result in them profiting from a large commission for a long period of time, as the stakes are locked for 30 days. The report suggests implementing a similar lockup period for commission changes to prevent unexpected increases. The issue has been fixed in the latest patch.

### Original Finding Content

## Registered Validators and Commission Structure

Registered validators can receive stake from the protocol or directly from individual delegators. Either way, a commission, set by the validator, must be paid. The `protocol_commission` must be smaller than `current_commission`, and both have to be smaller or equal to `ManagedStakePool max_commission`, which is set by the protocol in `delegation_service::initialize`. The issue is that validators have the ability to drastically increase the commission percentage at any given time.

## RUST Code Example

```rust
public entry fun change_commission(
    pool_owner: &signer,
    new_default_commission: u64,
    new_protocol_commission: u64,
) acquires ManagedStakePool {
    [...]
    assert_pool_exists(managed_pool_address);
    [...]
    assert!(
        new_default_commission <= managed_stake_pool.max_commission,
        error::invalid_argument(ECOMMISSION_EXCEEDS_MAX)
    );
    // (Input Assert, keep)
    assert!(
        new_protocol_commission <= new_default_commission,
        error::invalid_argument(EPROTOCOL_COMMISSION_EXCEEDS_DEFAULT)
    );
    [...]
    delegation_state::change_commission_internal(
        managed_pool_address,
        new_default_commission,
        new_protocol_commission,
    );
}
```

This allows a malicious validator to set a very small commission and later on increase it by a large margin. Given that the stakes are locked via lockup periods (30 days), the validator can profit from a large commission for a long period of time.

---

© 2022 OtterSec LLC. All Rights Reserved.

## Tortuga Audit 04 | Vulnerabilities

### Remediation

Implying a similar lockup period for commission percentage, as implied for the stake, could help avoid unexpected commission changes.

### Patch

Fixed in 90cd93e.

---

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tortuga |
| Report Date | N/A |
| Finders | OtterSec, Harrison Green, Fineas Silaghi |

### Source Links

- **Source**: https://tortuga.finance/
- **GitHub**: https://github.com/MoveLabsXYZ/liquid-staking-ottersec
- **Contest**: https://tortuga.finance/

### Keywords for Search

`vulnerability`

