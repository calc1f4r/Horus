---
# Core Classification
protocol: Euler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54214
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55
source_link: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Bauchibred
---

## Vulnerability Title

Protocol is going to ingest stale data for some Chainlink feeds 

### Overview

See description below for full details.

### Original Finding Content

## Chainlink Oracle Staleness Check Issue

## Context
`ChainlinkOracle.sol#L18`

## Description
The protocol integrates a lower and upper bound for their staleness checks when using Chainlink. However, a flawed assumption has been made regarding how low the heartbeat of a Chainlink feed can be, which causes the protocol to consistently ingest stale data for these feeds.

```solidity
uint256 internal constant MAX_STALENESS_LOWER_BOUND = 1 minutes;
```

The protocol assumes the minimum possible Chainlink price age to be 60 seconds. However, certain Chainlink oracles have a heartbeat of less than 60 seconds. These oracles are crucial for providing prices for the ERC20 tokens supported by this protocol. For example, the USDC/USD Chainlink oracle on Polygon has a heartbeat of 27 seconds, as indicated in the Trigger parameters section's information icon.

For Chainlink oracles with a heartbeat shorter than 60 seconds, the condition `block.timestamp - updatedAt > maxStaleness` in the `_getQuote()` function can return false even when the `updatedAt` timestamp reflects a stale price. For instance, if the `updatedAt` returned by the USDC/USD Chainlink oracle on Polygon is `block.timestamp - 27`, a newer price should have been reported at that timestamp. However, since `block.timestamp - updatedAt > maxStaleness` is false for such `updatedAt`, the `_getQuote` function does not trigger the error `Errors.PriceOracle_TooStale(staleness, maxStaleness)`. Consequently, the stale price is then used in the `_getQuote` function.

## Proof of Concept
Consider the code snippet from `ChainlinkOracle.sol#L41-L56`:

```solidity
constructor(address _base, address _quote, address _feed, uint256 _maxStaleness) {
    if (_maxStaleness < MAX_STALENESS_LOWER_BOUND || _maxStaleness > MAX_STALENESS_UPPER_BOUND) {
        revert Errors.PriceOracle_InvalidConfiguration();
    }
    base = _base;
    quote = _quote;
    feed = _feed;
    maxStaleness = _maxStaleness;
    // The scale factor is used to correctly convert decimals.
    uint8 baseDecimals = _getDecimals(base);
    uint8 quoteDecimals = _getDecimals(quote);
    uint8 feedDecimals = AggregatorV3Interface(feed).decimals();
    scale = ScaleUtils.calcScale(baseDecimals, quoteDecimals, feedDecimals);
}
```

## Recommendation
Remove the lower restriction on setting the staleness value. Since this function is admin-backed, we should trust that the correct value is set, allowing it to be appropriately set to less than a minute for feeds that require it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | Bauchibred |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

