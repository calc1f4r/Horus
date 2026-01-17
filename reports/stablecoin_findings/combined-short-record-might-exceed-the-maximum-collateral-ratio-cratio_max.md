---
# Core Classification
protocol: DittoETH
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27459
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc
source_link: none
github_link: https://github.com/Cyfrin/2023-09-ditto

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - caventa
  - happyformerlawyer
  - T1MOH
---

## Vulnerability Title

Combined short record might exceed the maximum collateral ratio (CRATIO_MAX)

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-09-ditto/blob/main/contracts/facets/ShortRecordFacet.sol#L117-L189">https://github.com/Cyfrin/2023-09-ditto/blob/main/contracts/facets/ShortRecordFacet.sol#L117-L189</a>


## Summary
The combined short record might exceed the maximum collateral ratio (CRATIO_MAX).

## Vulnerability Details
The collateral of a short record can be increased in two distinct manners:

1. Boosting collateral (Refer to ShortRecordFacet#increaseCollateral)
2. Merging short records (Refer to ShortRecordFacet#combineShorts)

While there's a cap in place for CR in the first method, ensuring it doesn't surpass CRATIO_MAX, the same restriction is absent in the second method.

## Impact
A short record formed via the merging of other short records might result in a CR that surpasses the CRATIO_MAX limit.

## Tools Used
Manual

## Recommendations
Add the subsequent validation to ShortRecordFacet#combineShorts

```solidity
if (cRatio >= Constants.CRATIO_MAX) revert Errors.CollateralHigherThanMax();
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | DittoETH |
| Report Date | N/A |
| Finders | caventa, happyformerlawyer, T1MOH |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-09-ditto
- **Contest**: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc

### Keywords for Search

`vulnerability`

