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
solodit_id: 16219
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - EBaizel
  - JayJonah8
  - Christoph Michel
  - Datapunk
  - Emanuele Ricci
---

## Vulnerability Title

Isolated assets are treated as collateral in Morpho

### Overview


This bug report is related to Aave-v3, which introduced isolation assets and isolation mode for users. The Morpho contract is intended not to be in isolation mode to avoid its restrictions. However, Morpho will still set these isolated assets as collateral for the supplying user and this should not be possible. As isolated assets are riskier when used as collateral and should only allow borrowing up to a specific debt ceiling, this could potentially put the system at risk of liquidation on Aave.

The current code assumes that a supplied asset is always set as collateral on Aave whenever a supplyCollateral action with its _POOL.supplyToPool call succeeds. As such, the recommendation is to either reject isolated assets for supplyCollateral calls or check that the supplied asset is indeed set as collateral on Aave after the _POOL.supplyToPool(underlying, amount) call.

Morpho addressed the issue with PR 569 and Spearbit fixed the issue. More information on edge cases and how to handle them can be found on the related website.

### Original Finding Content

## Severity: Critical Risk

## Context
- `aave-v3/SupplyLogic.sol#L78`
- `aave-v3/ValidationLogic.sol#L711`
- `aave-v3/UserConfiguration.sol#L194`
- `PositionsManagerInternal.sol#L408`

## Description
Aave-v3 introduced isolation assets and isolation mode for users:
> "Borrowers supplying an isolated asset as collateral cannot supply other assets as collateral (though they can still supply to capture yield). Only stablecoins that have been permitted by Aave governance to be borrowable in isolation mode can be borrowed by users utilizing isolated collateral up to a specified debt ceiling."

The Morpho contract is intended not to be in isolation mode to avoid its restrictions. Supplying an isolated asset to Aave while there are already other (non-isolated) assets set as collateral will simply supply the asset to earn yield without setting it as collateral. However, Morpho will still set these isolated assets as collateral for the supplying user. Morpho users can borrow any asset against them, which should not be possible:
- Isolated assets are by definition riskier when used as collateral and should only allow borrowing up to a specific debt ceiling.
- The borrows are not backed on Aave as the isolated asset is not treated as collateral there, lowering the Morpho Aave position's health factor and putting the system at risk of liquidation on Aave.

## Recommendation
The current code assumes that a supplied asset is always set as collateral on Aave whenever a `supplyCollateral` action with its `_POOL.supplyToPool` call succeeds. 

In addition to Morpho can end up in isolation mode which ensures that the system does not end up in isolation mode, reject isolated assets for `supplyCollateral` calls. Alternatively, check that the supplied asset is indeed set as collateral on Aave after the `_POOL.supplyToPool(underlying, amount)` call.

## Morpho: 
Addressed with PR 569.

More information on edge cases and how we would handle can be found [here](link-to-more-information).

## Spearbit: 
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | EBaizel, JayJonah8, Christoph Michel, Datapunk, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Av3-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

