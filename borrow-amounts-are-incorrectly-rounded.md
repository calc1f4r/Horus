---
# Core Classification
protocol: EVAA Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62249
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-08-evaafinance-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-08-evaafinance-securityreview.pdf
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
finders_count: 3
finders:
  - Kevin Valerio Trail of Bits PUBLIC
  - Guillermo Larregay
  - Quan Nguyen
---

## Vulnerability Title

Borrow amounts are incorrectly rounded

### Overview

See description below for full details.

### Original Finding Content

## Data Validation Report

**Difficulty:** Low  
**Type:** Data Validation  

## Description
Borrow amounts represent user debt, and therefore must be rounded up to avoid understating user liabilities. In FunC, it is recommended to use ceiling rounding in the `muldivc` function for these calculations. These small rounding errors can eventually add up and lead to a calculation mismatch between the internal accounting and the assets in custody.

Multiple borrow amount calculations throughout the `user-utils.fc` file fail to round up consistently, in particular:
- Line 164, in the `account_health_calc` function
- Line 231, in the `is_liquidatable` function
- Line 280, in the `get_available_to_borrow` function
- Line 354, in the `get_aggregated_balances` function

## Recommendations
**Short term:** Use `muldivc` instead of `muldiv` or normal multiplication and division when calculating user debt.

**Long term:** Expand the unit test suite to cover additional edge cases and to ensure that the system behaves as expected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | EVAA Finance |
| Report Date | N/A |
| Finders | Kevin Valerio Trail of Bits PUBLIC, Guillermo Larregay, Quan Nguyen |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-08-evaafinance-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-08-evaafinance-securityreview.pdf

### Keywords for Search

`vulnerability`

