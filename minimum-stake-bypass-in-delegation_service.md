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
solodit_id: 48534
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

Minimum Stake Bypass in delegation_service

### Overview


The report discusses a bug in the Tortuga protocol, which is a system used to delegate and compute rewards for validators and delegators. The bug involves the delegation_service module, which allows users to delegate directly to validators through an API. The bug allows users to bypass the minimum delegation amount by delegating a large amount and then immediately withdrawing a large portion. The proposed solution is to impose a restriction on direct delegations, requiring users to maintain the minimum delegation amount at all times or withdraw all their funds. The bug has been fixed in the af0d61f patch.

### Original Finding Content

## Tortuga Protocol Overview

The Tortuga protocol operates on top of the `delegation_service` module, which manages the pools and computes rewards for the validators and delegators. While most users will delegate indirectly through Tortuga (`stake_router`), validators can also receive direct delegations through the `delegation_service` API.

## Direct Delegations

Users who want to delegate directly can invoke `delegation_service::delegate` and provide an amount. Internally, this function ensures that the amount provided meets a minimum delegation amount (which is configurable by the pool owner):

```MOVE
fun certify_delegation(
    managed_pool_address: address,
    delegator_address: address,
    amount: u64
) ... {
    ...
    assert!(
        amount >= managed_stake_pool.min_delegation_amount,
        error::invalid_argument(EDELEGATION_AMOUNT_TOO_SMALL)
    );
    ...
}
```

While this check ensures that the instantaneous delegation amount is above the required minimum, this limit is not imposed upon withdrawals. Therefore, a user can simply delegate some amount of stake higher than `min_delegation_amount` and then immediately withdraw a large portion to effectively bypass this limit.

## Remediation

Impose a restriction on direct delegations such that delegators need to maintain a minimum delegation amount at all times (or withdraw all their funds).

## Patch

Fixed in af0d61f.

© 2022 OtterSec LLC. All Rights Reserved. 6 / 19

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

