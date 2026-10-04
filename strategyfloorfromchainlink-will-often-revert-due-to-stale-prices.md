---
# Core Classification
protocol: LOOKSRARE
chain: everychain
category: uncategorized
vulnerability_type: stale_price

# Attack Vector Details
attack_type: stale_price
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6970
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LooksRare-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LooksRare-Spearbit-Security-Review.pdf
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
  - stale_price

protocol_categories:
  - dexes
  - cdp
  - services
  - synthetics
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Riley Holterhus
  - Optimum
  - Maxime Viard
---

## Vulnerability Title

StrategyFloorFromChainlink will often revert due to stale prices

### Overview


This bug report is about the FloorFromChainlink strategy in the StrategyFloorFromChainlink.sol contract. Currently, the maxLatency of the strategy is restricted to 3600 seconds, but the mainnet floor price feeds have a heartbeat of 86400 seconds. As a result, the strategy often reverts with the PriceNotRecentEnough error, and users might miss out on exchanges they would have accepted. To solve this issue, the recommendation is to allow for a maxLatency value of 86400 instead of 3600. The bug has been fixed in PR 326 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
StrategyFloorFromChainlink.sol

## Description
The `FloorFromChainlink` strategy inherits from `BaseStrategyChainlinkPriceLatency`, so it can have a `maxLatency` of at most 3600 seconds. However, all of the Chainlink mainnet floor price feeds have a heartbeat of 86400 seconds (24 hours), which means the Chainlink strategies will revert with the `PriceNotRecentEnough` error quite often. At the time of writing, every single mainnet floor price feed has an `updateAt` timestamp well over 3600 seconds in the past, meaning the strategy would always revert for any mainnet price feed right now. 

This may have not been realized earlier because the Goerli floor price feeds do have a heartbeat of 3600, but the mainnet heartbeat is much less frequent. 

One of the consequences is that users might miss out on exchanges they would have accepted. For example, if a taker bid is interested in a maker ask with an ETH premium from the floor, in the likely scenario where the taker didn't log in within 1 hour of the last oracle update, the strategy will revert and the exchange won't happen even though both parties are willing. If the floor moves up again the taker might not be interested anymore. The maker will have lost out on making a premium from the floor, and the taker would have lost out on the exchange they were willing to make.

## Recommendation
For the `FloorFromChainlink` strategy, allow for a `maxLatency` value of 86400, instead of restricting it at 3600.

## LooksRare
Fixed in PR 326.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | LOOKSRARE |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Riley Holterhus, Optimum, Maxime Viard |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LooksRare-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LooksRare-Spearbit-Security-Review.pdf

### Keywords for Search

`Stale Price`

