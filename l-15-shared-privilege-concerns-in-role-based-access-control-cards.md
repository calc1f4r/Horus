---
# Core Classification
protocol: RipIt_2025-04-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62573
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-04-25.md
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

[L-15] Shared privilege concerns in role-based access control cards

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

In the Card contract, the MINT_MANAGER_ROLE and REDEEM_MANAGER_ROLE are defined as privileged roles for managing card minting and redemption operations, respectively.

However, multiple `Cards` could refer to the same `rbac` (Role-Based Access Control) instance via `RoleBasedAccessControlConsumer`. This design implies that if a user is granted minting or redemption privileges in one `Card`, they inherently possess the same privileges in all other `Card` instances that share the same `rbac`.

This raises concerns about the independence of access control across different `Card` contracts, as it could lead to unintended privilege escalation or management issues if the roles are not intended to be universally applicable.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RipIt_2025-04-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-04-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

