---
# Core Classification
protocol: Coinlend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20934
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
github_link: none

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
finders_count: 1
finders:
  - AuditOne
---

## Vulnerability Title

Incorrect interestRate check allows users create unreasonable high interestRate loan

### Overview


This bug report describes an issue with the createLoanLend() function. The function incorrectly checks ltv <= 1000 instead of interestRate <= 1000, which allows users to create loans with interest rates of 100% or 1000%. To fix this, it is recommended to change the check to interestRate <= 1000 to prevent users from creating loans with unreasonably high-interest rates.

### Original Finding Content

**Description:**

The interestRate check in the createLoanLend() function is incorrect. Instead of checking interestRate <= 1000, it mistakenly checks ltv <= 1000. The value of ltv is already validated earlier to always be smaller than maxLTV. This missing upper bound check allows users to create loans with interest rates of 100% or 1000%.

**Recommendations:**

Consider fixing the interestRate check to interestRate <= 1000 to ensure that users cannot create loans with unreasonably high-interest rates.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Coinlend |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

