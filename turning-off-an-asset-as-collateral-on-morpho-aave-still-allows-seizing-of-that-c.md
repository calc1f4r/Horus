---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6912
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

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

Turning off an asset as collateral on Morpho-Aave still allows seizing of that collateral on Morpho and leads to liquidations

### Overview


This bug report is about the Morpho Aave deployment. The issue is that the feature to prevent liquidators from seizing an asset as collateral does not extend to users on Morpho. This means that when the asset is turned off as collateral, users on Morpho suddenly lose this asset as collateral and will be liquidated. The recommendation is to clarify when this feature is supposed to be used, taking into consideration the mentioned issues. It is also recommended to reconsider if the feature is required. The bug has been fixed in PR 1542 and verified.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
- [MorphoGovernance.sol#L407](https://github.com/aave-v2/MorphoGovernance.sol#L407)
- [MorphoUtils.sol#L285](https://github.com/aave-v2/MorphoUtils.sol#L285)

## Description
The Morpho Aave deployment can set the asset to not be used as collateral for Aave's Morpho contract position. On Aave, this prevents liquidators from seizing this asset as collateral.

1. However, this prevention does not extend to users on Morpho as Morpho has not implemented this check. Liquidations are performed through a repay & withdraw combination, and withdrawing the asset on Aave is still allowed.
2. When turning off the asset as collateral, the single Morpho contract position on Aave might still be over-collateralized, but some users on Morpho suddenly lose this asset as collateral (LTV becomes 0) and will be liquidated.

## Recommendation
The feature does not work well with the current version of the Morpho Aave contracts. It must be enabled right from the beginning and may not be set later when users are already borrowing against the asset as collateral on Morpho. Clarify when this feature is supposed to be used, taking into consideration the mentioned issues. Reconsider if it's required.

**Morpho:** Fixed in PR 1542.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | EBaizel, JayJonah8, Christoph Michel, Datapunk, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

