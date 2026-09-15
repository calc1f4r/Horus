---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18279
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Partial fills for buy orders in ERC1155 swaps will fail when pair has insufficient balance

### Overview


This bug report is about the VeryFastRouter, a component of the Ethereum blockchain. The problem is that partial fills are currently supported for buy orders in VeryFastRouter.swap(), but when the function _findMaxFillableAmtForBuy() determines the number of items to fill, it is not guaranteed that the underlying pair has so many items left to fill. This leads to an early revert, which defeats the purpose of the swap() function.

The recommendation is to check for the number of items to fill against the pair balance, and use the smaller of the two for partial filling. This means that the amount of NFTs to transfer should be the minimum of numItemsToFill and erc1155.balanceOf(pair).

The issue has been fixed after the review started as part of PR#26, which has been verified.

### Original Finding Content

## High Risk Severity Issue

## Context
VeryFastRouter.sol#L189-L198

## Description
Partial fills are currently supported for buy orders in `VeryFastRouter.swap()`. When `_findMaxFillableAmtForBuy()` determines `numItemsToFill`, it is not guaranteed that the underlying pair has so many items left to fill. 

While ERC721 swap handles the scenario where pair balance is less than `numItemsToFill` in the logic of `_findAvailableIds()` (maxIdsNeeded vs numIdsFound), ERC1155 swap is missing a similar check and reduction of item numbers when required.

Partial fills for buy orders in ERC1155 swaps will fail when the pair has a balance less than `numItemsToFill` as determined by `_findMaxFillableAmtForBuy()`. Partial filling, a key feature of `VeryFastRouter`, will then not work as expected and would lead to an early revert, which defeats the purpose of `swap()`.

## Recommendation
Check for `numItemsToFill` against pair balance and use the smaller of the two for partial filling, i.e. calculate `min(numItemsToFill, erc1155.balanceOf(pair))` as the amount of NFTs to transfer.

## Sudorandom Labs
This has been fixed after the review started as part of PR#26.

## Spearbit
Verified that this is fixed by PR#26.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

