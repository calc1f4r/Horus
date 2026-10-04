---
# Core Classification
protocol: Gainsnetwork May
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36423
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-May.md
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
  - liquidation

protocol_categories:
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Incorrect calculation of new liquidation price

### Overview


This bug report describes an issue with the function `prepareCallbackValues` in the code. The function is used to calculate the new liquidation price for trading positions. However, the current implementation can lead to incorrect liquidation prices, causing unexpected errors when validating the callback. This is because the function uses `newCollateralAmount` and `newLeverage` as inputs, which can result in overstating the borrowing fee. To fix this issue, it is recommended to pass the current borrowing fee instead of recalculating it with `newCollateralAmount` and `newLeverage`. 

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

When calculating the newLiqPrice in `IncreasePositionSizeUtils.prepareCallbackValues`, the function uses `newCollateralAmount` and `newLeverage`.

```solidity
  function prepareCallbackValues(
        ITradingStorage.Trade memory _existingTrade,
        ITradingStorage.Trade memory _partialTrade,
        ITradingCallbacks.AggregatorAnswer memory _answer
    ) internal view returns (IUpdatePositionSizeUtils.IncreasePositionSizeValues memory values) {
        ...
        values.newLiqPrice = _getMultiCollatDiamond().getTradeLiquidationPrice(
            IBorrowingFees.LiqPriceInput(
                _existingTrade.collateralIndex,
                _existingTrade.user,
                _existingTrade.pairIndex,
                _existingTrade.index,
                uint64(values.newOpenPrice),
                _existingTrade.long,
                values.newCollateralAmount, // @audit use newCollateralAmount & newLeverage => borrowing fee is overstated
                values.newLeverage
            )
        );
        ...
    }
```

To calculate the liquidation price, the current borrowing fee amount needs to be considered. Using `newCollateralAmount` and `newLeverage` as inputs can lead to overstating the borrowing fee if these values are higher than the current collateral and leverage. This results in an incorrect new liquidation price, making it higher for long positions and lower for short positions. This miscalculation can cause unexpected reverts when validating the callback due to the liquidation price being incorrectly calculated as reached.

```solidity
    function getTradeBorrowingFee(
        IBorrowingFees.BorrowingFeeInput memory _input
    ) internal view returns (uint256 feeAmountCollateral) {
        ...

        feeAmountCollateral = (_input.collateral * _input.leverage * borrowingFeeP) / 1e3 / ConstantsUtils.P_10 / 100; // collateral precision
    }
```

**Recommendations**

Pass the current borrowing fee to calculate the new liquidation price instead of recalculating the borrowing fee with `newCollateralAmount` and `newLeverage`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Gainsnetwork May |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-May.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Liquidation`

