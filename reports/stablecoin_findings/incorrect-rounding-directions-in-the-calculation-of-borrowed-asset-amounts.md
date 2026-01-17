---
# Core Classification
protocol: Folks Finance Capital Market Protocol v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21277
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-11-folksfinance-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-11-folksfinance-securityreview.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Vara Prasad Bandaru
  - Josselin Feist
---

## Vulnerability Title

Incorrect rounding directions in the calculation of borrowed asset amounts

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

## Target: formulae.py, loan.py

### Description
Multiple incorrect rounding directions are used in the computation of the amount borrowed in a loan. Thus, the result of the calculation may be too low, causing the system to underestimate the amount of assets borrowed in a loan.

To determine whether a loan is overcollateralized, `is_loan_over_collateralized` iterates over an array of all collateral assets and sums the underlying values of those assets:

*CODE REDACTED*

Figure 6.1: REDACTED

As part of this process, it calls `get_stable_borrow_balance` and `get_var_borrow_balance`, both of which call `calc_borrow_balance` to calculate the borrow balance of the loan at time `t`:

*CODE REDACTED*

Figure 6.2: REDACTED

The operation performed by the `calc_borrow_balance` function is equivalent to that shown in figure 6.3:

*CODE REDACTED*

Figure 6.3: REDACTED

The function adds 1 to the result of the equation to round it up. However, the portion of the equation rounds down, which can cause the overall rounding error to be greater than 1.

Similar issues are present in other functions involved in the computation, including the following:

- `calc_asset_loan_value`, which rounds down the results of its two calls to `mul_scale`
- `calc_borrow_interest_index`, which rounds down the result of the `mul_scale` call
- `exp_by_squaring`, which also rounds down the result of the `mul_scale` call

The cumulative loss of precision can cause the system to underestimate the amount of assets borrowed in a loan, preventing the loan’s liquidation. 

We set the severity of this issue to low because the loss of precision is limited. However, there may be other rounding issues present in the codebase.

### Exploit Scenario
Eve’s loan has become undercollateralized. However, because the loan contract rounds down when calculating the amount borrowed in a loan, it does not identify Eve’s loan as undercollateralized, and the position cannot be liquidated. By contrast, if the contract performed precise accounting, Eve’s loan would be eligible for liquidation.

### Recommendations
**Short term:** Ensure all arithmetic operations in `is_loan_over_collateralized` use a conservative rounding direction—that is, ensure that the loss of precision causes the system to interpret a loan as less collateralized than it actually is. Additionally, document those operations.

**Long term:** Document the expected rounding direction of every arithmetic operation, and create rounding-specific functions (e.g., `mul_scale_down` and `mul_scale_down_up`) to facilitate reviews of the arithmetic rounding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Folks Finance Capital Market Protocol v2 |
| Report Date | N/A |
| Finders | Vara Prasad Bandaru, Josselin Feist |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-11-folksfinance-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-11-folksfinance-securityreview.pdf

### Keywords for Search

`vulnerability`

