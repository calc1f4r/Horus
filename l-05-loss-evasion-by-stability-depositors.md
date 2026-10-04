---
# Core Classification
protocol: Roots_2025-02-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55128
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
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

[L-05] Loss evasion by stability depositors

### Overview

See description below for full details.

### Original Finding Content

In extreme scenarios, a CDP's collateral ratio may drop below 100%. If this occurs during normal mode, depositors of the stability pool might be motivated to withdraw their deposits to prevent losses before the liquidation process begins.

Consider adding a check in `StabilityPool.withdrawFromSP()` to prevent withdrawals when there are troves that are liquidatable.

See more details in this [GH issue](https://github.com/liquity/dev/issues/34) from Liquity V1.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Roots_2025-02-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

