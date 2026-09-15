---
# Core Classification
protocol: Compound Open Price Feed – Uniswap Integration Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11384
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-open-price-feed-uniswap-integration-audit/
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M02] Inconsistent behavior when anchor price is zero

### Overview


This bug report is about the UniswapAnchoredView contract, which enables reporters to submit prices for an asset via the postPrices function. The submitted price can only deviate to a certain extent from the asset's anchor price, which is calculated as a time-weighted average price based on the corresponding Uniswap V2 market for the asset.

The problem is that if the anchor price is zero, it will be impossible for the reporter to match the anchor price and effectively set the asset’s price to zero, as the reporter’s price must be greater than zero to be considered within the anchor. However, if the reporter is invalidated, the UniswapAnchoredView does not take into account the reporter's price, and the asset's price can effectively be set to zero without any restrictions.

The bug report suggests that a single behavior should be defined for the oracle when the anchor price is zero, so that asset prices of zero are allowed or disallowed regardless of whether the reporter has been invalidated or not.

### Original Finding Content

The assigned reporter for the `UniswapAnchoredView` contract is expected to submit prices via its [`postPrices` function](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L135). This price can only deviate [to a certain extent](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L172) from the asset’s anchor price, calculated as a time-weighted average price based on the corresponding Uniswap V2 market for the asset.


Should the anchor price be zero, it will be impossible for the reporter to match the anchor price and effectively set the asset’s price to zero. This is due to the fact the reporter’s [price must be greater than zero](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L173) to be considered within the anchor – a check that is always done as long as the reporter is not invalidated.


When a reporter is invalidated (after executing the [`invalidateReporter` function](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L258)), the `UniswapAnchoredView` no longer takes into account prices submitted by the former reporter account, and considers the price from Uniswap as the “official” price for the asset. In this case, [if the anchor price is zero and the reporter has been invalidated](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L160-L162), the asset’s price can effectively be set to zero without any restrictions.


To favor consistency, consider defining a single behavior for the oracle when the anchor prize is zero. In particular, the oracle should allow (or disallow) asset prices of zero regardless of whether the reporter has been invalidated or not.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Open Price Feed – Uniswap Integration Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-open-price-feed-uniswap-integration-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

