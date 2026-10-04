---
# Core Classification
protocol: Tadle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38080
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clzcnh4o1000p11vucwtzgoro
source_link: none
github_link: https://github.com/Cyfrin/2024-08-tadle

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
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - eeyore
  - n3smaro
  - Tigerfrake
  - Waydou
---

## Vulnerability Title

Missing validation in `PreMarkets.abortBidTaker()` leading to funds lock.

### Overview

See description below for full details.

### Original Finding Content

## Summary

There is a missing validation in the `PreMarkets.abortBidTaker()` function that fails to check whether the offer is actually a `Bid` offer. Without this check, a user can call this function with their `Bid` stock of an `Ask` offer, which can lead to funds being locked if the collateral ratio is greater than 100%.

## Vulnerability Details

There are other issues that, when fixed, will reveal additional problems in the `PreMarkets.abortBidTaker()` function.

### Preconditions

1. The issue with `overinflated maker refund when collateral ratio is > 100%` in the `PreMarkets.abortAskOffer()` function is fixed. This issue was reported separately. Assume the function is working as expected.

```solidity
File: PreMarkets.sol
607:         uint256 totalDepositAmount = OfferLibraries.getDepositAmount(
608:             offerInfo.offerType,
609:             offerInfo.collateralRate,
610:             totalUsedAmount,
611:             false, // <== should be true
612:             Math.Rounding.Ceil
613:         );
```

2. The issue with `incorrect depositAmount calculation` in the `PreMarkets.abortBidTaker()` function is fixed. This issue was reported separately. Assume the calculation of the `depositAmount` value works as expected.

```solidity
File: PreMarkets.sol
671:         uint256 depositAmount = stockInfo.points.mulDiv(
672:             preOfferInfo.points, // <== incorrect; should be preOfferInfo.amount
673:             preOfferInfo.amount, // <== incorrect denominator; should be preOfferInfo.points
674:             Math.Rounding.Floor
675:         );
```

### Scenario

Given the above preconditions, consider the following scenario:

1. The maker creates an `Ask` offer for 50 points for 50 USDC, with a 200% collateral ratio, and deposits 100 USDC as collateral.
2. The taker accepts this `Ask` offer for 25 points for 25 USDC.
3. The maker aborts the `Ask` offer, retrieving 50 USDC of collateral and leaving 50 USDC as compensation for the taker.
4. The taker can now call `PreMarkets.abortBidTaker()`. Since the function does not check if the offer is a `Bid` offer, the taker can mistakenly call this function. The calculations for the `transferAmount` do not account for the collateral ratio, so the taker receives only 25 USDC. An additional 25 USDC that were used as collateral are locked in the contract and lost.

Although it is user error to call `PreMarkets.abortBidTaker()` instead of `DeliveryPlace.closeBidTaker()` (which would correctly refund 50 USDC), the end result is that the user loses funds, and they are locked in the system.

## Impact

- Funds are locked.

## Tools Used

- Manual review.

## Recommendations

Add validation in the `PreMarkets.abortBidTaker()` function to ensure the offer is a `Bid` offer before proceeding with execution.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Tadle |
| Report Date | N/A |
| Finders | eeyore, n3smaro, Tigerfrake, Waydou |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-08-tadle
- **Contest**: https://codehawks.cyfrin.io/c/clzcnh4o1000p11vucwtzgoro

### Keywords for Search

`vulnerability`

