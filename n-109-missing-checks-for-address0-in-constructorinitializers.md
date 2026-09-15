---
# Core Classification
protocol: Panoptic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33809
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-panoptic
source_link: https://code4rena.com/reports/2024-04-panoptic
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
finders_count: 0
finders:
---

## Vulnerability Title

[N-109] Missing checks for `address(0)` in constructor/initializers

### Overview

See description below for full details.

### Original Finding Content


Check for zero-address to avoid the risk of setting `address(0)` for state variables when deploying.

*There are 9 instances of this issue.*

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Panoptic |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-panoptic
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-04-panoptic

### Keywords for Search

`vulnerability`

