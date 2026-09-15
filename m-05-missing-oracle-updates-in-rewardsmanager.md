---
# Core Classification
protocol: Level_2025-04-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63742
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Level-security-review_2025-04-09.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-05] Missing oracle updates in `RewardsManager`

### Overview


This bug report highlights an issue with the `RewardsManager.getAccruedYield()` function in the BoringDAO protocol. The function fails to update the oracle before fetching prices, which is different from the behavior in another contract. This means that outdated prices may be used in rewards calculations, and it is unclear when the oracle will be updated. To resolve this issue, the report recommends updating the oracle before retrieving prices, similar to how it is done in another contract. 

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `RewardsManager.getAccruedYield()` function calculates rewards based on oracle prices but fails to call `_tryUpdateOracle()` before fetching prices. This behavior is different from `LevelMintingV2`, which explicitly updates oracles before using their prices.
```solidity
    function getAccruedYield(address[] calldata assets) public view returns (uint256 accrued) {
        uint256 total;

        for (uint256 i = 0; i < assets.length; i++) {
            address asset = assets[i];
            StrategyConfig[] memory strategies = allStrategies[asset];
@>            uint256 totalForAsset = vault._getTotalAssets(strategies, asset);

            // ...
        }

        // ...
    }
```
As shown above, `getAccruedYield` calls `_getTotalAssets` for assets like `USDC` and `USDT` to compute the total assets controlled by `BoringVault`. This computation virtually converts all vault shares from lending strategies into their underlying assets.
```solidity
    function _getTotalAssets(BoringVault vault, StrategyConfig[] memory strategies, address asset)
        internal
        view
        returns (uint256 total)
    {
        // Initialize to undeployed
        uint256 totalForAsset = ERC20(asset).balanceOf(address(vault));

        for (uint256 j = 0; j < strategies.length; j++) {
            StrategyConfig memory config = strategies[j];
@>            totalForAsset += StrategyLib.getAssets(config, address(vault));
        }

        return totalForAsset;
    }
```
To perform this conversion, `StrategyLib.getAssets` is used. It checks the number of shares held in each strategy and converts them to the underlying asset using oracle prices. However, as shown below, the call to update the oracle (required for share tokens like steakUSDC or any other using `ERC4626DelayedOracle`) is missing.
```solidity
    function getAssets(StrategyConfig memory config, address vault) internal view returns (uint256 assets_) {
        // ...

        uint256 shares = receiptToken.balanceOf(vault);

        uint256 sharesToAssetDecimals =
            shares.mulDivDown(10 ** ERC20(address(config.baseCollateral)).decimals(), 10 ** receiptToken.decimals());

@>        (int256 assetsForOneShare, uint256 decimals) = OracleLib.getPriceAndDecimals(address(config.oracle), 0);
        assets_ = uint256(assetsForOneShare).mulDivDown(sharesToAssetDecimals, 10 ** decimals);
        return assets_;
    }
```
The impact of this vulnerability is that stale prices may be used during each rewards calculation, and it’s unclear when `ERC4626DelayedOracle::update` will next be called to assign updated prices.

## Recommendations

To resolve this issue, ensure that the oracle is updated before price retrieval, similar to the approach used in `LevelMintingV2.sol`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Level_2025-04-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Level-security-review_2025-04-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

