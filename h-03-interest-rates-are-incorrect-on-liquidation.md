---
# Core Classification
protocol: ParaSpace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 15976
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-paraspace-contest
source_link: https://code4rena.com/reports/2022-11-paraspace
github_link: https://github.com/code-423n4/2022-11-paraspace-findings/issues/173

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
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - csanuragjain
  - unforgiven  cccz
---

## Vulnerability Title

[H-03] Interest rates are incorrect on Liquidation

### Overview


This bug report is about a vulnerability in the LiquidationLogic.sol contract, which is part of the ParaSpace protocol. The debt tokens are being transferred before calculating the interest rates, but the interest rate calculation function assumes that debt token has not yet been sent. This leads to an incorrect outcome of `currentLiquidityRate`.

The bug can be replicated by following the steps in the Proof of Concept section: Liquidator L1 calls the `executeLiquidateERC20` function, which internally calls the `_burnDebtTokens` function. This function first transfers the debt asset to xToken using the `safeTransferFrom` function, which increases the balance of xTokenAddress for liquidationAsset. Then the `updateInterestRates` function is called on ReserveLogic.sol#L169, which finally calls the `calculateInterestRates` function on DefaultReserveInterestRateStrategy#L127. This calculates the interest rate, but the calculation for `vars.availableLiquidity` is incorrect as it includes the `params.liquidityAdded` value twice.

The recommended mitigation steps for this bug is to transfer the debt asset post interest calculation. This can be done by rearranging the code in the `_burnDebtTokens` function, so that the `safeTransferFrom` function is called after the `updateInterestRates` function.

### Original Finding Content


The debt tokens are being transferred before calculating the interest rates. But the interest rate calculation function assumes that debt token has not yet been sent thus the outcome `currentLiquidityRate` will be incorrect

### Proof of Concept

1.  Liquidator L1 calls [`executeLiquidateERC20`](https://github.com/code-423n4/2022-11-paraspace/blob/main/paraspace-core/contracts/protocol/libraries/logic/LiquidationLogic.sol#L161) for a position whose health factor <1

<!---->

    function executeLiquidateERC20(
            mapping(address => DataTypes.ReserveData) storage reservesData,
            mapping(uint256 => address) storage reservesList,
            mapping(address => DataTypes.UserConfigurationMap) storage usersConfig,
            DataTypes.ExecuteLiquidateParams memory params
        ) external returns (uint256) {

    ...
     _burnDebtTokens(liquidationAssetReserve, params, vars);
    ...
    }

2.  This internally calls [`_burnDebtTokens`](https://github.com/code-423n4/2022-11-paraspace/blob/main/paraspace-core/contracts/protocol/libraries/logic/LiquidationLogic.sol#L523)

<!---->

        function _burnDebtTokens(
            DataTypes.ReserveData storage liquidationAssetReserve,
            DataTypes.ExecuteLiquidateParams memory params,
            ExecuteLiquidateLocalVars memory vars
        ) internal {
           ...

            // Transfers the debt asset being repaid to the xToken, where the liquidity is kept
            IERC20(params.liquidationAsset).safeTransferFrom(
                vars.payer,
                vars.liquidationAssetReserveCache.xTokenAddress,
                vars.actualLiquidationAmount
            );
    ...
            // Update borrow & supply rate
            liquidationAssetReserve.updateInterestRates(
                vars.liquidationAssetReserveCache,
                params.liquidationAsset,
                vars.actualLiquidationAmount,
                0
            );
        }

3.  Basically first it transfers the debt asset to xToken using below. This increases the balance of xTokenAddress for liquidationAsset

<!---->

    IERC20(params.liquidationAsset).safeTransferFrom(
                vars.payer,
                vars.liquidationAssetReserveCache.xTokenAddress,
                vars.actualLiquidationAmount
            );

4.  Now `updateInterestRates` function is called on ReserveLogic.sol#L169

<!---->

    function updateInterestRates(
            DataTypes.ReserveData storage reserve,
            DataTypes.ReserveCache memory reserveCache,
            address reserveAddress,
            uint256 liquidityAdded,
            uint256 liquidityTaken
        ) internal {
    ...
    (
                vars.nextLiquidityRate,
                vars.nextVariableRate
            ) = IReserveInterestRateStrategy(reserve.interestRateStrategyAddress)
                .calculateInterestRates(
                    DataTypes.CalculateInterestRatesParams({
                        liquidityAdded: liquidityAdded,
                        liquidityTaken: liquidityTaken,
                        totalVariableDebt: vars.totalVariableDebt,
                        reserveFactor: reserveCache.reserveFactor,
                        reserve: reserveAddress,
                        xToken: reserveCache.xTokenAddress
                    })
                );
    ...
    }

5.  Finally call to `calculateInterestRates` function on DefaultReserveInterestRateStrategy#L127 contract is made which calculates the interest rate

<!---->

    function calculateInterestRates(
            DataTypes.CalculateInterestRatesParams calldata params
        ) external view override returns (uint256, uint256) {
    ...
    if (vars.totalDebt != 0) {
                vars.availableLiquidity =
                    IToken(params.reserve).balanceOf(params.xToken) +
                    params.liquidityAdded -
                    params.liquidityTaken;

                vars.availableLiquidityPlusDebt =
                    vars.availableLiquidity +
                    vars.totalDebt;
                vars.borrowUsageRatio = vars.totalDebt.rayDiv(
                    vars.availableLiquidityPlusDebt
                );
                vars.supplyUsageRatio = vars.totalDebt.rayDiv(
                    vars.availableLiquidityPlusDebt
                );
            }
    ...
    vars.currentLiquidityRate = vars
                .currentVariableBorrowRate
                .rayMul(vars.supplyUsageRatio)
                .percentMul(
                    PercentageMath.PERCENTAGE_FACTOR - params.reserveFactor
                );

            return (vars.currentLiquidityRate, vars.currentVariableBorrowRate);
    }

6.  As we can see in above code, `vars.availableLiquidity` is calculated as `IToken(params.reserve).balanceOf(params.xToken) +params.liquidityAdded - params.liquidityTaken`

7.  But the problem is that debt token is already transferred to `xToken` which means `xToken` already consist of `params.liquidityAdded`. Hence the calculation ultimately becomes `(xTokenBeforeBalance+params.liquidityAdded) +params.liquidityAdded - params.liquidityTaken`

8.  This is incorrect and would lead to higher `vars.availableLiquidity` which ultimately impacts the `currentLiquidityRate`

### Recommended Mitigation Steps

Transfer the debt asset post interest calculation

    function _burnDebtTokens(
            DataTypes.ReserveData storage liquidationAssetReserve,
            DataTypes.ExecuteLiquidateParams memory params,
            ExecuteLiquidateLocalVars memory vars
        ) internal {
    IPToken(vars.liquidationAssetReserveCache.xTokenAddress)
                .handleRepayment(params.liquidator, vars.actualLiquidationAmount);
            // Burn borrower's debt token
            vars
                .liquidationAssetReserveCache
                .nextScaledVariableDebt = IVariableDebtToken(
                vars.liquidationAssetReserveCache.variableDebtTokenAddress
            ).burn(
                    params.borrower,
                    vars.actualLiquidationAmount,
                    vars.liquidationAssetReserveCache.nextVariableBorrowIndex
                );

    liquidationAssetReserve.updateInterestRates(
                vars.liquidationAssetReserveCache,
                params.liquidationAsset,
                vars.actualLiquidationAmount,
                0
            );
    IERC20(params.liquidationAsset).safeTransferFrom(
                vars.payer,
                vars.liquidationAssetReserveCache.xTokenAddress,
                vars.actualLiquidationAmount
            );
    ...
    ...
    }



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ParaSpace |
| Report Date | N/A |
| Finders | csanuragjain, unforgiven  cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-paraspace
- **GitHub**: https://github.com/code-423n4/2022-11-paraspace-findings/issues/173
- **Contest**: https://code4rena.com/contests/2022-11-paraspace-contest

### Keywords for Search

`vulnerability`

