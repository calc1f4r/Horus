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
solodit_id: 11385
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

[M03] Unexpected behavior when retrieving the underlying price of a cToken

### Overview


A bug has been discovered in the `getUnderlyingPrice` function of the `UniswapAnchoredView` contract. This function is intended to implement an interface defined in the `PriceOracle` contract of the Compound protocol. The interface states that it should return zero when the price is unavailable. However, the `getUnderlyingPrice` function of the `UniswapAnchoredView` contract will revert when there is no price registered in the Open Price Feed for the queried cToken address. 

This bug does not pose any security risk to the Open Price Feed, however, it is a deviation from the expected behavior of the interface. This can lead to unexpected errors when interacting with the oracle. Furthermore, the bug is not being tested in the contract’s test suite. It is necessary to include relevant unit tests to comprehensively specify the function’s expected behavior.

### Original Finding Content

The [`getUnderlyingPrice` function](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L123) of the `UniswapAnchoredView` contract intends to implement [the interface defined in the `PriceOracle` contract](https://github.com/compound-finance/compound-protocol/blob/7561dcf5964527dbf2f3c7cd670775b3c6f7e378/contracts/PriceOracle.sol#L15) of the Compound protocol. While the functions’ signatures correctly match, the implemented function does not behave as specified in the interface’s docstrings. In particular, the interface states that it [should return zero when the price is unavailable](https://github.com/compound-finance/compound-protocol/blob/7561dcf5964527dbf2f3c7cd670775b3c6f7e378/contracts/PriceOracle.sol#L13). However, the `getUnderlyingPrice` function of the `UniswapAnchoredView` contract will revert when there is no price registered in the Open Price Feed for the queried cToken address.


While this does not pose a security risk for the Open Price Feed, it is a deviation from the interface’s expected behavior, which can cause unexpected errors when interacting with the oracle. Moreover, it should be noted that this particular case is not being tested in [the contract’s test suite](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/tests/UniswapAnchoredViewTest.js#L123). Relevant unit tests are to be included to comprehensively specify the function’s expected behavior.

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

