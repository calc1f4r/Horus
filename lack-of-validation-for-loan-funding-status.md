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
solodit_id: 45732
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

Lack of Validation for Loan Funding Status

### Overview


The withdrawFunds function in the loan management system does not check if the loan has been fully funded before allowing the seller to withdraw funds. This can result in a situation where the seller tries to withdraw funds before the loan is fully funded, leading to an inconsistent state and potential financial discrepancies. To fix this, a validation check should be added to the function to ensure the loan's funding status is confirmed before allowing any withdrawals. The client has confirmed this as an issue and it can make the loan and funds unusable. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**: 

The withdrawFunds function does not validate whether the loan has been fully funded before allowing the seller to withdraw funds. This could lead to a situation where a seller attempts to withdraw funds before the loan is adequately capitalized.

**Scenario**:

A loan is created, but for some reason, the funding process is delayed or incomplete.
The seller, without realizing the loan isn't fully funded, calls the withdrawFunds function.
Since there’s no validation check, the function might proceed with transferring funds, leading to an unexpected contract state or even financial discrepancies.

**Impact**: 

This can lead to an inconsistent state where the loan is not properly funded but funds are withdrawn. This could also potentially open up avenues for abuse, where a seller could try to withdraw funds from a partially funded loan.

**Recommendation**: 

Add a validation check in the withdrawFunds function to ensure that the loan's funding status is confirmed before allowing any withdrawal. This can be achieved by checking if the loan’s startDate is set (indicating the loan is funded).

**Client comment**: 

This is confirmed to be an issue: if the Pool Admin has not invoked LoanManager::fundLoan and the seller has already triggered LoanManager::withdrawFunds, the receivable will be transferred from the seller to the LoanManager contract. However, no asset tokens will be transferred since the loan's drawableFunds is not a non-zero amount. This prevents the user from withdrawing the funds again, making the receivable and the corresponding loan unusable.

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

