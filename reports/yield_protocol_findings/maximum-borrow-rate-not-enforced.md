---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60124
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
finders_count: 3
finders:
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

Maximum Borrow Rate Not Enforced

### Overview


The client has reported a bug in the `TroveInterestRateStrategy.sol` file. The bug involves the calculation of outstanding debt using a variable interest rate. According to the `getMaxBorrowRate()` function, the amount should be capped at a certain value. However, the `calculateInterestRates()` function returns a value that may exceed this cap, potentially causing errors. The recommendation is to either ensure that the values returned by `calculateInterestRates()` do not exceed the cap set by `getMaxBorrowRate()`, or to remove the `getMaxBorrowRate()` function altogether. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `295913f6e865e18e56e4d776f61209752a4eb48c`. The client provided the following explanation:

> Borrow rate cannot exceed the value given by getMaxBorrowRate().

**File(s) affected:**`TroveInterestRateStrategy.sol`

**Description:** ERD applies a variable interest rate in the calculation of outstanding debt. Per the function `getMaxBorrowRate()`, this amount should be capped at `baseBorrowRate + rateSlope1 + rateSlope2`. However, the function `calculateInterestRates()`, in the case where `vars.utilizationRate < optimalUtilizationRate`, returns `baseBorrowRate + rateSlope1 + rateSlope2 * remaindUtilizationRateRatio` where the value `remaindUtilizationRateRatio` may be greater than 1. This means that the returned value can be greater than the value returned by `getMaxBorrowRate()`.

**Recommendation:** Determine whether there is to be a maximum borrow rate. If yes, make sure that the values returned by `calculateInterestRates()` cannot exceed the value given by `getMaxBorrowRate()`. If no, consider removing the function `getMaxBorrowRate()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

