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
solodit_id: 62254
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

Incorrect rounding in present/principal value calculations for negative values

### Overview

See description below for full details.

### Original Finding Content

## Description

During the supply and withdrawal flows, the protocol calculates the new principal value of the user position by calculating the actual present value of the position, adding or removing from it the new deposit or withdrawal, and calculating the principal value of that updated present value. This process, consisting of multiplications and divisions, is subject to rounding errors.

These rounding errors can lead to situations where, if the supplied or withdrawn value is zero or very small, the resulting present value is incorrectly calculated. In particular, in some cases, the resulting principal value may be less than the original value for supply operations, or more than the original value for withdrawal operations.

The present value and principal value calculation functions use inappropriate rounding for negative principal values (borrows), creating a systematic bias that favors borrowers at the expense of the protocol. The `muldivc` ceiling function rounds negative values toward zero rather than away from zero, which is incorrect for conservative debt calculations.

The present value calculation function routes to different rounding implementations based on the sign of the principal value:

```c
(int) present_value_borrow_calc (int index, int principal_value) inline {
    return muldivc(principal_value, index, constants::factor_scale);
}
```

```c
(int) present_value(int s_rate, int b_rate, int principal_value) inline {
    if (principal_value >= 0) {
        return present_value_supply_calc(s_rate, principal_value);
    } else {
        return present_value_borrow_calc(b_rate, principal_value);
    }
}
```

*Figure 9.1: Borrow present value calculation using ceiling division in contracts_internal/contracts/logic/utils.fc#L11*

The issue arises because `muldivc` performs ceiling division, which rounds toward positive infinity. For negative values, this means rounding toward zero, effectively reducing the absolute value of debt amounts. For example, if a calculation results in -8.5, `muldivc` rounds it to -8 instead of the more conservative -9. This systematic undercalculation of debt favors borrowers by reducing their owed amounts, while the protocol and suppliers bear the cost of these rounding errors.

## Recommendations

**Short term:** Ensure that present and principal value calculations use the correct rounding function that rounds negative values away from zero for conservative debt calculations.

**Long term:** Implement comprehensive unit testing of all rounding operations to ensure that they align with the protocol’s risk management strategy, where debt calculations should be conservative and favor the protocol over individual users.

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

