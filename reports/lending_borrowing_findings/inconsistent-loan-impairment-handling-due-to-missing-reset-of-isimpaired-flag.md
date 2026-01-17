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
solodit_id: 45731
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

Inconsistent Loan Impairment Handling Due to Missing Reset of isImpaired Flag

### Overview


This bug report discusses an issue with the removeLoanImpairment function in the LoanManager contract. The function does not properly reset the isImpaired flag to false after removing a loan's impairment. This can lead to incorrect calculations and handling of loan defaults. The recommended solution is to update the function to include a line that resets the flag to false.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**: 

The removeLoanImpairment function in the LoanManager contract fails to reset the isImpaired flag to false after removing a loan's impairment. As a result, the loan remains incorrectly marked as impaired, leading to inconsistencies in how the loan is managed by the contract. This can cause incorrect calculations of unrealized losses and improper handling of loan defaults.

**Scenario**:

A loan is impaired by calling the impairLoan function, which correctly sets the isImpaired flag to true.
Later, the removeLoanImpairment function is called to remove the impairment. However, the function does not reset the isImpaired flag to false.
Despite the loan no longer being impaired, subsequent operations (such as triggerDefault) continue to treat the loan as impaired, leading to incorrect behavior and calculations.
For example, the unrealized losses calculated in PoolConfigurator::triggerDefault may be overstated because the loan is still incorrectly considered impaired.

**Recommendation**: 

Update the removeLoanImpairment function to include a line that resets the isImpaired flag to false after successfully removing the impairment. This ensures that the loan's state is correctly managed and that subsequent operations handle the loan as expected

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

