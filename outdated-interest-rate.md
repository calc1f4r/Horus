---
# Core Classification
protocol: Paribus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37394
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-Paribus.md
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

Outdated interest rate

### Overview


The report discusses a bug in the PToken.sol contract, where the methods `borrowRatePerBlock(...)` and `supplyRatePerBlock(...)` use the `getBorrowRate()` and `getSupplyRate()` methods from the interestRateModel contract. However, these methods rely on the `utilizationRate(...)` method, which uses outdated variables. This leads to incorrect calculations for the borrow rate and supply rate. The recommended solution is to call the `accrueInterest()` method first in the `borrowRatePerBlock(...)` and `supplyRatePerBlock(...)` methods.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

In Contract PToken.sol, the methods `borrowRatePerBlock(...)` and `supplyRatePerBlock(...)` uses interestRateModel contract’s getBorrowRate() and getSupplyRate().

Further,  getBorrowRate() and getSupplyRate() use the `utilizationRate(...)` method to calculate the respective rates. 

Now, utilizationRate method uses the following formula to calculate:
return borrows.mul(1e18).div(cash.add(borrows).sub(reserves));
Which clearly depends on the borrows, cash, and reserves amount. 

Now these variables (borrows, cash, and reserves) are out of date as they need to be updated in accrueInterest() method. Because of this cascading effect, the finally calculated borrow rate and supply rate will be not up-to-date as well.

Recommendation: Call the `accrueInterest()` method in the borrowRatePerBlock(...) and supplyRatePerBlock(...) methods first.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Paribus |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-Paribus.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

