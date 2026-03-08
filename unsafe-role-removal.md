---
# Core Classification
protocol: Cetus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47272
audit_firm: OtterSec
contest_link: https://www.cetus.zone/
source_link: https://www.cetus.zone/
github_link: https://github.com/CetusProtocol/cetus-limitorder

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

Unsafe Role Removal

### Overview


The bug report discusses a problem with the "remove_role" function in the ACL (Access Control List) code. When using the subtraction operation to remove a role, the current implementation fails to check if the role being removed is already unset, which can lead to unexpected results. The report suggests using a safe operation to ensure that only the specified role is removed. The recommended solution is to replace the operation with "*perms = *perms & (MAX_U128 - (1 << role))", which sets the bit position for the role to zero. The bug has been fixed in the latest version of the code.

### Original Finding Content

I n `acl::remove_role`, utilizing the subtraction operation for role removal may produce unexpected results. The current implementation fails to check if the role to be removed is set, allowing attempts to remove an unset role, which may result in other roles being added or removed. Employ a safe operation to guarantee that only the specified role is removed.

> _acl.move Rust_

```rust
/// @notice Revoke a role for a member in the ACL.
public fun remove_role(acl: &mut ACL, member: address, role: u8) {
    assert!(role < 128, ERoleNumberTooLarge);
    if (linked_table::contains(&acl.permissions, member)) {
        let perms = linked_table::borrow_mut(&mut acl.permissions, member);
        *perms = *perms - (1 << role);
    }
}
```

## Remediation
Replace the operation with `*perms = *perms & (MAX_U128 - (1 << role));`. In this case, the and operation sets the only bit position indicated by the role to zero.

## Patch
Fixed in a a1eba1.

© 2024 Otter Audits LLC. All Rights Reserved. 7/12

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cetus |
| Report Date | N/A |
| Finders | Robert Chen, Sangsoo Kang, MichałBochnak |

### Source Links

- **Source**: https://www.cetus.zone/
- **GitHub**: https://github.com/CetusProtocol/cetus-limitorder
- **Contest**: https://www.cetus.zone/

### Keywords for Search

`vulnerability`

