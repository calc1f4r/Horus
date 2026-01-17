---
# Core Classification
protocol: Wild Credit
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 468
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-wild-credit-contest
source_link: https://code4rena.com/reports/2021-07-wildcredit
github_link: https://github.com/code-423n4/2021-07-wildcredit-findings/issues/122

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - don't_update_state

protocol_categories:
  - dexes
  - cdp
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-02] LendingPair.liquidateAccount does not accrue and update cumulativeInterestRate

### Overview


This bug report is about a vulnerability in the `LendingPair.liquidateAccount` function. It does not accrue and update the `cumulativeInterestRate` before liquidating an account, which could cause the liquidatee's state to not be up to date. This could lead to the liquidatee being able to skip paying some interest payments if they are underwater. The recommendation is to call `accrueAccount` instead of `_accrueAccountInterest` to fix this issue.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `LendingPair.liquidateAccount` function does not accrue and update the `cumulativeInterestRate` first, it only calls `_accrueAccountInterest` which does not update and instead uses the old `cumulativeInterestRate`.

## Impact
The liquidatee (borrower)'s state will not be up to date.
I could skip some interest payments by liquidating myself instead of repaying if I'm under-water.
As the market interest index is not accrued, the borrower does not need to pay any interest accrued from the time of the last accrual until now.

## Recommendation
It should call `accrueAccount` instead of `_accrueAccountInterest`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Wild Credit |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-wildcredit
- **GitHub**: https://github.com/code-423n4/2021-07-wildcredit-findings/issues/122
- **Contest**: https://code4rena.com/contests/2021-07-wild-credit-contest

### Keywords for Search

`Don't update state`

