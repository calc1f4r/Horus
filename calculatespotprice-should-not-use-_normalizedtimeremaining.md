---
# Core Classification
protocol: Hyperdrive June 2023
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35858
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

calculateSpotPrice(...) should not use _normalizedTimeRemaining

### Overview


The report discusses a bug in the HyperdriveMath.sol code, specifically in the function calculateSpotPrice(). This function is used to calculate the spot price of bonds in terms of the base, but it is currently not working correctly. The bug results in the spot price being calculated with a wrong factor and the _normalizedTimeRemaining parameter not being used properly. This can lead to incorrect fee calculations for users. The report recommends changing the code to fix these issues and provides a suggested solution. The bug has been resolved in a recent pull request.

### Original Finding Content

## Medium Risk Issue Report

### Severity: Medium Risk

### Context
- **File:** HyperdriveMath.sol
- **Lines:** L17, L23, L24-L38

### Description
When one trades on the curve, the following share-bond curve is used (with fixed ts):
\[ c(z)^{1 - ts + y1 - ts} = k \]

If one calculates the spot price, which is the slope of the perpendicular line to the tangent of the curve at a point like (z, y), we would get:
\[ \frac{dz}{dy} = \frac{1}{c(z) y ts} \]

Instead, in `calculateSpotPrice(...)`, the spot price is calculated as:
\[ \frac{dz}{dy} = \frac{z}{y tr ts} \]

There are two issues where the first is more important:
1. The \( \text{cfactor} \) is not considered. This is due to a wrong NatSpec comment that mentions `calculateSpotPrice(...)` calculates the spot price without slippage of bonds in terms of shares, but it should be the spot price of bonds in terms of the base.
2. The variable `_normalizedTimeRemaining` does not have a concrete meaning since it is not used in the definition of the curve, but one can apply it to manipulate the price which will be used in fee calculations. However, those fee calculations should not consider the \( tr \) in the exponent when calculating fees for non-matured positions.

The spot price is recorded for oracles and is also used in LP and governance fee calculations.

### Recommendation
Based on the discussion with the client, `calculateSpotPrice(...)` should calculate (note the exponent term does not include \( tr \)):
\[ \frac{dx}{dy} = \frac{dx}{dz} \cdot \frac{dz}{dy} = \frac{z}{y ts} \]

As a user, we would probably want to query the average of \( \frac{dx}{dy} \) from the oracle before investing.

Thus, `calculateSpotPrice(...)` needs to be changed to:
```solidity
/// @dev Calculates the spot price without slippage of bonds in terms of base.
/// @param _shareReserves The pool's share reserves.
/// @param _bondReserves The pool's bond reserves.
/// @param _initialSharePrice The initial share price as an 18 fixed-point value.
/// @param _timeStretch The time stretch parameter as an 18 fixed-point value.
/// @return spotPrice The spot price of bonds in terms of base as an 18 fixed-point value.
function calculateSpotPrice(
    uint256 _shareReserves,
    uint256 _bondReserves,
    uint256 _initialSharePrice,
    uint256 _timeStretch
) internal pure returns (uint256 spotPrice) {
    // (y / (mu * z)) ** -ts
    // ((mu * z) / y) ** ts
    spotPrice = _initialSharePrice
        .mulDivDown(_shareReserves, _bondReserves)
        .pow(_timeStretch);
}
```

### Resolution
This issue was resolved in PR 396.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive June 2023 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf

### Keywords for Search

`vulnerability`

