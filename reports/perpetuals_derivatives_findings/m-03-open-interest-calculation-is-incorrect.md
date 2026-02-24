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
solodit_id: 36425
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

protocol_categories:
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Open interest calculation is incorrect

### Overview


This bug report describes an issue with the open interest delta calculation in a trading system. This calculation is incorrect when a position is opened and closed multiple times, leading to incorrect removal of open interest. The recommendation is to track the total open interest of a position and adjust it when the position is closed.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

The open interest (OI) delta is calculated using the `current collateral/USD` price when `adding OI`. Conversely, when `removing OI`, the delta is calculated using the `collateral/USD price at the time the OI was added`. This method works correctly if an order is only opened and closed once. However, if the order position is increased or decreased multiple times, the OI calculation becomes incorrect.

For example, if a position is opened when the collateral price is $100 and then increased when the price is $110, the OI to be removed upon closing is incorrectly calculated using the $110 price.

```solidity
    function handleOiDelta(
        ITradingStorage.Trade memory _trade,
        ITradingStorage.TradeInfo memory _tradeInfo,
        uint256 _newPositionSizeCollateral
    ) external {
        uint256 existingPositionSizeCollateral = getPositionSizeCollateral(_trade.collateralAmount, _trade.leverage);

        if (_newPositionSizeCollateral > existingPositionSizeCollateral) {
            addOiCollateral(_trade, _newPositionSizeCollateral - existingPositionSizeCollateral); // @audit using current collateral/usd price
        } else if (_newPositionSizeCollateral < existingPositionSizeCollateral) {
            removeOiCollateral(_trade, _tradeInfo, existingPositionSizeCollateral - _newPositionSizeCollateral); // @audit using the collateral/usd price when the OI was added last time
        }
    }
```

**Recommendations**

Track the total open interest of a position and adjust the open interest based on the maximum total open interest when the position is closed.

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

`vulnerability`

