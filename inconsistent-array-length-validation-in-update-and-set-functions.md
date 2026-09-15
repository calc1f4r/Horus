---
# Core Classification
protocol: DexodusV2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52408
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dexodus/dexodusv2
source_link: https://www.halborn.com/audits/dexodus/dexodusv2
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
  - Halborn
---

## Vulnerability Title

Inconsistent Array Length Validation in Update and Set Functions

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `updateUserVipLevel`, `updateUserAffiliate`, and `setVipLevelsDiscount` functions fail to validate that the input arrays `_users` and `vipLevel`, `_users` and `affiliateReceives`, and `vipLevel` and `discount` have matching lengths. This can lead to the following issues:

1. **Incomplete Updates** - If one array is shorter than the other, updates or assignments may be skipped, leaving some values uninitialized or unchanged.
2. **Reverts** - If the first array (used for iteration) is longer, attempts to access out-of-bound indices in the second array can trigger runtime reverts, resulting in a denial of service.

Such behavior could lead to incomplete or inconsistent data states, which may be exploited to create discrepancies in user permissions or rewards.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:H/A:L/D:N/Y:N/R:F/S:U (2.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:H/A:L/D:N/Y:N/R:F/S:U)

##### Recommendation

Add a validation step at the beginning of each function to ensure that all input arrays have the same length. For example:

```
require(_users.length == vipLevel.length, "Input arrays length mismatch");

```

Similar checks should be implemented for all affected functions. This ensures data consistency and prevents runtime errors during execution.

##### Remediation

**SOLVED**: Array length validation is not performed

##### Remediation Hash

2a9423c22a20ceddb37bd7c4a166e686817373a6

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | DexodusV2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dexodus/dexodusv2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dexodus/dexodusv2

### Keywords for Search

`vulnerability`

