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
solodit_id: 45734
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

Interest rates can be arbitrary which can allow the loan requester to set them to zero bypassing interest and late interest rates if funded

### Overview


The LoanManager contract has a low severity bug that allows buyers to bypass interest rates when requesting a loan. This can be fixed by having the contract admin set the interest rates using setters and validating the interest rates array against these state variables. It is also recommended to use a multi-signature wallet, such as Safe, for loan approvals to enhance security and reduce the risk of arbitrary or bad loans being approved by a single party.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Location**: LoanManager.sol#requestLoan

**Description**: 

The LoanManager allows a buyer to request a loan from the pool using the requestLoan function. The buyer can pass various parameters to the function such as the receivable asset, the receivables token id, grace period, principal requested and the interest rates as an array. The interestRate (as defined by the 0th index of the rates_ array) and the lateInterestPremiumRate (as defined by the 1st index of the rates_ array) can effectively be arbitrary. This can allow the buyer to specify these as zero in order to bypass interest rates.

**Recommendation**

It’s recommended that the contract admin sets these interest rates using setters within the contract. The interest rates array should be validated against these state variables.

**Client comment**: 

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

