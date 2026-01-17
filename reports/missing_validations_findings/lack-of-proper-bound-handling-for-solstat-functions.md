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
solodit_id: 26792
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-primitive-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-primitive-securityreview.pdf
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
  - Robert Schneider
  - Kurt Willis
  - Nat Chin
---

## Vulnerability Title

Lack of proper bound handling for solstat functions

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Low

## Type: Undeﬁned Behavior

### Description
The use of unchecked assembly across the system combined with a lack of data validation means that obscure bugs that are diﬃcult to track down may be prevalent in the system. One example of unchecked assembly that could result in bugs is the `getY` function. Due to assembly rounding issues in the codebase, the inverse of the function’s two variables does not hold. This function uses targeted functions in the Gaussian code. We wrote a fuzz test and ran it on the `getY` function to ensure that the return values are monotonically decreasing. However, the fuzzing campaign found cases in which the `getY` function returns a lower value than it should:

#### Logs:
- Bound Result: 999999989999999997
- Bound Result: 10000000003
- Bound Result: 10000000000
- Bound Result: 10000000000
- Bound Result: 86400

**Error:** a <= b not satisfied [uint]  
**Value a:** 10000000000  
**Value b:** 99  

![Figure 22.1: Results of fuzz testing the getY function](image-link)

The `solstat` Gaussian contract contains the cumulative distribution function (cdf), which relies on the `erfc` function. The `erfc` function, however, has multiple issues, indicated by its many breaking invariants; for example, it is not monotonic, returns hard-coded values outside of its input domain, has inconsistent rounding directions, and is missing overflow protection (further described below). This means that the cdf function’s assumption that it always returns a maximum error of 1.2e-7 may not hold under all conditions.

```solidity
/**
 * @notice Approximation of the Cumulative Distribution Function.
 *
 * @dev Equal to `D(x) = 0.5[ 1 + erf((x - µ) / σ√2)]`.
 * Only computes cdf of a distribution with µ = 0 and σ = 1.
 *
 * @custom:error Maximum error of 1.2e-7.
 * @custom:source https://mathworld.wolfram.com/NormalDistribution.html.
 */
function cdf(int256 x) internal pure returns (int256 z) {
    int256 negated;
    assembly {
        let res := sdiv(mul(x, ONE), SQRT2)
        negated := add(not(res), 1)
    }
    int256 _erfc = erfc(negated);
    assembly {
        z := sdiv(mul(ONE, _erfc), TWO)
    }
}
```
![Figure 22.2: The cdf() function in Gaussian.sol](image-link)

The `erfc` function (and related functions) are used throughout the Hyper contract to compute the contract’s reserves, prices, and the invariants. This function contains a few issues, described below the figure.

```solidity
function erfc(int256 input) internal pure returns (int256 output) {
    uint256 z = abs(input);
    int256 t;
    int256 step;
    int256 k;
    assembly {
        let quo := sdiv(mul(z, ONE), TWO)
        let den := add(ONE, quo)
        t := sdiv(SCALAR_SQRD, den)
        // [...]
    }
}
```
![Figure 22.3: The erfc() function in Gaussian.sol](image-link)

### Lack of Overflow Checks
The `erfc` function does not contain overflow checks. In the above assembly block, the first multiplication operation does not check for overflow. Operations performed in an assembly block use unchecked arithmetic by default. If `z`, the absolute value of the input, is larger than ⌈type(int256).max / 1e18⌉ (rounded up), the multiplication operation will result in an overflow.

### Use of sdiv Instead of div
Additionally, the `erfc` function uses the `sdiv` function instead of the `div` function on the result of the multiplication operation. The `div` function should be used instead because `z` and the product are positive. Even if the result of the previous multiplication operation does not overflow, if the result is larger than type(int256).max, then it will be incorrectly interpreted as a negative number due to the use of `sdiv`.

Because of these issues, the output values could lie well beyond the intended output domain of the function, [0, 2]. For example, erfc(x) ≈ 1e57 is a possible output value. Other functions—and those that rely on `erfc`, such as `pdf`, `ierfc`, `cdf`, `ppf`, `getX`, and `getY`—are similarly affected and could produce unexpected results. Some of these issues are further outlined in appendix E.

Due to the high complexity and use of the function throughout this codebase, the exact implications of an incorrect bound on the function are unclear. We specify further areas that require investigation in appendix C; however, Primitive should conduct additional analysis on the precision loss and specificity of `solstat` functions.

### Exploit Scenario
An attacker sees that under a certain swap configuration, the output amount in Hyper’s swap function will result in a significant advantage for the attacker.

### Recommendations
Short term, rewrite all of the affected code in high-level Solidity with native overflow protection enabled.

Long term, set up sufficient invariant tests using Echidna that can detect these issues in the code. For all functions, perform thorough analysis on the valid input range, document all assumptions, and ensure that all functions revert if the assumptions on the inputs do not hold.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

