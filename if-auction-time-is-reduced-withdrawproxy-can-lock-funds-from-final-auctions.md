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
solodit_id: 7313
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
rarity_score: 3

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

If auction time is reduced, withdrawProxy can lock funds from final auctions

### Overview


This bug report is about the WithdrawProxy.sol file, which is located at line 295. When a new liquidation occurs, the withdrawProxy sets s.finalAuctionEnd to be equal to the new incoming auction end. This would usually be fine, as new auctions start later than old auctions, and they all have the same length. However, if the auction time is reduced on the Router, it is possible for a new auction to have an end time that is sooner than an old auction. This would result in the WithdrawProxy being claimable before it should be, and then it will lock and not allow anyone to claim the funds from the final auction.

To fix this, the code should be replaced with a check like: uint40 auctionEnd = (block.timestamp + finalAuctionDelta).safeCastTo40(); if (auctionEnd > s.finalAuctionEnd) s.finalAuctionEnd = auctionEnd;. This was fixed by Astaria in commit 050487, and verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
WithdrawProxy.sol#L295

## Description
When a new liquidation happens, the `withdrawProxy` sets `s.finalAuctionEnd` to be equal to the new incoming auction end. This will usually be fine, because new auctions start later than old auctions, and they all have the same length. However, if the auction time is reduced on the Router, it is possible for a new auction to have an end time that is sooner than an old auction. The result will be that the WithdrawProxy is claimable before it should be, and then will lock and not allow anyone to claim the funds from the final auction.

## Recommendation
Replace this with a check like:
```solidity
uint40 auctionEnd = (block.timestamp + finalAuctionDelta).safeCastTo40();
if (auctionEnd > s.finalAuctionEnd) s.finalAuctionEnd = auctionEnd;
```

## Status
**Astaria:** Fixed in commit 050487.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
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

