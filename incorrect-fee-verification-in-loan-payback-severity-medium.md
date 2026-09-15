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
solodit_id: 20929
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

Incorrect Fee Verification in Loan Payback Severity: Medium

### Overview


This bug report is about an issue with the hasBorrowerEnoughFundsForPayback function. This function is used to check if a borrower has enough funds to pay back a loan, including the interest and a fee. Currently, the fee is calculated as a portion of the interest amount, which means the borrower is required to have more funds than necessary. The recommendation is to not consider the fee in the verification, and only require the borrower to have enough funds to cover the loan amount and the interest (minus the fee).

### Original Finding Content

**Description:** 

The hasBorrowerEnoughFundsForPayback function checks if the borrower has enough funds to pay back the loan, the interest, and the fee. However, the fee is a portion of the interest amount, not an additional cost. This means that the borrower is required to have more funds than necessary to pay back the loan.

**Recommendations:**

The fee should not be considered in the verification, not added to it. This will ensure that the borrower is only required to have enough funds to cover the loan amount and the interest (minus the fee).

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

