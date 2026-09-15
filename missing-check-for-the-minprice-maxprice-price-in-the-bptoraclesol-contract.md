---
# Core Classification
protocol: OpalProtocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54313
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007
source_link: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xRizwan
  - Cheems
---

## Vulnerability Title

Missing check for the minprice /maxprice price in the bptoracle.sol contract 

### Overview


This report highlights two issues in the `BPTOracle.getUSDPrice` function. The first issue is that there is no check for negative or zero prices, which could lead to incorrect calculations. The second issue is that there is no check to ensure that the returned price is within a predetermined range, which could also result in incorrect prices being returned. These issues could potentially impact the protocol and it is recommended to add checks to avoid incorrect results.

### Original Finding Content

## Context

(No context files were provided by the reviewer)

## Issues in `BPTOracle.getUSDPrice`

### 1. Lack of Check for Negative or Zero Price

There is no check for negative or zero price returned by `priceFeed.latestRoundData()`, which could lead to underflow.

```solidity
function getUSDPrice(address token) public view returns (uint256 priceInUSD) {
    if (tokenHeartbeat[token] == 0) { revert HeartbeatNotSet(); }
    IOracle priceFeed = IPriceFeed(priceFeedAddress).getPriceFeedFromAsset(token);
    if (address(priceFeed) == address(0)) revert PriceFeedNotFound();
    // @audit there is no check for negative or zero price.
    (, int256 priceInUSDInt,, uint256 updatedAt,) = priceFeed.latestRoundData();
    if (updatedAt + tokenHeartbeat[token] < block.timestamp) revert StalePrice();
    
    // simulate negative price
    priceInUSDInt = -1;
    // Oracle answers are normalized to 8 decimals
    uint256 newPrice = _normalizeAmount(uint256(priceInUSDInt), 8);
    return newPrice;
}

// Test
function test_NegativePrice() public {
    uint256 amount = bptPrice.BptPriceStablePool(
        bytes32(0x06df3b2bbb68adc8b0e302443692037ed9f91b42000000000000000000000063)
    );
}
```

### 2. No Check for Min/Max Price Range

There is no check to ensure that the returned `priceInUSDInt` is between `minPrice` and `maxPrice`, which is recommended. Chainlink has a circuit breaker if the price of an asset goes outside of a predetermined price band (`minPrice`/`maxPrice`). 

For example, if an asset had a huge drop in value, it will continue to return the `minPrice` instead of the actual price. In this case, `getUSDPrice` will return the wrong price.

### Impact

If an asset drops in value, the wrong price will be returned and incorrect calculations will happen when using `getUSDPrice`, which will affect the protocol.

### Recommendation

Ensure that the returned `priceInUSDInt` is between `minPrice` and `maxPrice` to avoid results based on incorrect prices.

```solidity
function getUSDPrice(address token) public view returns (uint256 priceInUSD) {
    if (tokenHeartbeat[token] == 0) { revert HeartbeatNotSet(); }
    IOracle priceFeed = IPriceFeed(priceFeedAddress).getPriceFeedFromAsset(token);
    if (address(priceFeed) == address(0)) revert PriceFeedNotFound();
    (, int256 priceInUSDInt,, uint256 updatedAt,) = priceFeed.latestRoundData();
    if (updatedAt + tokenHeartbeat[token] < block.timestamp) revert StalePrice();
    
    + if (signedPrice < 0) revert negative_priceInUSDInt();
    + if (priceInUSDInt < minPrice) revert hit_minPrice();
    + if (priceInUSDInt > maxPrice) revert hit_maxPrice();
    
    // Oracle answers are normalized to 8 decimals
    uint256 newPrice = _normalizeAmount(uint256(priceInUSDInt), 8);
    return newPrice;
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OpalProtocol |
| Report Date | N/A |
| Finders | 0xRizwan, Cheems |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007

### Keywords for Search

`vulnerability`

