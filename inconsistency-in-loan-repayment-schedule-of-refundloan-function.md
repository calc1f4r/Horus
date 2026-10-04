---
# Core Classification
protocol: Nemeos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59585
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
source_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Sebastian Banescu
  - Faycal Lalidji
  - Guillermo Escobero
---

## Vulnerability Title

Inconsistency in Loan Repayment Schedule of `refundLoan()` Function

### Overview


The bug report is about a function called `refundLoan()` in the `Pool.sol` file. This function currently has a problem where it adds a fixed amount of time to the loan repayment schedule, causing a discrepancy in the loan terms. This means that borrowers can accrue interest for a shorter period of time than originally intended, but still have the same amount of time to repay the loan. The recommendation is to adjust the function to account for the remaining days when making the final payment, to ensure fairness for both borrowers and lenders.

### Original Finding Content

**Update**
Fixed in `43badd87a66241c3030dbdc773858fec19f6f48d`.

**File(s) affected:**`Pool.sol`

**Description:** The `refundLoan()` function currently updates the `loan.nextPaymentTime` by directly adding the `MAX_LOAN_REFUND_INTERVAL`, which introduces a discrepancy in loan terms. Specifically, taking the case of a loan requested for 45 days, this calculation method allows the borrower to accrue interest for only the initial 45 days but grants an extension to repay the principal amount up to 60 days. This discrepancy arises because the `MAX_LOAN_REFUND_INTERVAL` is statically added to the `nextPaymentTime` without considering the original remaining loan duration which should be 15 days.

**Recommendation:** To ensure the repayment schedule aligns with the original loan terms and fairness in the interest accrual period, the loan repayment logic needs adjustment. Specifically, it should account for the remaining days when executing the final payment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nemeos |
| Report Date | N/A |
| Finders | Sebastian Banescu, Faycal Lalidji, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html

### Keywords for Search

`vulnerability`

