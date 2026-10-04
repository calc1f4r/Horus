---
# Core Classification
protocol: AladdinDAO f(x) Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31032
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
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
  - Troy Sargent
  - Robert Schneider
---

## Vulnerability Title

Time-weighted Chainlink oracle can report inaccurate price

### Overview


This bug report discusses a medium difficulty issue with data validation in the Chainlink oracle used to price Ethereum in USD. The report explains that the time-weighted average price used can lead to inaccurate pricing during times of high volatility, which can result in bad debt and potential losses for users. The report also outlines a potential exploit scenario where a user takes advantage of the price discrepancy to make a profit. The report recommends short-term solutions to remove reliance on the time-weighted average price for liquidations and long-term solutions to adhere to best practices for oracle solutions and ensure safety checks are in place. 

### Original Finding Content

## Diﬃculty: Medium

## Type: Data Validation

### Target: 
contracts/price-oracle/twap/ChainlinkTwapOracleV3.sol

## Description
The Chainlink oracle used to price the value of ETH in USD is subject to a time-weighted average price that will over-represent or under-represent the true price in times of swift volatility. This can increase the likelihood of bad debt if a sudden price change is not acted on due to the lag, and it is too late once the collateral’s loss in value is reflected in the TWAP price.

```solidity
function _fetchPrice() internal view returns (CachedPrice memory _cached) {
    _cached.ETH_USDPrice = ITwapOracle(chainlinkETHTwapOracle).getTwap(block.timestamp);
    _cached.frxETH_ETHPrice = ICurvePoolOracle(curvePool).ema_price();
    _cached.frxETH_USDPrice = (_cached.ETH_USDPrice * _cached.frxETH_ETHPrice) / PRECISION;
}
```
Figure 6.1: Use of TWAP computed from Chainlink feed (aladdin-v3-contracts/contracts/f(x)/oracle/FxFrxETHTwapOracle.sol#85–89)

## Exploit Scenario
The price of Ethereum jumps 10% over the course of 10 minutes. Eve notices the price discrepancy between the actual price and the reported price, and takes out a 4x long position on the frxETH pool. Once the time-weighted average price of ETH catches up to the actual price, Eve cashes out her long position for a profit.

## Recommendations
- Short term, remove the reliance on a time-weighted average price, at least for liquidations. It is best to be punitive when pricing debt and conservative when valuing collateral, so the TWAP may be appropriate for minting.
- Long term, adhere to best practices for oracle solutions and ensure backup oracles and safety checks do not create credit risk.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | AladdinDAO f(x) Protocol |
| Report Date | N/A |
| Finders | Troy Sargent, Robert Schneider |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

