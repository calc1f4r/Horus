---
# Core Classification
protocol: Sui Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47401
audit_firm: OtterSec
contest_link: https://www.mystenlabs.com/
source_link: https://www.mystenlabs.com/
github_link: https://github.com/MystenLabs/sui

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
  - Tuyết Dương
  - Jessica Clendinen
---

## Vulnerability Title

Inability To End An Epoch

### Overview


The report describes a bug where the system is unable to create a new committee at the end of an epoch due to an error in the code. When the function try_create_next_committee is called, it tries to create a new committee based on the registrations stored in member_registrations. However, when attempting to insert the members into the new_members mapping, using vec_map::insert, the insertion fails if the public key already exists in the mapping. This prevents the system from creating a new committee even if there is enough stake available. The result is that the committee is not updated properly and the end of epoch process fails to create the committee. The bug has been identified and a patch has been implemented to fix it. The fix restricts validators from registering with an existing public key. 

### Original Finding Content

## Validator Registration Issue

Register a validator to register with a used public key (`bridge_pubkey_bytes`). When `try_create_next_committee` is called at the end of epoch, the function creates a new committee based on the registrations stored in `member_registrations`. When attempting to insert the members into the `new_members` mapping utilizing `vec_map::insert`, the insertion will fail if the public key already exists in the mapping. This prevents the system from creating a new committee even if enough stake is available. As a result, the committee is not updated properly, and an end of epoch would fail to attempt to create the committee.

> _packages/bridge/sources/committee.moverust_

```rust
if (vector::contains(&validators, &registration.sui_address)) {
    let stake_amount = sui_system::validator_stake_amount(system_state, registration.sui_address);
    let voting_power = ((stake_amount as u128) * 10000) / total_stake_amount;
    total_member_stake = total_member_stake + (stake_amount as u128);
    let member = CommitteeMember {
        sui_address: registration.sui_address,
        bridge_pubkey_bytes: registration.bridge_pubkey_bytes,
        voting_power: (voting_power as u64),
        http_rest_url: registration.http_rest_url,
        blocklisted: false,
    };
    vec_map::insert(&mut new_members, registration.bridge_pubkey_bytes, member)
};
```

## Remediation

Restrict the validator from registering with an existing public key.

## Patch

Fixed in PR #16909.

© 2024 Otter Audits LLC. All Rights Reserved. 6/19

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Sui Bridge |
| Report Date | N/A |
| Finders | Tuyết Dương, Jessica Clendinen |

### Source Links

- **Source**: https://www.mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/sui
- **Contest**: https://www.mystenlabs.com/

### Keywords for Search

`vulnerability`

