---
# Core Classification
protocol: Lyra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18906
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
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
  - dexes
  - cdp
  - services
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-11 Decreasing a losing hedge position could make it overly-leveraged

### Overview


A bug has been discovered in GMXFuturesPoolHedger, where it is possible for the leverage ratio to be higher than intended when decreasing a position in order to be delta neutral. This occurs when the fees deducted from the collateral are greater than the collateral delta, causing the collateral delta to be zero-ed out. This increases the liquidation risk, which is not part of the Lyra risk model. It is recommended that a positionRouter.createIncreasePosition() call is made with the difference in deltas if adjustedDelta > collateralDelta holds. However, this recommendation will not be resolved as the risk is very temporary and there is no easy fix. Keepers will be able to follow up with an updateCollateral() request to increase the collateral if the hedger is over-leveraged after the decrease position request.

### Original Finding Content

**Description:**
It may be necessary to decrease a position in order to be delta neutral. When 
GMXFuturesPoolHedger does that, it also decreases the collateral so that the leverage ratio 
would equal the set **targetLeverage**. In GMX, fees are deducted from collateral when losses 
are realized. Therefore, the code takes into account that additional collateral needs to be sent, 
to make up for the fees deducted. It’s done in this block:
```solidity
      if (currentPos.unrealisedPnl < 0) {
          uint adjustedDelta = Math.abs(currentPos.unrealisedPnl).multiplyDecimal(sizeDelta)divideDecimal      (currentPos.size);
      if (adjustedDelta > collateralDelta) {
          collateralDelta = 0;
      } else {
            collateralDelta -= adjustedDelta;
           }
       }
```
Notably, when **adjustedDelta > collateralDelta** is true, **collateralDelta** is zero-ed out. Since 
GMX decreasePositionRequest() receives a uint as the collateral delta and decreases by that 
amount, the function is not able to add the delta difference. However, that collateral debt is 
effectively forgotten, and as a result, the leverage ratio could be higher than intended. The 
impact is an increased liquidation risk which is not part of the Lyra risk model.

**Recommended mitigation:**
If adjustedDelta > collateralDelta holds, make a positionRouter.createIncreasePosition() call 
with the difference in deltas.

**Team response:**
If the hedger is over-leveraged after the decrease position request; keepers will be able to 
follow up with a updateCollateral() request almost immediately to increase the collateral.
Whilst valid, it is a very unlikely case with minimal impact. The recommendation would break 
the concept of only one pending position request for the hedger at any time. As the risk is very 
temporary and there is no easy fix, this will not be resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Lyra Finance |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

