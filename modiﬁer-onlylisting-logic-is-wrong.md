---
# Core Classification
protocol: Kim Exchange
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46424
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/f4fbb598-ae17-4ef2-8290-864a0ab3d83e
source_link: https://cdn.cantina.xyz/reports/cantina_kim_exchange_november2024.pdf
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
finders_count: 2
finders:
  - cccz
  - Chinmay Farkya
---

## Vulnerability Title

Modiﬁer onlyListing() logic is wrong 

### Overview

See description below for full details.

### Original Finding Content

## KimNFTMarketplace Review

## Context
`KimNFTMarketplace.sol#L70-L74`

## Description
The `onlyListing()` modifier is used on all user interactions to validate that the input `listingID` actually exists. It does so by checking if the `listingID` is greater than the actual array elements in the `listings` array.

However, the current logic also considers `array index == listings.length` as a valid element, which cannot exist, as the array only has `length - 1` elements. This doesn't have much of an impact, as the purpose is only to return a nice error instead of a straight-up array out-of-bounds revert.

## Recommendation
Change the code to:

```solidity
modifier onlyListing(uint256 listingId) {
    if (listings.length == 0) revert InvalidListing();
    if (listingId >= listings.length) revert InvalidListing();
    _;
}
```

## KIM Exchange
Fixed in PR 8.

## Cantina Managed
The fix implements the recommendation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Kim Exchange |
| Report Date | N/A |
| Finders | cccz, Chinmay Farkya |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_kim_exchange_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/f4fbb598-ae17-4ef2-8290-864a0ab3d83e

### Keywords for Search

`vulnerability`

