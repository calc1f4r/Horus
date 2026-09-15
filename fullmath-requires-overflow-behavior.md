---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: overflow/underflow

# Attack Vector Details
attack_type: overflow/underflow
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6922
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
  - overflow/underflow
  - solc_version

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

FullMath requires overflow behavior

### Overview


This bug report is about the UniswapV3’s FullMath.sol, which is copied and migrated from an old solidity version to version 0.8. This migration caused the code to revert on overflows when it should not, breaking the SwapManagerUniV3 contract. The severity of this bug is rated as high risk.

The recommendation for this bug is to use the official FullMath.sol 0.8 branch that wraps the code in an unchecked statement. The bug has been fixed with the Uniswap V3 branch added as a dependency in the PR #550.

### Original Finding Content

## Security Audit Summary

## Severity
**High Risk**

## Context
`FullMath.sol#L2`

## Description
UniswapV3’s `FullMath.sol` is copied and migrated from an old solidity version to version 0.8, which reverts on overflows. However, the old `FullMath` relies on implicit overflow behavior. The current code will revert on overflows when it should not, which breaks the `SwapManagerUniV3` contract.

## Recommendation
Use the official `FullMath.sol` 0.8 branch that wraps the code in an unchecked statement. See #40.

## Spearbit
Fixed. The Uniswap V3 branch is added as a dependency in PR #550.

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

`Overflow/Underflow, SOLC Version`

