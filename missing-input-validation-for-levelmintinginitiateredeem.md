---
# Core Classification
protocol: Level  Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42052
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/99c7abab-0ff5-4e0e-a796-b1294271ca25
source_link: https://cdn.cantina.xyz/reports/cantina_level_money_sep2024.pdf
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
  - Delvir0
  - tchkvsky
  - MiloTruck
  - xiaoming90
---

## Vulnerability Title

Missing input validation for LevelMinting.initiateRedeem() 

### Overview

See description below for full details.

### Original Finding Content

## Issue Summary: LevelMinting.sol#L277-L295

## Description
The `LevelMinting.initiateRedeem()` function only checks that `order.order_type` is `Order-Type.REDEEM`. There are no other checks for the fields in the order struct. As such, users can initiate redemption with:

1. `order.collateral_asset` as an asset not in `supportedAssets`. This allows them to initiate redemption for a collateral that will be added in the future, or they might accidentally initiate a redemption for a collateral asset that never gets added.
2. `order.lvlusd_amount` not equal to `order.collateral_amount`.

In both cases, the initiated redemption cannot be completed.

## Recommendation
Consider adding the following checks:

1. Add a `supportedAssets.contains(collateral_asset)` check to `initiateRedeem()`.
2. Move the `checkCollateralAndlvlUSDAmountEquality()` check from `completeRedeem()` to `initiateRedeem()`.

This prevents users from accidentally initiating a redemption that cannot be completed.

## Level Money
- Fixed in commit `5afc1851`.

## Cantina
The recommended checks were added to `initiateRedeem()`. However, since assets that were removed from `supportedAssets` should still be redeemable, `initiateRedeem()` should now check if `collateral_assets` is in `_redeemableAssets` instead.

## Level Money
- Fixed in commit `532771c9`.

## Cantina
Verified: assets removed from `supportedAssets` will now still be withdrawable through `initiateRedeem()`. To allow the protocol admin to make an asset non-withdrawable, `removeRedeemableAssets()` was added to remove assets from `_redeemableAssets`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Level  Money |
| Report Date | N/A |
| Finders | Delvir0, tchkvsky, MiloTruck, xiaoming90 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_level_money_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/99c7abab-0ff5-4e0e-a796-b1294271ca25

### Keywords for Search

`vulnerability`

