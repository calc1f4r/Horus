---
# Core Classification
protocol: Starknet_2025-07-31
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62460
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Starknet-security-review_2025-07-31.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-04] Zero-amount initial undelegation intents allows `Event` spamming

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

The `exit_delegation_pool_intent()` function in the delegation pool contract allows a `pool member` to submit an `amount = 0` request even if they have no existing undelegate intent.

This triggers event emissions `PoolMemberExitIntent` and `PoolMemberBalanceChanged` (on the pool side) and `RemoveFromDelegationPoolIntent` and `StakeDelegatedBalanceChanged` (on staking contract) that have no real meaning.
```rust
    // @audit When 0, unpool_time is set to None but the rest of function flows normally
>>  if amount.is_zero() {
        pool_member_info.unpool_time = Option::None;
    } else {
        pool_member_info.unpool_time = Option::Some(unpool_time);
    }
    ...
    // pool::exit_delegation_pool_intent()
    self.emit(Events::PoolMemberExitIntent { ... });
    self.emit(Events::PoolMemberBalanceChanged { ... });

    // staking::remove_from_delegation_pool_intent()
    self.emit(Events::RemoveFromDelegationPoolIntent { ... });
    self.emit(Events::StakeDelegatedBalanceChanged { ... });
```
Because there’s no restriction on repeating such `zero-amount` calls, a malicious user could repeatedly call the function to generate spam events and polluting event logs.

**Recommendations**

Add a check to ensure that `zero-amount` calls are only permitted if the caller already has an active undelegate intent (`unpool_time.is_some()`).
```diff
+   assert!(
+       !amount.is_zero() || pool_member_info.unpool_time.is_some(),
+       "{}",
+       GenericError::ZERO_AMOUNT_INITIAL_INTENT
+   );

    // @audit proceed normaly
    if amount.is_zero() {
        pool_member_info.unpool_time = Option::None;
    } else {
        pool_member_info.unpool_time = Option::Some(unpool_time);
    }
```
This ensures:
- First-time exit intents must have `amount > 0`.
- Zero-amount calls are only valid as cancellations of existing intents.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Starknet_2025-07-31 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Starknet-security-review_2025-07-31.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

