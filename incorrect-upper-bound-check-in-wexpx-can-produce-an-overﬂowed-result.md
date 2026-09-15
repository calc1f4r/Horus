---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54432
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/2c9a9dc9-d39d-4018-a61b-d7b43619180e
source_link: https://cdn.cantina.xyz/reports/cantina_morpho_blue_irm_oct2023.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Saw-mon and Natalie
  - Jonah Wu
  - StErMi
---

## Vulnerability Title

Incorrect upper bound check in wExp(x) can produce an overﬂowed result 

### Overview


The bug report is about an issue in a function called `wExp(x)` in the `MathLib.sol` code. The problem is that the upper bound used in this function is not strict enough, which can cause an overflow. The report suggests that the upper bound should be calculated in a similar way to another function called `FixedPointMathLib`. The report also provides some calculations and values for the upper bound, as well as a test case that shows the problem. The recommendation is to update the upper bound limit check to avoid the overflow issue. The bug has been fixed in a pull request (PR). 

### Original Finding Content

## Context: MathLib.sol#L26

## Description
Upper-bound used in `wExp(x)` is not restrict enough:

```solidity
// Revert if x > ln(2^256-1) ~ 177.
require(x <= 177.44567822334599921 ether, ErrorsLib.WEXP_OVERFLOW);
```

As this function accepts `x` in the 18 decimal format and is supposed to return an 18 decimal number, the upper bound should be calculated similarly to Remco's `FixedPointMathLib`:

\[
10^{18} e^{x + \epsilon} \leq 10^{18} e^{x + \epsilon} 10^{18} \leq 2^{256} - 1
\]

So:

\[
x \leq \frac{10^{18} \ln(2^{256} - 1)}{10^{18}} - \epsilon
\]

Here \(\epsilon = \text{LN2\_INT}\).

And so the upper bound would be approximately:

\[
135.305999368893231588 \text{ ether}:
\]

\[
135.305999368893231588 \cdot 10^{18} = \frac{10^{18} \ln(2^{256} - 1)}{10^{18}} - 10^{18} \ln(2)
\]

This is a rough estimate as the actual implementation uses the 2nd order Taylor expansion of the `exp` function. A less strict upper bound would be:

\[
135.652572959173204244 \text{ ether}.
\]

Using binary search, one can find the exact value for the upper bound (below the unit is ether):

- \(136.549994570309225873 < 197 \cdot \text{LN2}\) - overflows
- \(135.999582271169154766\) overflows
- \(135.999582271169154765\) does not overflow
- \(135.856847389749280564 < 196 \cdot \text{LN2}\)
- \(135.652572959173204244\) approximate (\(\epsilon \text{LN2\_HALF}\))
- \(135.305999368893231589\) Remco's limit
- \(135.305999368893231588\) approximate (\(\epsilon \text{LN2}\))

## Test Case for MathLibTest.sol
```solidity
function testWExpSpecial() public {
    console2.log("e(x0): ", MathLib.wExp(135.999582271169154765 ether));
    console2.log("e(x1): ", MathLib.wExp(135.999582271169154766 ether));
    console2.log("e(x2): ", MathLib.wExp(135.999582271169154767 ether));
}
```

### Logs (note that `x0 < x1 < x2`):
- `e(x0): 115792089237316195323137357242501015631897353894317901381819896896488577433600`
- `e(x1): 0`
- `e(x2): 100433627766186892221372630771322662657637687111424552206336`

## Recommendation
Update the upper bound limit check to a value to avoid the overflow issues. If a specific value is chosen, document why and produce a proof that overflows would not happen for the values below that limit. One can use one of the approximate values from above to be more conservative or a rounded bound \(196 \cdot \text{LN2}\).

Note the exact bounds are implementation-dependent, but the more approximate ones should work for all implementations as long as the `wExp` returns a smaller value compared to the expected one.

## Morpho
Fixed in PR 62.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Jonah Wu, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_morpho_blue_irm_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/2c9a9dc9-d39d-4018-a61b-d7b43619180e

### Keywords for Search

`vulnerability`

