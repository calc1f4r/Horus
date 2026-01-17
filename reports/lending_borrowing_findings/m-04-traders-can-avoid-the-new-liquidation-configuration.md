---
# Core Classification
protocol: GainsNetwork-security-July2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58125
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-July2.md
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

[M-04] Traders can avoid the new liquidation configuration

### Overview


This bug report discusses a new update that introduces group liquidation parameters for trading. These parameters allow traders to adjust their liquidation thresholds based on their leverage, making their positions more sensitive to price changes and more prone to liquidation. However, there is a bug in the code that allows traders to exploit this new feature. When users update their position size or leverage, the code will always use the initial liquidation parameters, even if the trade was created before the update. This means that traders can create low-risk trades before the update and then adjust their position size or leverage afterward to avoid the new liquidation threshold calculation and use the previously fixed legacy threshold. To fix this bug, the code should be updated to apply the new liquidation configuration when updating trades, even if they are from legacy trades. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The new update introduces group liquidation parameters, where liquidation thresholds are now configurable and depend on leverage. Higher leverage results in lower liquidation thresholds, making positions more sensitive to price changes and more prone to liquidation.

```solidity
    function getLiqPnlThresholdP(
        IPairsStorage.GroupLiquidationParams memory _params,
        uint256 _leverage
    ) public pure returns (uint256) {
        // For trades opened before v9.2, use legacy liquidation threshold
        // LEGACY_LIQ_THRESHOLD_P = 90 * P_10; // -90% pnl
>>>     if (_params.maxLiqSpreadP == 0) return ConstantsUtils.LEGACY_LIQ_THRESHOLD_P;
        if (_leverage < _params.startLeverage) return _params.startLiqThresholdP;
        if (_leverage > _params.endLeverage) return _params.endLiqThresholdP;

        return
            _params.startLiqThresholdP -
            ((_leverage - _params.startLeverage) * (_params.startLiqThresholdP - _params.endLiqThresholdP)) /
            (_params.endLeverage - _params.startLeverage);
    }
```

When users update their position size or leverage, it will always use initial liquidation params, which means if the order is created before the update, it will always use legacy liquidation threshold.

```solidity
   // update leverage
    function _prepareCallbackValues(
        ITradingStorage.Trade memory _existingTrade,
        ITradingStorage.Trade memory _pendingTrade,
        bool _isIncrease
    ) internal view returns (IUpdateLeverageUtils.UpdateLeverageValues memory values) {
        if (_existingTrade.isOpen == false) return values;

        values.newLeverage = _pendingTrade.leverage;
        values.govFeeCollateral = TradingCommonUtils.getGovFeeCollateral(
            _existingTrade.user,
            _existingTrade.pairIndex,
            TradingCommonUtils.getMinPositionSizeCollateral(_existingTrade.collateralIndex, _existingTrade.pairIndex) /
                2 // use min fee / 2
        );
        values.newCollateralAmount =
            (
                _isIncrease
                    ? _existingTrade.collateralAmount - _pendingTrade.collateralAmount
                    : _existingTrade.collateralAmount + _pendingTrade.collateralAmount
            ) -
            values.govFeeCollateral;
>>>     values.liqPrice = _getMultiCollatDiamond().getTradeLiquidationPrice(
            IBorrowingFees.LiqPriceInput(
                _existingTrade.collateralIndex,
                _existingTrade.user,
                _existingTrade.pairIndex,
                _existingTrade.index,
                _existingTrade.openPrice,
                _existingTrade.long,
                _isIncrease ? values.newCollateralAmount : _existingTrade.collateralAmount,
                _isIncrease ? values.newLeverage : _existingTrade.leverage,
                true
            )
        ); // for increase leverage we calculate new trade liquidation price and for decrease leverage we calculate existing trade liquidation price
    }
```

```solidity
// increase position size
    function prepareCallbackValues(
        ITradingStorage.Trade memory _existingTrade,
        ITradingStorage.Trade memory _partialTrade,
        ITradingCallbacks.AggregatorAnswer memory _answer
    ) internal view returns (IUpdatePositionSizeUtils.IncreasePositionSizeValues memory values) {
        // ...
        values.newOpenPrice =
            (positionSizePlusPnlCollateral *
                uint256(_existingTrade.openPrice) +
                values.positionSizeCollateralDelta *
                values.priceAfterImpact) /
            (positionSizePlusPnlCollateral + values.positionSizeCollateralDelta);

        // 8. Calculate existing and new liq price
        values.existingLiqPrice = TradingCommonUtils.getTradeLiquidationPrice(_existingTrade, true);
>>>     values.newLiqPrice = _getMultiCollatDiamond().getTradeLiquidationPrice(
            IBorrowingFees.LiqPriceInput(
                _existingTrade.collateralIndex,
                _existingTrade.user,
                _existingTrade.pairIndex,
                _existingTrade.index,
                uint64(values.newOpenPrice),
                _existingTrade.long,
                values.newCollateralAmount,
                values.newLeverage,
                false
            )
        );
    }
```

Traders can exploit this by creating small, low-risk trades before the update and then adjusting the position size or leverage afterward. By doing this, they can avoid the new liquidation threshold calculation that depends on leverage and use the previously fixed legacy threshold, which is more desirable for them.

## Recommendations

When users update trades and calculate the new liquidation price, update the trades and apply the liquidation configuration if they are from legacy trades.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GainsNetwork-security-July2 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-July2.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

