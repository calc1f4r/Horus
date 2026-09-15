---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6925
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
  - validation
  - swap

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

SwapManager assumes Morpho token is token0 of every token pair

### Overview


This bug report outlines a high risk issue in the SwapManagerUniV2.sol contract at line 106. This issue is in the consult function which wrongly assumes that the Morpho token is always the first token in theMorpho <> Reward token token pair. This could lead to inverted prices and a denial of service attack when claiming rewards as the wrongly calculated expected amount slippage check reverts.

The recommendation is to consider using similar code to the example UniswapV2 oracle. It is also noted that depending on how this issue is fixed in consult, the caller of this function needs to be adjusted to return a Morpho token amount as amountOut.

Morpho has fixed this issue in PR #585 and Spearbit has acknowledged this.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
`SwapManagerUniV2.sol#L106`

## Description
The `consult` function wrongly assumes that the Morpho token is always the first token (`token0`) in the Morpho <> Reward token token pair. This could lead to inverted prices and a denial of service attack when claiming rewards, as the wrongly calculated expected amount slippage check reverts.

## Recommendation
Consider using similar code to the example UniswapV2 oracle. Note that depending on how this issue is fixed in `consult`, the caller of this function needs to be adjusted as well to return a Morpho token amount as `amountOut`.

## Morpho
Fixed in PR #585.

## Spearbit
Acknowledged.

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

`Validation, Swap`

