---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6919
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - wrong_math

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - hack3r-0m
  - Jay Jonah
  - Christoph Michel
  - Emanuele Ricci
---

## Vulnerability Title

Wrong P2P exchange rate calculation

### Overview


This bug report is regarding the MarketsManagerForAave.sol#L436. The issue is that _p2pDelta is divided by _poolIndex and multiplied by _p2pRate, which is incorrect. The correct order should be to multiply by _poolIndex and divide by _p2pRate to compute the correct share of the delta. This leads to wrong P2P rates throughout all markets if supply / borrow delta is involved.

The recommendation is to change the order and adjust the return values accordingly. The code should be changed to the following: uint256 shareOfTheDelta = _p2pDelta.wadToRay().rayMul(_poolIndex).rayDiv(_p2pRate).rayDiv(_p2pAmount.wadToRay());

Morpho has fixed this issue in PR #536, where _computeNewP2PExchangeRate is changed as recommended. Spearbit has acknowledged this.

### Original Finding Content

## Security Report

## Severity
**Critical Risk**

## Context
MarketsManagerForAave.sol#L436

## Description
`_p2pDelta` is divided by `_poolIndex` and multiplied by `_p2pRate`, nevertheless it should have been multiplied by `_poolIndex` and divided by `_p2pRate` to compute the correct share of the delta. This leads to wrong P2P rates throughout all markets if supply/borrow delta is involved.

## Recommendation
Change order and adjust return values accordingly.

```solidity
uint256 shareOfTheDelta = _p2pDelta
  .wadToRay()
  - .rayMul(_p2pRate)
  - .rayDiv(_poolIndex)
  + .rayMul(_poolIndex)
  + .rayDiv(_p2pRate)
  .rayDiv(_p2pAmount.wadToRay());
```

## Morpho
Fixed in PR #536, `_computeNewP2PExchangeRate` is changed as recommended.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`Wrong Math`

