---
# Core Classification
protocol: Morpho
chain: everychain
category: arithmetic
vulnerability_type: precision_loss

# Attack Vector Details
attack_type: precision_loss
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6937
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
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
  - precision_loss

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

Initial SwapManager cumulative prices values are wrong

### Overview


This bug report is about a medium risk issue found in the SwapManagerUniV2.sol code. The issue is that the initial cumulative price values are being calculated as integer divisions of unscaled reserves and not UQ112x112 fixed-point values. This means that one of the values will almost always be zero and when the difference is taken to the real currentCumulativePrices inupdate, the TWAP (time-weighted average price) will be a large, wrong value. As a result, the slippage checks will not work correctly.

The recommended solution is to use the same code as the UniswapV2 example oracle. This was acknowledged by Spearbit and fixed in PR #550 by Morpho.

### Original Finding Content

## Medium Risk Severity Report

## Context
- **File:** SwapManagerUniV2.sol
- **Lines:** 65-66

## Description
The initial cumulative price values are integer divisions of unscaled reserves and not UQ112x112 fixed-point values.

```solidity
(reserve0, reserve1, blockTimestampLast) = pair.getReserves();
price0CumulativeLast = reserve1 / reserve0;
price1CumulativeLast = reserve0 / reserve1;
```

One of these values will (almost) always be zero due to integer division. Then, when the difference is taken to the real `currentCumulativePrices` in `update`, the TWAP will be a large, wrong value. The slippage checks will not work correctly.

## Recommendation
Consider using the same code as the UniswapV2 example oracle.

## Morpho
Fixed in PR #550.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

`Precision Loss`

