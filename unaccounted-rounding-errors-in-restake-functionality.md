---
# Core Classification
protocol: Amnis Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47292
audit_firm: OtterSec
contest_link: https://amnis.finance/
source_link: https://amnis.finance/
github_link: https://github.com/amnis-finance/amnis-contract

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Unaccounted Rounding Errors In Restake Functionality

### Overview

See description below for full details.

### Original Finding Content

## Delegation Manager: Restake Functionality

`delegation_manager::restake` calculates the amount of pending inactive stake to restake (`restake_amount`) based on the minimum between the remaining amount to restake (`remain_amount`) and the available pending inactive stake. However, it does not account for rounding errors originating from `delegation_pool::reactivate_stake`, leading to cases where the pool covers these losses.

> _delegation_manager rust_

```rust
public(friend) fun restake(amount: u64): u64 acquires DelegationManager, DelegationRecord {
    [...]
    vector::for_each(all_delegations, |delegation| {
        let delegation = *delegation_record_data(delegation);
        let (_, _, pending_inactive) = delegation_pool::get_stake(
            delegation.stake_pool,
            delegation_manager_address()
        );
        if (pending_inactive > 0 && remain_amount > 0) {
            let restake_amount = math64::min(remain_amount, pending_inactive);
            delegation_pool::reactivate_stake(delegation_signer(),
                delegation.stake_pool, restake_amount);
            update_state(delegation.stake_pool);
            remain_amount = remain_amount - restake_amount;
        };
    });
    remain_amount
}
```

## Remediation

Update `restake` to track rounding errors in the same way as `unstake`.

## Patch

Fixed in `44d5605`.

© 2024 Otter Audits LLC. All Rights Reserved. 5/10

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Amnis Finance |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://amnis.finance/
- **GitHub**: https://github.com/amnis-finance/amnis-contract
- **Contest**: https://amnis.finance/

### Keywords for Search

`vulnerability`

