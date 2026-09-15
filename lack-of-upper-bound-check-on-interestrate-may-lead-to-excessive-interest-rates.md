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
solodit_id: 20927
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

Lack of Upper Bound Check on interestRate May Lead to Excessive Interest Rates

### Overview


This bug report is about the createLoanLend and createLoanBorrow functions which are not properly checking for excessively high interest rates. Currently, the code only checks that the interest rate is at least 1, but there is no upper limit set. Additionally, the code mistakenly checks ltv instead of interestRate in the same line. The recommendation is to set an upper bound for interestRate and correct the error in the require statement. The upper bound should be determined based on platform policies or market conditions.

### Original Finding Content

**Description:** 

The createLoanLend & createLoanBorrow functions currently check whether the interestRate is at least 1, but there is no upper bound check, allowing for excessively high interest rates. Moreover, the code seems to mistakenly check ltv again in the same line, which is probably a coding error.

**Recommendations:**

 An upper bound should be set for the interestRate to ensure that it does not exceed a reasonable value. The appropriate limit can be determined based on platform policies or market conditions. Also, correct the error in the require statement, where ltv is being checked instead of interestRate.

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

