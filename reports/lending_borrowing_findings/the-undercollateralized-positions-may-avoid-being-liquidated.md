---
# Core Classification
protocol: Narwhal Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37287
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal Finance.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

The undercollateralized positions may avoid being liquidated

### Overview


This bug report describes a critical issue with the stopTrade function in the Trading contract. This function is used to close undercollateralized positions, but it can be exploited by the position owner to delay the liquidation process indefinitely. This is because the function's check for the minimum acceptance delay can be bypassed by continuously updating the Take Profit and Stop Loss values of the position. The recommendation is to implement a separate tracking mechanism for the lastUpdateTime and to remove the condition for undercollateralized positions. The issue has been resolved.

### Original Finding Content

**Severity**: Critical

**Status**: Resolved

**Description**

The stopTrade function in the Trading contract is designed to be called for the liquidation of undercollateralized positions. This function verifies various conditions to ensure a trade can be legitimately closed. These include checking if the trade exists, ensuring compliance with the minimum acceptance delay, and confirming that the closing price has been reached. 
mo
Additionally, the stopTrade function includes a check
```solidity
require(ot.lastUpdateTime + minAcceptanceDelay <= block.timestamp,"wait");
```
which is intended to prevent the premature liquidation of a position. However, this mechanism can be exploited by the position owner.

The contract also includes an updateTPAndSL function, which allows the position owner to update the TP (Take Profit) and SL (Stop Loss) values of their open trades. 
Upon anticipating potential liquidation, the position owner can utilize the updateTPAndSL function to make slight adjustments to the TP/SL values. Each invocation of this function updates the lastUpdateTime of the open trade. Consequently, the owner can continually front-run the liquidation order and advance the lastUpdateTime, effectively preventing the execution of the stopTrade function due to the minAcceptanceDelay condition. This loophole allows the position owner to indefinitely delay the liquidation of an undercollateralized position.

**Recommendation**: 

Consider introducing a separate tracking mechanism for the lastUpdateTime that is only affected by market-related changes, not by TP/SL updates. 
Omit the lastUpdateTime condition if the transaction is intended to liquidate an undercollateralized position.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Narwhal Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

