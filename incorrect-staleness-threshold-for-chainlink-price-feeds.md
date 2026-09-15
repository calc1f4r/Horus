---
# Core Classification
protocol: Copra
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37582
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-23-Copra.md
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
  - Zokyo
---

## Vulnerability Title

Incorrect Staleness Threshold for Chainlink Price Feeds

### Overview


This bug report discusses an issue with the current implementation of a contract called GammaSwapLiquidityWarehouse.sol. The contract uses a single constant to determine the freshness of price feeds from Chainlink, a decentralized oracle network. However, this approach is problematic because different price feeds have different heartbeat intervals, which can lead to two critical issues. Firstly, for feeds with shorter heartbeats, the current implementation can use outdated prices for up to 23 hours longer than intended, potentially causing financial losses. Secondly, for feeds with longer heartbeats, the current threshold may incorrectly flag fresh prices as stale, causing unnecessary service interruptions. This issue was highlighted in a real-world incident when the Chainlink ETH/USD price feed experienced a 6-hour delay, potentially leading to financial losses or incorrect contract executions. The report recommends implementing a token-specific staleness threshold system and provides code examples for how to do so. It also suggests setting appropriate thresholds for each asset based on the specific Chainlink feed's heartbeat interval. The report includes a reference to the Chainlink documentation for more information on price feed contract addresses and heartbeats. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Location**: GammaSwapLiquidityWarehouse.sol

**Description**

The current implementation uses a single `STALENESS_THRESHOLD` constant (24 hours) for all Chainlink price feeds. This approach is problematic because different price feeds have vastly different heartbeat intervals. For example, the ETH/USD feed has a heartbeat of 1 hour, while the AMPL/USD feed has a heartbeat of 48 hours.
Using a single threshold for all feeds can lead to two critical issues:
- For feeds with shorter heartbeats (e.g., ETH/USD), the current implementation allows prices to be considered fresh for up to 23 hours longer than intended. This could result in the use of severely outdated prices, potentially causing significant financial losses.
- For feeds with longer heartbeats (e.g., AMPL/USD), the current threshold might incorrectly flag fresh prices as stale, potentially causing unnecessary service interruptions.
- A real-world incident highlighting the risks of this approach occurred when the Chainlink ETH/USD price feed experienced a 6-hour delay. In such scenarios, using outdated prices could lead to substantial financial losses or incorrect contract executions. https://cryptobriefing.com/chainlink-experiences-6-hour-delay-eth-price-feed/
- 
The current implementation in the `_getAssetOraclePrice` function uses a single `STALENESS_THRESHOLD`:
```solidity
if (block.timestamp - updatedAt > STALENESS_THRESHOLD) revert ChainlinkPriceFeedStale();
```
This check does not account for the varying heartbeat intervals of different price feeds.

**Recommendation**

Implement a token-specific staleness threshold system: Replace the single `STALENESS_THRESHOLD` constant with a mapping that stores individual staleness thresholds for each token:
```solidity
mapping(address => uint256) private s_stalenessTresholds;
```
Modify the `_getAssetOraclePrice` function to use the token-specific threshold:
```solidity
function _getAssetOraclePrice(address asset) internal view returns (uint256) {
    AggregatorV3Interface priceFeed = s_assetConfigs[asset].chainlinkPriceFeed;
    (, int256 oraclePrice,, uint256 updatedAt,) = priceFeed.latestRoundData();
    if (block.timestamp - updatedAt > s_stalenessTresholds[asset]) revert ChainlinkPriceFeedStale();
    // ... rest of the function
}
```
Implement a function to set and update staleness thresholds for each asset:
```solidity
function setStalnessThreshold(address asset, uint256 threshold) external onlyRole(DEFAULT_ADMIN_ROLE) {
    s_stalenessTresholds[asset] = threshold;
}
```

When adding new assets or updating configurations, ensure that appropriate staleness thresholds are set based on the specific Chainlink feed's heartbeat interval. It's recommended to set the threshold slightly higher than the heartbeat to account for minor delays, but not so high as to accept severely outdated prices.

**Reference**

Price Feed Contract Addresses | Chainlink Documentation - click on Show more details for heartbeats

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Copra |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-23-Copra.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

