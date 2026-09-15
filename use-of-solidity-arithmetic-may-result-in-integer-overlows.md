---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17898
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Use of Solidity arithmetic may result in integer over�lows

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** CurveAMO_V3.sol  

**Difficulty:** Medium  

## Description
The `showAllocations()` function returns an array of values, one of which is calculated from the sum of `usdc_subtotal` (which is a `uint256`) and another integer expression. The two values are added using the `+` operator, which performs native Solidity integer addition without checking for overflows. As such, if the sum is too large a value, it will cause a wraparound, which could lead to unexpected behavior.

```solidity
return [
    frax_in_contract,   // [0]
    frax_withdrawable,  // [1]
    frax_withdrawable.add(frax_in_contract),   // [2]
    usdc_in_contract,   // [3]
    usdc_withdrawable,  // [4]
    usdc_subtotal,      // [5]
    usdc_subtotal + 
    (frax_in_contract.add(frax_withdrawable)).mul(fraxDiscountRate()).div(1e6 * (10 ** missing_decimals)),   // [6] USDC Total
    lp_owned,           // [7]
    frax3crv_supply,    // [8]
    _3pool_withdrawable, // [9]
    lp_value_in_vault   // [10]
];
```

_Figure 18.1: contracts/Curve/CurveAMO_V3.sol#L223-L235_

## Recommendations
**Short term:** Either use `SafeMath` (that is, `usdc_subtotal.add(...)`) to cause a revert in the case of a failure or document the reason that native integer addition is used.  

**Long term:** Use `Echidna` or `Manticore` to detect arithmetic overflows/underflows in the code.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

