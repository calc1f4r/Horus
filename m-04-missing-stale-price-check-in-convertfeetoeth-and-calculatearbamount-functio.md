---
# Core Classification
protocol: Pear V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44104
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Pear-v2-Security-Review.md
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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[M-04] Missing Stale Price Check in `convertFeeToEth()` and `calculateArbAmount()` Functions

### Overview


The bug report discusses an issue with the `convertFeeToEth()` and `calculateArbAmount()` functions in the `PlatformLogic.sol` and `RewardsClaimer.sol` files. These functions do not check if the price returned by the oracle is outdated. This means that the price used for converting fees from USD to Ether may be incorrect. The team recommends checking the return value of `ethUsdPrice` and `arbUsdPrice` and setting a maximum delay for retrieving data from Chainlink. The team has acknowledged the issue.

### Original Finding Content

## Severity

Medium Risk

## Description

The functions `convertFeeToEth()` in `PlatformLogic.sol` and `calculateArbAmount()` in `RewardsClaimer.sol` do not check if the price returned by the oracle is stale. We will give an example with `convertFeeToEth()`, but the same applies to the other function.

This is `convertFeeToEth()`:

```solidity
function convertFeeToEth(uint256 feeAmount) public view returns (uint256) {
    IChainLinkAggregator ethUsdAggregator =
        IChainLinkAggregator(comptroller.getEthUsdAggregator());
    (, int256 ethUsdPrice,,,) = ethUsdAggregator.latestRoundData();
// contain 8 decimals
    uint256 feeInEth = (feeAmount * 1e20) / uint256(ethUsdPrice);
    return feeInEth;
}
```

This function converts a fee amount denominated in USD to its equivalent value in Ether, based on the latest ETH/USD exchange rate provided by a Chainlink Aggregator.

According to Chainlink's [documentation](https://docs.chain.link/data-feeds/price-feeds/historical-data), this function does not error if no answer has been reached but returns 0 or outdated round data. So we need to check that `ethUsdPrice` is not 0.

The other problem is that there is no check for `Heartbeat`. This function fetches the current price of ETH in USD using Chainlink's ETH/USD feed, but there is no check for Heartbeat. Here as a reference, you can see that there should be a check every hour → [here](https://data.chain.link/feeds/ethereum/mainnet/eth-usd).

## Impact

If these checks are missing the price that is retrieved from the oracle may be outdated.

## Location of Affected Code

File: [src/PlatformLogic.sol#L486](https://github.com/pear-protocol/gmx-v2-core/blob/f3329d0474013d60d183a5773093b94a9e55caae/src/PlatformLogic.sol#L486)

File: [src/rewards/RewardsClaimer.sol#L414](https://github.com/pear-protocol/gmx-v2-core/blob/f3329d0474013d60d183a5773093b94a9e55caae/src/rewards/RewardsClaimer.sol#L414)

## Recommendation

You need to check the return value of `ethUsdPrice` and `arbUsdPrice` and the maximum delay accepted between answers from Chainlink.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Pear V2 |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Pear-v2-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

