---
# Core Classification
protocol: Overlay
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6880
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Overlay-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Overlay-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Mudit Gupta
  - Harikrishnan Mulackal
  - Gerard Persoon
---

## Vulnerability Title

Liquidation might fail

### Overview


This bug report is about the liquidate() function in the OverlayV1Market and Position smart contracts. This function checks if a position can be liquidated and uses maintenanceMarginFraction to determine if enough value is left. However, liquidationFeeRate is used to determine the fee paid to the liquidator which is not necessarily true that enough value is left for the fee. This is classified as high risk because liquidation is an essential functionality of Overlay. The recommendation is to also take into account liquidationFee to determine if a position can/should be liquidated. Overlay agreed that the liquidation fee in its current form is not as a percentage of the current notionalWithPnl() like trading fees are, which means that it won’t affect the ability to liquidate the position. They suggested to potentially change this and the bug was fixed in commit 082c6c7. Spearbit acknowledged this.

### Original Finding Content

## High Risk Vulnerability Report

## Severity
**High Risk**

## Context
- **Files**: 
  - `OverlayV1Market.sol#L345-L376`
  - `Position.sol#L221-L247`

## Description
The `liquidate()` function checks if a position can be liquidated and, through the `liquidatable()` function, uses `maintenanceMarginFraction` as a factor to determine if enough value is left. However, in the rest of the `liquidate()` function, `liquidationFeeRate` is used to determine the fee paid to the liquidator.

It is not necessarily true that enough value is left for the fee, as two different ways are used to calculate this, which means that positions might be liquidated unexpectedly. This is classified as high risk because liquidation is an essential functionality of Overlay.

```solidity
contract OverlayV1Market is IOverlayV1Market {
    function liquidate(address owner, uint256 positionId) external {
        ...
        require(pos.liquidatable(..., maintenanceMarginFraction), "OVLV1:!liquidatable");
        ...
        uint256 liquidationFee = value.mulDown(liquidationFeeRate);
        ...
        ovl.transfer(msg.sender, value - liquidationFee);
        ovl.transfer(IOverlayV1Factory(factory).feeRecipient(), liquidationFee);
    }
}

library Position {
    function liquidatable(..., uint256 maintenanceMarginFraction) ... {
        ...
        uint256 maintenanceMargin = posNotionalInitial.mulUp(maintenanceMarginFraction);
        can_ = val < maintenanceMargin;
    }
}
```

## Recommendation
Also take into account `liquidationFee` to determine if a position can/should be liquidated.

**Note**: The `build()` function also calls `liquidatable()`.

## Overlay Response
Agreed. The way the liquidation fee amount is calculated, it’s taken from the remaining maintenance margin once the `liquidate()` function is called (less any burn of margin as insurance). 

So the liquidation fee, in its current form, is not a percentage of the current `notionalWithPnl()` like trading fees are, which means that it won’t affect the ability to liquidate the position. We should potentially change this.

**Fixed in commit**: `082c6c7`.

## Spearbit Response
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Overlay |
| Report Date | N/A |
| Finders | Mudit Gupta, Harikrishnan Mulackal, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Overlay-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Overlay-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

