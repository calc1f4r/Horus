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
solodit_id: 36419
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-May.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
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

[H-01] `FeeTierPoints` is incorrectly increased twice

### Overview


A bug has been discovered in the execution of the position size increase feature. This bug results in the trader fee tier points being updated twice, causing the trader to receive double the points. This can be exploited by traders to earn more points and get fee reduction quicker, which can lead to a loss in fee revenue for the protocol, vault users, and stakers. The bug can be resolved by removing the redundant update of fee tier points.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** High

**Description**

The execution of the position size increase will call `TradingCommonUtils.updateFeeTierPoints()` to update the trader fee tier points by the position size delta.

However, the trader fee tier points have been updated in the preceding call `TradingCommonUtils.processOpeningFees()`.

That means the trader fee tier points are incorrectly updated twice, causing the trader to receive double the points. A trader can exploit this to earn more points and get fee reduction quicker, causing protocol, vault users, and stakers to incur a loss in fee revenue.

```Solidity
    function executeIncreasePositionSizeMarket(
        ITradingStorage.PendingOrder memory _order,
        ITradingCallbacks.AggregatorAnswer memory _answer
    ) external {
            ...
            // 5. If passes further validation, execute callback
            if (cancelReason == ITradingCallbacks.CancelReason.NONE) {
                // 5.1 Update trade collateral / leverage / open price in storage, and reset trade borrowing fees
                IncreasePositionSizeUtils.updateTradeSuccess(existingTrade, values);

                // 5.2 Distribute opening fees
                //@audit this will update trader fee tier points for the increase of position size
                TradingCommonUtils.processOpeningFees(
                    existingTrade,
                    values.positionSizeCollateralDelta,
                    _order.orderType
                );

                // 5.3 Store trader fee tier points for position size delta
                //@audit this will incorrectly update trader fee tier points again
                TradingCommonUtils.updateFeeTierPoints(
                    existingTrade.collateralIndex,
                    existingTrade.user,
                    existingTrade.pairIndex,
                    values.positionSizeCollateralDelta
                );
            }
        }

        ;;;
    }
```

**Recommendations**

This can be resolved by removing the redundant update of fee tier points.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`vulnerability`

