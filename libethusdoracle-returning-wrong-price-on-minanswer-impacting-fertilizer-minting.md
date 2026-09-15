---
# Core Classification
protocol: Beanstalk Part 1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31880
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clsxlpte900074r5et7x6kh96
source_link: none
github_link: https://github.com/Cyfrin/2024-02-Beanstalk-1

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
finders_count: 3
finders:
  - 0xBeastBoy
  - Igdbaxe
  - 0xTheBlackPanther
---

## Vulnerability Title

LibEthUsdOracle returning wrong price on `minAnswer`, impacting fertilizer minting

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-02-Beanstalk-1/blob/a3658861af8f5126224718af494d02352fbb3ea5/protocol/contracts/libraries/Oracle/LibEthUsdOracle.sol#L63-L101">https://github.com/Cyfrin/2024-02-Beanstalk-1/blob/a3658861af8f5126224718af494d02352fbb3ea5/protocol/contracts/libraries/Oracle/LibEthUsdOracle.sol#L63-L101</a>


## Summary
The Chainlink aggregator utilized in the `LibEthUsdOracle` contract lacks a mechanism to detect and handle scenarios where the price of an asset falls outside of a predetermined price band. This limitation can result in the oracle returning the `minPrice` instead of the actual price of the asset during extreme market events, such as a significant drop in value. Consequently, users may continue to interact with the system, such as minting fertilizer tokens, using inaccurate price data. <a href="https://rekt.news/venus-blizz-rekt/" target="_blank"> similar case happened with Venus on BSC when LUNA imploded </a>

More Refs for similar issues like this:
- https://medium.com/cyfrin/chainlink-oracle-defi-attacks-93b6cb6541bf ( check Oracle Returns Incorrect Price During Flash Crashes )
- https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/18
- https://github.com/sherlock-audit/2023-05-ironbank-judging/issues/25

## Impact

The Chainlink aggregator can lead to potential exploitation of price discrepancies during extreme market conditions. For instance, if the price of an asset experiences a sudden crash, the oracle may continue to provide the `minPrice`, allowing users to conduct transactions at incorrect prices. This could result in financial losses for users and undermine the integrity of the system.

In our scenario, the `mintFertilizer` function within the FertilizerFacet contract, although it falls out of our immediate scope, relies on the `LibEthUsdOracle.getEthUsdPrice()` function (within our scope) to fetch the ETH/USD price from the Chainlink oracle. This price is crucial for calculating the amount of Fertilizer tokens that can be acquired with the provided `wethAmountIn` of WETH. However, if this function returns the `minPrice` during extreme market events, it would not reflect the actual price of the asset. Consequently, users could continue to mint fertilizer tokens using this **inaccurate price data**, leading to transactions occurring at incorrect prices.

## Recommendation
It is recommended to enhance the Chainlink oracle (`LibEthUsdOracle`) by implementing a mechanism to check the returned answer against predefined `minPrice` and `maxPrice` bounds. If the answer falls outside of these bounds, the oracle should revert the transaction, indicating that the price data is not reliable due to market conditions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beanstalk Part 1 |
| Report Date | N/A |
| Finders | 0xBeastBoy, Igdbaxe, 0xTheBlackPanther |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-02-Beanstalk-1
- **Contest**: https://www.codehawks.com/contests/clsxlpte900074r5et7x6kh96

### Keywords for Search

`vulnerability`

