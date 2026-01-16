---
# Core Classification
protocol: Gainsnetwork May
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36421
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-May.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] Overcharging of closing and trigger fees

### Overview


The bug report states that there is an issue with the calculation of closing and trigger fees in a trading system. Currently, a fixed 5% fee is being applied to all non-MARKET_CLOSE orders, but it should only be applied to LIQ_CLOSE orders. This is causing overcharging for TP_CLOSE and SL_CLOSE orders. The report recommends revising the fee calculation logic to apply the correct fees for each order type. 

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** High

**Description**

Currently, the calculation for closing and trigger fees applies a fixed `5%` fee to all `non-MARKET_CLOSE` orders. This fee should only apply to `LIQ_CLOSE` orders. For `TP_CLOSE` and `SL_CLOSE` orders, the calculation should use the pair close fee percentage and pair trigger order fee percentage, respectively. As a result, `TP_CLOSE` and `SL_CLOSE` orders are being overcharged.

```solidity
    function processClosingFees(
        ITradingStorage.Trade memory _trade,
        uint256 _positionSizeCollateral,
        ITradingStorage.PendingOrderType _orderType
    ) external returns (ITradingCallbacks.Values memory values) {
        // 1. Calculate closing fees
        values.positionSizeCollateral = getPositionSizeCollateralBasis(
            _trade.collateralIndex,
            _trade.pairIndex,
            _positionSizeCollateral
        ); // Charge fees on max(min position size, trade position size)

        values.closingFeeCollateral = _orderType == ITradingStorage.PendingOrderType.MARKET_CLOSE
            ? (values.positionSizeCollateral * _getMultiCollatDiamond().pairCloseFeeP(_trade.pairIndex)) /
                100 /
                ConstantsUtils.P_10
            : (_trade.collateralAmount * 5) / 100; // @audit charge fixed 5% for non-MARKET_CLOSE

        values.triggerFeeCollateral = _orderType == ITradingStorage.PendingOrderType.MARKET_CLOSE
            ? (values.positionSizeCollateral * _getMultiCollatDiamond().pairTriggerOrderFeeP(_trade.pairIndex)) /
                100 /
                ConstantsUtils.P_10
            : values.closingFeeCollateral; // @audit charge fixed 5% for non-MARKET_CLOSE
        ...
    }
```

**Recommendations**

Revise the fee calculation logic to apply the pair close fee percentage and pair trigger order fee percentage specifically for `TP_CLOSE` and `SL_CLOSE` orders, while retaining the 5% fee for `LIQ_CLOSE` orders.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
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

`vulnerability`

