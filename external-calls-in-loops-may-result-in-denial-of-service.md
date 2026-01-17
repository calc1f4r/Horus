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
solodit_id: 17896
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

External calls in loops may result in denial of service

### Overview

See description below for full details.

### Original Finding Content

## Documentation

**Type:** Documentation  
**Target:** veFXS.vy, CurveAMO_V3.sol  

**Difficulty:** Low  

## Description
The use of external calls in nested loops and subsequent loops, which iterate over lists that could have been provided by callers, may result in an out-of-gas failure during execution. To determine the total value of the collateral in the FRAX system, the code loops over all `frax_pools` to retrieve the collateral balance (in dollars):

```solidity
// Iterate through all frax pools and calculate all value of collateral in all pools globally
function globalCollateralValue() public view returns (uint256) {
    uint256 total_collateral_value_d18 = 0;
    for (uint i = 0; i < frax_pools_array.length; i++) {
        // Exclude null addresses
        if (frax_pools_array[i] != address(0)) {
            total_collateral_value_d18 =
            total_collateral_value_d18.add(FraxPool(frax_pools_array[i]).collatDollarBalance());
        }
    }
    return total_collateral_value_d18;
}
```

*Figure 16.1: contracts/Curve/CurveAMO_V3.sol#L256-L265*

This issue is also present in the following functions:
- `CurveAMO_V3.iterate()`
- `veFXS._checkpoint()`

## Exploit Scenario
Alice, a user, tries to retrieve the total balance of the collateral in the FRAX system. The execution runs out of gas during the computation, and an administrator must remove pools before the total collateral value can be determined.

## Recommendations
**Short term:** Develop documentation to inform users of what to do if a transaction fails because it has run out of gas.  

**Long term:** Investigate all loops used in the system to check whether they can run out of gas. Focus on determining whether the number of iterations performed by a single loop can increase over time or can be influenced by users.

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

