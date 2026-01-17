---
# Core Classification
protocol: Fndz
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56095
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-25-FNDZ.md
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
  - Zokyo
---

## Vulnerability Title

Zero address check

### Overview

See description below for full details.

### Original Finding Content

**Description**

contracts/FNDZToken.sol#355, constructor()
Check for zero address is missing. Since there is no way to retrieve tokens from the zero
address consider additional check. Thus the issue is marked as low.
The same issue refers to Vesting contract (Vesting.sol, line 465) - recipient is not checked
against zero address.

**Recommendation**:

Add check for the zero address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Fndz |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-25-FNDZ.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

