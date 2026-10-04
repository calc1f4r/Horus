---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21171
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
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
finders_count: 0
finders:
---

## Vulnerability Title

[L-03] `LybraEUSDVaultBase.superLiquidation()`: Confusing code comments deviates from function logic

### Overview

See description below for full details.

### Original Finding Content


### Impact
```solidity
/**
    * @notice When overallCollateralRatio is below badCollateralRatio, borrowers with collateralRatio below 125% could be fully liquidated.
    * Emits a `LiquidationRecord` event.
    *
    * Requirements:
    * - Current overallCollateralRatio should be below badCollateralRatio
    * - `onBehalfOf`collateralRatio should be below 125%
    * @dev After Liquidation, borrower's debt is reduced by collateralAmount * etherPrice, deposit is reduced by collateralAmount * borrower's collateralRatio. Keeper gets a liquidation reward of `keeperRatio / borrower's collateralRatio
    */
function superLiquidation(address provider, address onBehalfOf, uint256 assetAmount) external virtual {
    uint256 assetPrice = getAssetPrice();
    require((totalDepositedAsset * assetPrice * 100) / poolTotalEUSDCirculation < badCollateralRatio, "overallCollateralRatio should below 150%");
    uint256 onBehalfOfCollateralRatio = (depositedAsset[onBehalfOf] * assetPrice * 100) / borrowed[onBehalfOf];
    require(onBehalfOfCollateralRatio < 125 * 1e18, "borrowers collateralRatio should below 125%");
    require(assetAmount <= depositedAsset[onBehalfOf], "total of collateral can be liquidated at most");
    uint256 eusdAmount = (assetAmount * assetPrice) / 1e18;
    if (onBehalfOfCollateralRatio >= 1e20) {
        eusdAmount = (eusdAmount * 1e20) / onBehalfOfCollateralRatio;
    }
    require(EUSD.allowance(provider, address(this)) >= eusdAmount, "provider should authorize to provide liquidation EUSD");

    _repay(provider, onBehalfOf, eusdAmount);

    totalDepositedAsset -= assetAmount;
    depositedAsset[onBehalfOf] -= assetAmount;
    uint256 reward2keeper;
    if (msg.sender != provider && onBehalfOfCollateralRatio >= 1e20 + configurator.vaultKeeperRatio(address(this)) * 1e18) {
        reward2keeper = ((assetAmount * configurator.vaultKeeperRatio(address(this))) * 1e18) / onBehalfOfCollateralRatio;
        collateralAsset.transfer(msg.sender, reward2keeper);
    }
    collateralAsset.transfer(provider, assetAmount - reward2keeper);

    emit LiquidationRecord(provider, msg.sender, onBehalfOf, eusdAmount, assetAmount, reward2keeper, true, block.timestamp);
}
```

In code comments of `superLiquidation()`, it is mentioned that deposit of borrower (collateral) will be reduced by collateral amount * borrower's collateral ratio. This is inaccurate, as the goal of `superLiquidation()` is to allow possible complete liquidation of borrower's collateral; hence, `totalDepositAsset` is simply subtracted by `assetAmount`.  

### Recommendation
Adjust code comments to follow function logic.

## Non-Critical



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`vulnerability`

