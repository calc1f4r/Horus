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
solodit_id: 16221
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

RewardsManager does not take in account users that have supplied collateral directly to the pool

### Overview


This bug report is about a high-risk issue in the RewardsManager.sol#L436 of the Morpho system. The system is not taking into account the amount of collateral that the user has supplied directly into the Aave pool when calculating the amount of supplied and borrowed balance for a user. As a result, the user is eligible for fewer rewards or even zero in the case where they have only supplied collateral. 

The recommendation given is that when asset is equal to market.aToken, userAssetBalances[i].balance should be equal to _MORPHO.scaledPoolSupplyBalance(market.underlying, user) + _MORPHO.scaledCollateralBalance(market.underlying, user). Morpho has implemented this recommendation in PR 587 and it has been fixed by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
`RewardsManager.sol#L436`

## Description
Inside `RewardsManager._getUserAssetBalances`, Morpho is calculating the amount of the supplied and borrowed balance for a specific user. In the current implementation, Morpho is ignoring the amount that the user has supplied as collateral directly into the Aave pool. As a consequence, the user will be eligible for fewer rewards or even zero in the case where he/she has supplied only collateral.

## Recommendation
When `asset == market.aToken`, `userAssetBalances[i].balance` should be equal to:
```solidity
_MORPHO.scaledPoolSupplyBalance(market.underlying, user) + _MORPHO.scaledCollateralBalance(market.underlying, user)
```

## Morpho
Recommendation implemented in PR 587.

## Spearbit
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

