---
# Core Classification
protocol: Umee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16904
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Paweł Płatek
  - Dominik Czarnota
---

## Vulnerability Title

Incorrect comparison in SetCollateralSetting method

### Overview


This bug report concerns a data validation issue with the Umee platform. The SetCollateralSetting method should ensure that the borrow limit will not drop below the amount borrowed, but the function uses an incorrect comparison, checking that the borrow limit will be greater than, not less than, that amount. This could allow an attacker to provide collateral, borrow coins, and then disable the use of the collateral asset; because of the incorrect comparison, the disable operation would succeed, and the collateral would be sent back to the attacker.

The short-term recommendation is to correct the comparison in the SetCollateralSetting method. The long-term recommendation is to implement tests to check whether basic functionality works as expected.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

## Target: umee/x/leverage

### Description
Umee users can send a `SetCollateral` message to disable the use of a certain asset as collateral. The messages are handled by the `SetCollateralSetting` method (Figure 11.1), which should ensure that the borrow limit will not drop below the amount borrowed. However, the function uses an incorrect comparison, checking that the borrow limit will be greater than, not less than, that amount.

```go
// Return error if borrow limit would drop below borrowed value
if newBorrowLimit.GT(borrowedValue) {
    return sdkerrors.Wrap(types.ErrBorrowLimitLow, newBorrowLimit.String())
}
```

**Figure 11.1:** The incorrect comparison in the `SetCollateralSetting` method (umee/x/leverage/keeper/keeper.go#343–346)

### Exploit Scenario
An attacker provides collateral to the Umee system and borrows some coins. Then the attacker disables the use of the collateral asset; because of the incorrect comparison in the `SetCollateralSetting` method, the disable operation succeeds, and the collateral is sent back to the attacker.

### Recommendations
- **Short term:** Correct the comparison in the `SetCollateralSetting` method.
- **Long term:** Implement tests to check whether basic functionality works as expected.

*Trail of Bits*

UMEE Security Assessment

PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Umee |
| Report Date | N/A |
| Finders | Paweł Płatek, Dominik Czarnota |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf

### Keywords for Search

`vulnerability`

