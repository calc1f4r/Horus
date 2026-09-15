---
# Core Classification
protocol: Primitive Hyper
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26776
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-primitive-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-primitive-securityreview.pdf
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
finders_count: 4
finders:
  - Tarun Bansal
  - Robert Schneider
  - Kurt Willis
  - Nat Chin
---

## Vulnerability Title

Swap function returns incorrectly scaled output token amount

### Overview


This bug report is about the swap function in Hyper.sol not scaling the output value by the pool's total liquidity. This means that users are not receiving the number of tokens they expect on swaps. Primitive discovered this issue during the code review. In order for Alice to receive the correct output token value, the swap function must be revised so that it multiplies the output token by the total liquidity present in the pool. Additionally, long-term, additional system invariants should be identified and fuzzed using Echidna to ensure that the functions return the expected values and that they are accurate.

### Original Finding Content

## Diﬃculty: Low

## Type: Undeﬁned Behavior

## Description

The swap function’s output value is given per unit of liquidity in the given pool, but it is not scaled by the pool’s total liquidity. As a result, users will not receive the number of tokens that they expect on swaps:

```solidity
function swap(
    uint64 poolId,
    bool sellAsset,
    uint amount,
    uint limit
) external lock interactions returns (uint output, uint remainder) {
```
*Figure 6.1: The function signature of the swap function in Hyper.sol*

The output token value is calculated using the difference between the `liveDependent` and `nextDependent` variables, both of which are calculated using the reserve amount of the input token. However, the output value is not multiplied by the total liquidity value of the pool, so the output amount is scaled incorrectly:

```solidity
_swap.output += (liveDependent - nextDependent);
```
*Figure 6.2: The output calculation in the _swapExactIn function in Hyper.sol*

This causes the number of output tokens to be either too few or too many, depending on the current amount of liquidity in the pool. Primitive also discovered this issue during the code review.

## Exploit Scenario

Alice swaps WETH for USDC using Hyper. The pool has less than 1 wad of liquidity. The token output value that is returned to Alice is less than what it should be.

## Recommendations

- **Short term**: Revise the swap function so that it multiplies the output token by the total liquidity present in the pool in which the swap takes place.
- **Long term**: Identify additional system invariants and fuzz them using Echidna to ensure that the functions return the expected values and that they are accurate.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Primitive Hyper |
| Report Date | N/A |
| Finders | Tarun Bansal, Robert Schneider, Kurt Willis, Nat Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-primitive-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-primitive-securityreview.pdf

### Keywords for Search

`vulnerability`

