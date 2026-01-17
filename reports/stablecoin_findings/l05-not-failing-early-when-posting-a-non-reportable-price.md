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
solodit_id: 11391
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-open-price-feed-uniswap-integration-audit/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L05] Not failing early when posting a non-reportable price

### Overview

See description below for full details.

### Original Finding Content

The `UniswapAnchoredView` contract expects most prices to be posted by the assigned reporter via the [`postPrices` function](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L135). Some assets prices (such as SAI, USDC or USDT) are not to be reported but rather remain fixed (either in ETH or US dollars) since construction. Assets whose prices are reported are tied to a Uniswap market address used to fetch anchor prices, while those that are not to be reported [are not associated with any market](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L92).


The `postPrices` function does not explicitly validate whether a received price is expected to be reported or not. As a consequence, it takes several operations until the transaction is effectively reverted. This ultimately occurs down the call chain when attempting to fetch the anchor price for the asset from a non-existing Uniswap market at the zero address in [line 45 of `UniswapLib.sol`](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapLib.sol#L45).


For added readability and explicitness, consider validating that posted prices via the `postPrices` are indeed expected to be reported.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

