---
# Core Classification
protocol: Yhairvesting
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31422
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-11-01-yHairVesting.md
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
  - Pashov
---

## Vulnerability Title

[L-04] Missing input validation in token price setters

### Overview

See description below for full details.

### Original Finding Content

The `setVTokenCost` and `setTokenCost` methods are missing lower and upper bounds, meaning the caller of them can set for example huge values so tokens are not actually purchasable. Make sure to put a sensible upper bound and possibly a lower bound on the values that you can set in those methods.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Yhairvesting |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-11-01-yHairVesting.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

