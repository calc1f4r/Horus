---
# Core Classification
protocol: Elixir_2025-08-17
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62328
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Elixir-security-review_2025-08-17.md
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

[L-04] Missing role bounds check in `has_role`

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The has_role function in `sources/acl.move` lacks role bounds validation, unlike other role functions. This inconsistency could cause runtime aborts if invalid role values (≥128) are passed. The issue may arise in future integrations where external contracts pass user-controlled role parameters or during cross-contract calls with unvalidated inputs.

Impact -> Runtime trxs abort instead of graceful error handling, leading to inconsistent API behavior.

Recommendation -> Add `assert!(role < 128, EInvalidRole);` at the beginning of `has_role` function for consistency with add_role and remove_role.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Elixir_2025-08-17 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Elixir-security-review_2025-08-17.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

