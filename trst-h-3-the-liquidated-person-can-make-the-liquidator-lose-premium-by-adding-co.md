---
# Core Classification
protocol: Stella
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19047
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
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
  - front-running

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-3 The liquidated person can make the liquidator lose premium by adding collateral in advance

### Overview


This bug report describes a scenario in which Alice attempts to liquidate Bob's position, but due to Bob's quick action of frontrunning Alice's transaction and adjusting the position's health state, Alice ends up losing the premium she paid. This breaks the protocol's liquidation mechanism and could lead to more bad debts. The recommended mitigation is to have the liquidated party bear the premium, or the liquidator use the minDiscount parameter to set the minimum acceptable discount. The team suggested adding a maxPayAmount parameter as slippage control in the liquidate() function and reverting if the requiredPayAmount exceeds the value. This mitigation would allow liquidators to use the maxPayAmount parameter to prevent compromise in liquidation. The severity of the bug is based on the worst-case scenario.

### Original Finding Content

**Description:**
When the position with **debtRatioE18 >= 1e18** or **startLiqTimestamp ! = 0**, the position can 
be liquidated. On liquidation, the liquidator needs to pay premium, but the profit is related 
to the position's health factor and **deltaTime**, and when **discount == 0**, the liquidator loses 
premium.
```solidity
            uint deltaTime;
            // 1.1 check the amount of time since position is marked
            if (pos.startLiqTimestamp > 0) {
                 deltaTime = Math.max(deltaTime, block.timestamp - pos.startLiqTimestamp);
            }
            // 1.2 check the amount of time since position is past the deadline
             if (block.timestamp > pos.positionDeadline) {
                    deltaTime = Math.max(deltaTime, block.timestamp - pos.positionDeadline);
            }
            // 1.3 cap time-based discount, as configured
              uint timeDiscountMultiplierE18 = Math.max(
                IConfig(config).minLiquidateTimeDiscountMultiplierE18(),
                     ONE_E18 - deltaTime * IConfig(config).liquidateTimeDiscountGrowthRateE18()
            );
            // 2. calculate health-based discount factor
            uint curHealthFactorE18 = (ONE_E18 * ONE_E18) /
             getPositionDebtRatioE18(_positionManager, _user, _posId);
                 uint minDesiredHealthFactorE18 = IConfig(config).minDesiredHealthFactorE18s(strategy);
            // 2.1 interpolate linear health discount factor (according to the diagram in documentation)
            uint healthDiscountMultiplierE18 = ONE_E18;
             if (curHealthFactorE18 < ONE_E18) {
                 healthDiscountMultiplierE18 = curHealthFactorE18 > minDesiredHealthFactorE18
                     ? ((curHealthFactorE18 - minDesiredHealthFactorE18) * ONE_E18) /
            (ONE_E18 - minDesiredHealthFactorE18)
            : 0;
            }
            // 3. final liquidation discount = apply the two discount methods together
            liquidationDiscountMultiplierE18 =
            (timeDiscountMultiplierE18 * healthDiscountMultiplierE18) /
            ONE_E18;
```
Consider the following scenario.
1. Alice notices Bob's position with **debtRatioE18 >= 1e18** and calls `liquidatePosition()` to 
liquidate.
2. Bob observes Alice's transaction, frontruns a call `markLiquidationStatus()` to make 
**startLiqTimestamp == block.timestamp**, and calls `adjustExtraColls()` to bring the position 
back to the health state.
3. Alice's transaction is executed, and since the **startLiqTimestamp** of Bob's 
**position.startLiqTimestamp ! = 0**, it can be liquidated, but since **discount = 0**, Alice loses 
premium.
This breaks the protocol's liquidation mechanism and causes the liquidator not to launch 
liquidation for fear of losing assets, which will lead to more bad debts 

**Recommended Mitigation:**
Consider having the liquidated person bear the premium, or at least have the liquidator use 
the minDiscount parameter to set the minimum acceptable discount.

**Team response:**
Liquidator contracts can easily require the min amount in their own logic to ensure 
profitability anyways.

Add **maxPayAmount** parameter as slippage control in the `liquidate()` and if 
**requiredPayAmount** exceeds the value, just revert.

**Mitigation Review:**
The fix makes liquidators able to use the **maxPayAmount** parameter to prevent compromise 
in liquidation.
In addition, after discussing with the team, there are some external conditions / measures 
that the team could make, which could lead to a lower severity, but the assigned severity is 
based on the worst-case scenario.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Front-Running`

