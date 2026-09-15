---
# Core Classification
protocol: Salty.IO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29619
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
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
  - Damilola Edwards
  - Richie Humphrey
---

## Vulnerability Title

Chainlink oracles could return stale price data

### Overview

See description below for full details.

### Original Finding Content

## Difficulty: Low

## Type: Data Validation

## Description
The `latestRoundData()` function from Chainlink oracles returns five values: `roundId`, `answer`, `startedAt`, `updatedAt`, and `answeredInRound`. The PriceConverter contract reads only the `answer` value and discards the rest. This can cause outdated prices to be used for token conversions.

```solidity
// Returns a Chainlink oracle price with 18 decimals (converted from
// Chainlink's 8 decimals).
// Returns zero on any type of failure.
function latestChainlinkPrice(address _chainlinkFeed) public view returns (uint256) {
    AggregatorV3Interface chainlinkFeed = AggregatorV3Interface(_chainlinkFeed);
    
    int256 price = 0;
    try chainlinkFeed.latestRoundData() returns (
        uint80, // _roundID
        int256 _price,
        uint256, // _startedAt
        uint256, // _timeStamp
        uint80 // _answeredInRound
    ) {
        price = _price;
    }
}
```

*Figure 10.1*: All returned data other than the answer value is ignored during the call to a Chainlink feed’s `latestRoundData` method.  
(src/price_feed/CoreChainlinkFeed.sol#L67–L71)

According to the Chainlink documentation, if the `latestRoundData()` function is used, the `updatedAt` value should be checked to ensure that the returned value is recent enough for the application.

## Recommendations
- **Short term:** Make sure that the oracle queries check for up-to-date data. In the case of stale oracle data, have the `latestRoundData()` function return zero to indicate failure.
- **Long term:** Review the documentation for Chainlink and other oracle integrations to ensure that all of the security requirements are met to avoid potential issues, and add tests that take these possible situations into account.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Salty.IO |
| Report Date | N/A |
| Finders | Damilola Edwards, Richie Humphrey |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf

### Keywords for Search

`vulnerability`

