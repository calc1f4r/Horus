---
# Core Classification
protocol: Cap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62171
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/990
source_link: none
github_link: https://github.com/sherlock-audit/2025-07-cap-judging/issues/542

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - farismaulana
  - Drynooo
  - valuevalk
  - silver\_eth
  - Tigerfrake
---

## Vulnerability Title

M-9: Missing slippage protection in liquidation allows unexpected collateral loss

### Overview


This bug report discusses an issue found by multiple individuals in the code for a lending platform. The problem is that liquidators are not able to specify a minimum amount of collateral they want to receive during a liquidation. This means that they may end up receiving less than expected, leading to potential losses. The root cause of this issue is that the function responsible for liquidation does not have a parameter for liquidators to specify a minimum acceptable amount of collateral. This means that if the total slashable collateral is less than the expected amount, the liquidator will still receive the lower amount without any option to revert the transaction. This is a viable issue because the calculation of the total slashable collateral is based on the timestamp, which can change between the off-chain calculation and the transaction execution. Additionally, another liquidation for a different asset could occur before this one, further reducing the available collateral. This could result in unexpected losses for the liquidator. The impact of this issue is that liquidators may receive less than expected, and there is currently no way to protect against this scenario. The report suggests adding a minimum collateral received parameter to the liquidate function to mitigate this issue.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-07-cap-judging/issues/542 

## Found by 
0xsh, Drynooo, Tigerfrake, dobrevaleri, farismaulana, silver\_eth, valuevalk

### Summary

Liquidators cannot specify a minimum amount of collateral to receive during liquidation, exposing them to potential losses when slashable collateral is less than expected.

### Root Cause

In [LiquidationLogic::liquidate()](https://github.com/sherlock-audit/2025-07-cap/blob/main/cap-contracts/contracts/lendingPool/libraries/LiquidationLogic.sol#L61-L96), the function lacks a parameter for liquidators to specify a minimum acceptable amount of collateral to receive. The function contains a safety check that caps the liquidation value to the total slashable collateral:

```solidity
    function liquidate(ILender.LenderStorage storage $, ILender.RepayParams memory params)
        external
        returns (uint256 liquidatedValue)
    {
        (uint256 totalDelegation, uint256 totalSlashableCollateral, uint256 totalDebt,,, uint256 health) =
            ViewLogic.agent($, params.agent);


        ValidationLogic.validateLiquidation(
            health,
            totalDelegation * $.emergencyLiquidationThreshold / totalDebt,
            $.liquidationStart[params.agent],
            $.grace,
            $.expiry
        );


        (uint256 assetPrice,) = IOracle($.oracle).getPrice(params.asset);
        uint256 bonus = ViewLogic.bonus($, params.agent);
        uint256 maxLiquidation = ViewLogic.maxLiquidatable($, params.agent, params.asset);
        uint256 liquidated = params.amount > maxLiquidation ? maxLiquidation : params.amount;


        liquidated = BorrowLogic.repay(
            $,
            ILender.RepayParams({ agent: params.agent, asset: params.asset, amount: liquidated, caller: params.caller })
        );


        (,,,,, health) = ViewLogic.agent($, params.agent);
        if (health >= 1e27) _closeLiquidation($, params.agent);


@>      liquidatedValue =
            (liquidated + (liquidated * bonus / 1e27)) * assetPrice / (10 ** $.reservesData[params.asset].decimals);
@>      if (totalSlashableCollateral < liquidatedValue) liquidatedValue = totalSlashableCollateral;


        if (liquidatedValue > 0) IDelegation($.delegation).slash(params.agent, params.caller, liquidatedValue);


        emit Liquidate(params.agent, params.caller, params.asset, liquidated, liquidatedValue);
    }
```

However, there's no corresponding check to ensure liquidators receive at least a specified minimum amount. This means liquidators are forced to accept whatever collateral is available, which could be significantly less than what they paid to repay the debt.

The function calculates the expected liquidation value based on the repaid debt amount, asset price, and bonus.

But when `totalSlashableCollateral < liquidatedValue`, the liquidator receives less value than calculated, with no option to revert the transaction.

The issue is viable, because the `totalSlashableCollateral` is calcualted based on the epoch, which is calculated based on the timestamp. So the epoch can change between the off-chain calculation and the transaction execution, which could lead to lesser collateral available for seizing. Moreover, another liquidation (for another asset) could be executed first, which will reduce the `totalSlashableCollateral` and there is no mechanism for protecting agains such scenarios.


### Internal Pre-conditions

1. Agent's position must have less slashable collateral than what would be expected based on their debt
2. Liquidator needs to call `liquidate()` with an amount parameter for an asset the agent has borrowed


### External Pre-conditions

1. Collateral value must have decreased since the agent's position was opened


### Attack Path

1. An agent's position becomes unhealthy
2. Liquidator opens liquidation via `Lender::openLiquidation(agent)`
3. After grace period, liquidator calls `Lender::liquidate(agent, asset, amount)`
4. System calculates expected collateral to receive: `liquidatedValue`
5. System checks if `totalSlashableCollateral < liquidatedValue`
6. If true, liquidator receives `totalSlashableCollateral` instead of `liquidatedValue`
7. Transaction completes successfully, but liquidator receives less collateral than expected
8. Liquidator suffers unexpected losses

### Impact

The liquidators can receive less than expected and there is no way to protect against such scenarios.


### PoC

_No response_

### Mitigation

Add a minimum collateral received parameter to the liquidate function, which will act as a guard.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cap |
| Report Date | N/A |
| Finders | farismaulana, Drynooo, valuevalk, silver\_eth, Tigerfrake, 0xsh, dobrevaleri |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-07-cap-judging/issues/542
- **Contest**: https://app.sherlock.xyz/audits/contests/990

### Keywords for Search

`vulnerability`

