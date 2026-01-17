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
solodit_id: 6924
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
rarity_score: 4

# Context Tags
tags:
  - wrong_math
  - protocol_reserve

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

Wrong reserve factor computation on P2P rates

### Overview


This bug report is about a high-risk issue in the MarketsManagerForAave.sol code. The reserve factor is used on the entire P2P supply and borrow rates instead of just on the spread of the pool rates. This causes overcharging for suppliers and borrowers and makes it possible to earn a worse rate on Morpho than the pool rates. The suggested fix for this issue is to update the formula to a + (1/2 +- f)(b-a) where f is the reserve factor. This bug has been acknowledged and fixed in PR #565.

### Original Finding Content

## Audit Report

## Severity
**High Risk**

## Context
`MarketsManagerForAave.sol#L413-L418`

## Description
The reserve factor is taken on the entire P2P supply and borrow rates instead of just on the spread of the pool rates. It’s currently overcharging suppliers and borrowers and making it possible to earn a worse rate on Morpho than the pool rates.

```solidity
supplyP2PSPY[_marketAddress] =
(meanSPY * (MAX_BASIS_POINTS - reserveFactor[_marketAddress])) /
MAX_BASIS_POINTS;

borrowP2PSPY[_marketAddress] =
(meanSPY * (MAX_BASIS_POINTS + reserveFactor[_marketAddress])) /
MAX_BASIS_POINTS;
```

## Recommendation
Fix the computation. The real reserve factor should apply only on the spread so you’re right that this formula is wrong and needs to be updated: 
`a + (1/2 ± f)(b-a)` where f is the reserve factor.

## Spearbit
Acknowledged, fixed in PR #565.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`Wrong Math, Protocol Reserve`

