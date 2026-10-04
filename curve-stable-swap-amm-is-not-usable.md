---
# Core Classification
protocol: FIVA Yield Tokenization Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57087
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-FIVA-yieldtokenizationprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-FIVA-yieldtokenizationprotocol-securityreview.pdf
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
finders_count: 4
finders:
  - Tarun Bansal
  - Quan Nguyen
  - Nicolas Donboly
  - Coriolan Pinhas
---

## Vulnerability Title

Curve stable swap AMM is not usable

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Low

## Type: Undeﬁned Behavior

## Description
The `AMM/markets/curve_stable/math.fc` uses `CUBE_STABLE` as `SWAP_TYPE` instead of `CURVE_STABLE_SWAP`. The use of an incorrect swap type makes it unusable. The FIVA Pool contract uses the `SWAP_TYPE` constant to modify the contract storage usage for different types of automated market-making (AMM) mechanisms. The protocol supports the constant product, cube stable swap, and curve stable swap AMMs. Each AMM has its own directory in the markets directory with a `math.fc` file in it. These `math.fc` files contain the AMM-specific invariant and swap functions along with the `SWAP_TYPE` constant definition.

The `SWAP_TYPE` value is used in the `load_data` and `store_data` functions of the `storage.fc` file:

```plaintext
if (swap_type == CURVE_STABLE_SWAP) {
    storage::amplification_coefficient = ds~load_uint(8);
}
if (swap_type == CUBE_STABLE) {
    storage::sy_pt_price = ds~load_uint(32);
}
```

**Figure 7.1:** A snippet of the `load_data` function of the Pool contract  
`contracts/AMM/storage.fc#L83-L88`

However, the `math.fc` file of the curve stable swap has the `CUBE_STABLE` value for the `SWAP_TYPE` constant instead of the `CURVE_STABLE_SWAP`, as shown in the figure below:

```plaintext
const SWAP_TYPE = CUBE_STABLE;
```

**Figure 7.2:** The `SWAP_TYPE` constant definition  
`contracts/AMM/markets/curve_stable/math.fc#L6-L6`

The incorrect `SWAP_TYPE` value results in the `storage::amplification_coefficient` value not being assigned, which makes the curve stable swap AMM unusable because of division by zero in all of the functions of the `AMM/markets/curve_stable/math.fc` file. The curve stable swap AMM is deprecated; therefore, the severity of this issue has been downgraded to informational.

## Exploit Scenario
The FIVA administrator deploys a new curve stable pool by updating the `swaps.fc` to include the `curve_stable/math.fc` and using the curve stable pool configuration. However, the `SWAP_TYPE` constant remains incorrect in the `curve_stable/math.fc`, which makes the newly deployed pool unusable.

## Recommendations
- **Short term:** Update the `AMM/markets/curve_stable/math.fc` file to assign the `CURVE_STABLE_SWAP` value to the `SWAP_TYPE` constant.
- **Long term:** Improve the test suite to test all code paths and all contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | FIVA Yield Tokenization Protocol |
| Report Date | N/A |
| Finders | Tarun Bansal, Quan Nguyen, Nicolas Donboly, Coriolan Pinhas |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-FIVA-yieldtokenizationprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-FIVA-yieldtokenizationprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

