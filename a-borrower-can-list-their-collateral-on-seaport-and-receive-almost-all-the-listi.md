---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7283
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
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
  - business_logic

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

A borrower can list their collateral on Seaport and receive almost all the listing price without paying back their liens

### Overview


This bug report is about a critical risk in the LienToken.sol code. When the collateral is listed on SeaPort by the borrower using listForSaleOnSeaport, the payment is sent to the borrower instead of the lending vaults. This means that the borrower can take/borrow liens by offering a collateral, list it on SeaPort, and keep the listing price minus the amount sent to the liquidator, without paying back the liens to the vaults. To fix this, the listing and liquidating logic was separated and the auction stack was set. The listForSaleOnSeaport endpoint was also removed as a fix.

### Original Finding Content

## Severity: Critical Risk

## Context
**File:** LienToken.sol#L480

## Description
When the collateral is listed on SeaPort by the borrower using `listForSaleOnSeaport`, `s.auctionData` is not populated. Thus, if that order gets fulfilled/matched and `ClearingHouse`'s fallback function gets called since `stack.length` is 0, this loop will not run and no payment is sent to the lending vaults. The rest of the payment is sent to the borrower. The collateral token and its related data get burnt/deleted by calling `settleAuction`. The lien tokens and the vaults remain untouched as though nothing has happened. 

So basically, a borrower can:
1. Take/borrow liens by offering collateral.
2. List their collateral on SeaPort through the `listForSaleOnSeaport` endpoint.
3. Once/if the SeaPort order fulfills/matches, the borrower would be paid the listing price minus the amount sent to the liquidator (`address(0)` in this case, which should be corrected).
4. Collateral token/data gets burnt/deleted.
5. Lien token data remains, and the loans are not paid back to the vaults.

As a result, the borrower could end up with all the loans they have taken plus the listing price from the SeaPort order. 

Note that when a user lists their own collateral on SeaPort, it seems that we intentionally do not kick off the auction process:
- Liens are continued.
- Collateral state hash is unchanged.
- Liquidator isn't set.
- Vaults aren't updated.
- Withdraw proxies aren't set, etc.

## Related Issue
Issue #88

## Recommendation
Be careful and pay attention that listing by a borrower versus auctioning by a liquidator takes separate return/payback paths. It is recommended to separate the listing and liquidating logic and ensure auction funds are distributed appropriately. Most importantly, the auction stack must be set.

## Astaria
We've removed the ability for self-listing on SeaPort as the fix for v0 and will add this feature in a future release.

## Spearbit
Fixed in the following PR by removing the `listForSaleOnSeaport` endpoint (PR 206).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`Business Logic`

