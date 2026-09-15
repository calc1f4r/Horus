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
solodit_id: 37589
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-23-Copra.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Unhandled Chainlink Oracle Access Revocation Risk

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Location**: GammaSwapLiquidityWarehouse.sol

**Description**

The `_getAssetOraclePrice` function in the `GammaLiquidityWarehouse` contract directly calls the `latestRoundData` function of Chainlink price feeds without proper error handling. This approach is vulnerable to potential access revocation by multisigs controlling the price feeds, which could lead to unexpected contract failures and denial of service.
Currently, the function makes two direct calls to `latestRoundData`:

For the asset price feed:

`(, int256 oraclePrice,, uint256 updatedAt,) = priceFeed.latestRoundData();`

For the sequencer uptime feed:

`(, int256 answer, uint256 startedAt,,) = i_sequencerUptimeFeed.latestRoundData();`

If access to these price feeds is revoked or blocked, these calls will revert, causing the entire function to fail. This could potentially render critical parts of the contract inoperable, as price information is essential for many DeFi operations.

**Recommendation**

Implement a try-catch mechanism for both `latestRoundData` calls to handle potential access revocations gracefully. This approach allows the contract to maintain control and implement appropriate fallback mechanisms or error handling.
Here's an example of how the function could be refactored:
```solidity
function _getAssetOraclePrice(address asset) internal view returns (uint256) {
    AggregatorV3Interface priceFeed = s_assetConfigs[asset].chainlinkPriceFeed;

    try priceFeed.latestRoundData() returns (
        uint80,
        int256 oraclePrice,
        uint256,
        uint256 updatedAt,
        uint80
    ) {
        if (block.timestamp - updatedAt > STALENESS_THRESHOLD) revert ChainlinkPriceFeedStale();

        try i_sequencerUptimeFeed.latestRoundData() returns (
            uint80,
            int256 answer,
            uint256 startedAt,
            uint256,
            uint80
        ) {
            if (answer == 1) {
                revert SequencerDown();
            }
            if (block.timestamp - startedAt <= GRACE_PERIOD_TIME) {
                revert GracePeriodNotOver();
            }
            return oraclePrice.toUint256() * 10 ** (18 - priceFeed.decimals());
        } catch {
            // Handle sequencer uptime feed failure
            // e.g., revert with a custom error, use a fallback mechanism, etc.
            revert SequencerUptimeFeedFailure();
        }
    } catch {
        // Handle price feed failure
        // e.g., revert with a custom error, use a fallback oracle, etc.
        revert PriceFeedAccessRevoked();
    }
}
```
This refactored version wraps both `latestRoundData` calls in `try-catch` blocks. If either call fails due to access revocation or other issues, the contract can handle the error gracefully, either by reverting with a specific error message or implementing alternative logic (such as using a fallback oracle).

**Reference**

Smart Contract Security Guidelines #3: The Dangers of Price Oracles - OpenZeppelin blog

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

