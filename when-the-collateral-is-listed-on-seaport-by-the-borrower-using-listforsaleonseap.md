---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7322
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
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
  - validation

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

When the collateral is listed on SeaPort by the borrower using listForSaleOnSeaport , when settled the liquidation fee will be sent to address(0)

### Overview


This bug report is about the LienToken.sol#L472-L477 code, which is of medium risk. When the collateral is listed on SeaPort by the borrower, the liquidator (s.auctionData in general) will not be set and thus the liquidatorPayment will be sent to address(0). This could cause an issue as the liquidation fee will be sent to address(0). To fix this, it is recommended that before calculating and transferring the liquidation fee, the liquidator should be checked to make sure it is not address(0). This issue was fixed in PR 206 and verified by Spearbit.

### Original Finding Content

## Security Assessment Report

## Severity
**Medium Risk**

## Context
LienToken.sol#L472-L477

## Description
When the collateral is listed on SeaPort by the borrower using `listForSaleOnSeaport`, `s.auctionData[collateralId].liquidator` (and `s.auctionData` in general) will not be set and will default to `address(0)`. Consequently, the `liquidatorPayment` will be sent to `address(0)`.

## Recommendation
Before calculating and transferring the liquidation fee, make sure that the liquidator is not `address(0)`.

## Astaria
Fixed in PR 206.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

