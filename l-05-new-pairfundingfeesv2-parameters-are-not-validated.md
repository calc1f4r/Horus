---
# Core Classification
protocol: Ostium_2025-01-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61518
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ostium-security-review_2025-01-21.md
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

[L-05] New `PairFundingFeesV2` parameters are not validated

### Overview

See description below for full details.

### Original Finding Content


During the initialization of new funding fee parameters in the `initializeV2()` function, these values are not sanity-checked against the given maximum values.

Since a sanity check is performed in other setter functions when the `PairFundingFeesV2` parameters are updated, consider adding proper validation to the `initializeV2()` function as well.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ostium_2025-01-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ostium-security-review_2025-01-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

