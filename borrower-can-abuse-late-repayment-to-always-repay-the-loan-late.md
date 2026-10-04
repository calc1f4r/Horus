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
solodit_id: 20937
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

Borrower can abuse late repayment to always repay the loan late

### Overview


This bug report describes an issue with the protocol of a loan. Borrowers are allowed to repay the loan late without any penalty or fees, which could be an incentive for them to always repay late. The lender's function forceLiquidateExpiredLoan() checks if the borrower can repay first and tries to repay instead of liquidating the collateral. To prevent this from happening, the report recommends applying a fee when the borrower repays late or a higher interest rate for the late repayment period. This would discourage borrowers from repaying late and ensure that the lender is compensated for the delay.

### Original Finding Content

**Description:** 

In the protocol, borrowers are allowed to repay the loan late without any penalty or fees. Even when the lender calls the function forceLiquidateExpiredLoan(), it still checks if the borrower can repay first and tries to repay instead of liquidating the collateral. However, during the late repayment period, the borrower only needs to pay the same interest rate and no penalty or fee is applied. As a result, it could be an incentive for borrowers to always repay late, in spite of the duration agreed upon by both parties.

**Recommendations:**

Consider applying a fee when the borrower repays late or a higher interest rate for the late repayment period.

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

