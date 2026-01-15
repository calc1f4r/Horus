---
# Core Classification
protocol: Maple Finance v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17415
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-maplefinance-mapleprotocolv2-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-maplefinance-mapleprotocolv2-securityreview.pdf
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Simone Monica
  - Robert Schneider
---

## Vulnerability Title

Partially incorrect Chainlink price feed safety checks

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: High

## Type: Undeﬁned Behavior

## Description
The `getLatestPrice` function retrieves a specific asset price from Chainlink. However, the price (a signed integer) is first checked that it is non-zero and then is cast to an unsigned integer with a potentially negative value. An incorrect price would temporarily affect the expected amount of fund assets during liquidation.

```solidity
function getLatestPrice(address asset_) external override view returns (uint256 latestPrice_) {
    // If governor has overridden price because of oracle outage, return overridden price.
    if (manualOverridePrice[asset_] != 0) return manualOverridePrice[asset_];

    ( uint80 roundId_, int256 price_, , uint256 updatedAt_, uint80 answeredInRound_ ) =
    IChainlinkAggregatorV3Like(oracleFor[asset_]).latestRoundData();

    require(updatedAt_ != 0,              "MG:GLP:ROUND_NOT_COMPLETE");
    require(answeredInRound_ >= roundId_, "MG:GLP:STALE_DATA");
    require(price_ != int256(0),          "MG:GLP:ZERO_PRICE");
    latestPrice_ = uint256(price_);
}
```
*Figure 5.1: getLatestPrice function (globals-v2/contracts/MapleGlobals.sol#297-308)*

## Exploit Scenario
Chainlink’s oracle returns a negative value for an in-process liquidation. This value is then unsafely cast to a uint256. The expected amount of fund assets from the protocol is incorrect, which prevents liquidation.

## Recommendations
- **Short term**: Check that the price is greater than 0.
- **Long term**: Add tests for the Chainlink price feed with various edge cases. Additionally, set up a monitoring system in the event of unexpected market failures. A Chainlink oracle can have a minimum and maximum value, and if the real price is outside of that range, it will not be possible to update the oracle; as a result, it will report an incorrect price, and it will be impossible to know this on-chain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Maple Finance v2 |
| Report Date | N/A |
| Finders | Simone Monica, Robert Schneider |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-maplefinance-mapleprotocolv2-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-maplefinance-mapleprotocolv2-securityreview.pdf

### Keywords for Search

`vulnerability`

