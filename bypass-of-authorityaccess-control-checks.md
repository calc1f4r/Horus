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
solodit_id: 47018
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

Bypass Of Authority/Access Control Checks

### Overview


The vulnerability in PermissionSet instruction arises from how errors are handled within derive_any_permissioned. This function calls derive_permissioned::<OracleAccountData, _> and derive_permissioned::<PullFeedAccountData, _>, but immediately discards any errors via ok(). This means that any checks on the granter's authority and access control may be bypassed, allowing unauthorized entities to gain control over oracle and pull feed accounts. This compromises the system's integrity and security. To fix this issue, the errors should be properly propagated back to the caller instead of being discarded. The issue has been resolved in version 6ed294e.

### Original Finding Content

## Vulnerability in PermissionSet

The vulnerability in `PermissionSet` instruction arises from how errors are handled within `derive_any_permissioned`. `derive_any_permissioned` calls `derive_permissioned::<OracleAccountData, _>` and `derive_permissioned::<PullFeedAccountData, _>`, but it immediately discards any errors via `ok()`.

```rust
// permission/permission_set_action.rs
fn derive_any_permissioned<'a, F>(account: &'a AccountInfo<'a>, f: F) -> Result<()>
where
    F: Fn(&mut dyn Permissioned) -> Result<()>,
{
    derive_permissioned::<OracleAccountData, _>(account, &f).ok();
    derive_permissioned::<PullFeedAccountData, _>(account, &f).ok();
    Ok(())
}
```

In the closure passed to `derive_any_permissioned`, checks on the granter’s authority and access control checks are performed. However, since any errors from `derive_any_permissioned` are discarded, these checks may be bypassed. As a result, any entity may change permissions on any oracle or pull feed account. This will result in unauthorized entities gaining control over oracles and pull feeds, compromising the system’s integrity and security.

## Remediation

Ensure the errors are not discarded in `derive_any_permissioned`. Instead, they should be properly propagated back to the caller.

## Patch

Resolved in 6ed294e.

© 2024 Otter Audits LLC. All Rights Reserved. 9/39

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

