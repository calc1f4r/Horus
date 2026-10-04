---
# Core Classification
protocol: Tortugal TIP
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48027
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

Minimum Stake Bypass

### Overview


The Tortuga protocol has a bug in its delegation_service module, which manages pools and computes rewards for validators and delegators. While most users delegate through Tortuga, validators can also receive direct delegations through the delegation_service API. However, the function that ensures the minimum delegation amount is met does not apply to withdrawals, allowing users to bypass this limit by delegating a large amount and then immediately withdrawing it. To fix this, a restriction will be imposed on direct delegations to maintain a minimum amount or withdraw all funds. This bug has been fixed in the latest patch.

### Original Finding Content

## Tortuga Protocol and Delegation Service

The Tortuga protocol operates on top of the `delegation_service` module, which controls the pools and computes rewards for validators and delegators. While most users will delegate indirectly through Tortuga (`stake_router`), validators may also receive direct delegations through the `delegation_service` API. 

## Direct Delegation

Users who wish to delegate directly may invoke `delegation_service::delegate` and provide an amount. Internally, this function ensures that the amount provided meets a minimum delegation amount, which is configurable by the pool owner:

```move
fun certify_delegation(
    managed_pool_address: address,
    delegator_address: address,
    amount: u64
) { 
    ...
    assert!(
        amount >= managed_stake_pool.min_delegation_amount,
        error::invalid_argument(EDELEGATION_AMOUNT_TOO_SMALL)
    );
    ...
}
```

While this check ensures that the instantaneous delegation amount is above the required minimum, withdrawals do not impose this limit. Therefore, a user may delegate some amount of stake higher than `min_delegation_amount`, then immediately withdraw a large portion to effectively bypass this limit.

## Remediation

Impose a restriction on direct delegations such that delegators maintain a minimum delegation amount at all times or withdraw all their funds.

## Patch

Fixed in `af0d61f`.

© 2023 OtterSec LLC. All Rights Reserved. 6 / 24

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tortugal TIP |
| Report Date | N/A |
| Finders | OtterSec, Harrison Green, Fineas Silaghi |

### Source Links

- **Source**: https://tortuga.finance/
- **GitHub**: https://github.com/MoveLabsXYZ/liquid-staking-ottersec
- **Contest**: https://tortuga.finance/

### Keywords for Search

`vulnerability`

