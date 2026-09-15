---
# Core Classification
protocol: Isle Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45735
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
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
  - Zokyo
---

## Vulnerability Title

The gracePeriod_ parameter in the requestLoan function of the LoanManager can be set indefinitely allowing the attacker to protect themselves from defaults if funded

### Overview


The LoanManager contract has a function called requestLoan that allows a buyer to specify a grace period for their loan. However, there is a bug in the triggerDefault function that checks if the loan is past the grace period. This bug allows the buyer to set an indefinite grace period, which can prevent the admin from triggering a default on the loan. It is recommended that the admin be able to set a maximum threshold for grace periods and that there be additional validations for grace periods when requesting a loan. The client suggests using a multi-signature wallet for the admin to enhance security and reduce the risk of approving bad loans.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Location**: LoanManager.sol#requestLoan

**Description**: 

The requestLoan function of the LoanManager contract allows a buyer when requesting a loan to specify a grace period for the loan. This is seen as a “warning” period for which the borrower will have to return their loan to a healthy state or else their position will be put into a defaulted state by the pool configurator admin. There exists a condition in the triggerDefault function of the loan manager which will check if the loan is past the supplied grace period. 

Because this value can be set to an indefinite value (ie. a date that is excessively far into the future), this can prevent the admin from triggering a default on the loan if repayments aren’t made.

**Recommendation**

Consider allowing the pool configurator admin to set a maximum threshold after a loan due date for which grace periods can be set to prevent overly extensive grace periods. It’s recommended that there are additional validations made on the grace period when requesting a loan. 

**Client comment**: 

 This scenario is similar to the one mentioned in this issue's comments. While the buyer can set arbitrary parameters in the LoanManager::requestLoan function, the request may still be rejected by the Pool Admin.
Pool Admin use a multi-signature wallet, such as Safe, instead of a single wallet. This will enhance security and ensure that loan approvals are more robust, reducing the risk of arbitrary or bad loans being approved by a single party..

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Isle Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

