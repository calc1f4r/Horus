---
# Core Classification
protocol: Marginswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3858
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-marginswap-contest
source_link: https://code4rena.com/reports/2021-04-marginswap
github_link: https://github.com/code-423n4/2021-04-marginswap-findings/issues/21

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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - indexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-03] Price feed can be manipulated

### Overview


This bug report outlines an issue with the `PriceAware.getCurrentPriceInPeg(token, inAmount, forceCurBlock=true)` function. This function is used to trigger an update to the price feed, but if the update window has passed, the price will be computed by simulating a Uniswap-like trade with the amounts. Unfortunately, this simulation can be manipulated using flash loans to yield almost arbitrary output amounts, and thus prices. 

This bug has the potential to cause serious issues, as wrong prices can break the core functionality of the contracts such as borrowing on margin, liquidations, etc.

To mitigate this issue, it is recommended to not use the Uniswap spot price as the real price and instead implement a Time-Weighted Average Price (TWAP) price oracle using the `price*CumulativeLast` variables. Uniswap itself warns against using the spot price and recommends implementing a TWAP price oracle instead.

The bug report was submitted by @cmichelio (mail@cmichel.io) with the Ethereum address 0x6823636c2462cfdcD8d33fE53fBCD0EdbE2752ad.

### Original Finding Content


Anyone can trigger an update to the price feed by calling `PriceAware.getCurrentPriceInPeg(token, inAmount, forceCurBlock=true)`.
If the update window has passed, the price will be computed by simulating a Uniswap-like trade with the amounts.
This simulation uses the reserves of the Uniswap pairs which can be changed drastically using flash loans to yield almost arbitrary output amounts, and thus prices. Wrong prices break the core functionality of the contracts such as borrowing on margin, liquidations, etc.

Recommend against using the Uniswap spot price as the real price. Uniswap itself warns against this and instead recommends implementing a [TWAP price oracle](https://uniswap.org/docs/v2/smart-contract-integration/building-an-oracle/) using the `price*CumulativeLast` variables.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Marginswap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-marginswap
- **GitHub**: https://github.com/code-423n4/2021-04-marginswap-findings/issues/21
- **Contest**: https://code4rena.com/contests/2021-04-marginswap-contest

### Keywords for Search

`vulnerability`

