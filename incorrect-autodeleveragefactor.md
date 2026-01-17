---
# Core Classification
protocol: Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49978
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl
source_link: none
github_link: https://github.com/Cyfrin/2025-01-zaros-part-2

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xtimefliez
  - kupiasec
---

## Vulnerability Title

Incorrect `AutoDeleverageFactor`.

### Overview


The bug report is about an incorrect calculation of `AutoDeleverageFactor` in a code repository. This factor is used to determine the amount of profit a trader receives when the market enters a certain state. The bug causes traders to not receive their profits when the market enters the auto deleverage state. The recommendation is to make a small change in the code to fix the calculation and ensure traders receive their profits correctly.

### Original Finding Content

## Summary
The calculation of `AutoDeleverageFactor` is incorrect.

## Vulnerability Details
https://github.com/Cyfrin/2025-01-zaros-part-2/blob/main/src/market-making/leaves/Market.sol#L174
```solidity
    function getAutoDeleverageFactor(
        ...
    )   ...
    {   ...
        UD60x18 unscaledDeleverageFactor = Math.min(marketDebtRatio, autoDeleverageEndThresholdX18).sub(
            autoDeleverageStartThresholdX18
        ).div(autoDeleverageEndThresholdX18.sub(autoDeleverageStartThresholdX18));

        // finally, raise to the power scale
174:    autoDeleverageFactorX18 = unscaledDeleverageFactor.pow(autoDeleverageExponentZX18);
    }
```
As we can see, when `marketRatio >= ADL start threshold`, the smaller debt, the smaller `autoDeleverageFactor`.
For example:
When `marketDebtRatio = autoDeleverageStartThresholdX18`, the calcuatated AutoDeleverageFactor is zero.
When `marketDebtRatio = autoDeleverageEndThresholdX18`, the calcuatated AutoDeleverageFactor is one.

https://github.com/Cyfrin/2025-01-zaros-part-2/blob/main/src/market-making/branches/CreditDelegationBranch.sol#L159
```solidity    
    function getAdjustedProfitForMarketId(
        ...
        if (market.isAutoDeleverageTriggered(delegatedCreditUsdX18, marketTotalDebtUsdX18)) {
            // if the market's auto deleverage system is triggered, it assumes marketTotalDebtUsdX18 > 0
            adjustedProfitUsdX18 =
159:            market.getAutoDeleverageFactor(delegatedCreditUsdX18, marketTotalDebtUsdX18).mul(adjustedProfitUsdX18);
        }
```
https://github.com/Cyfrin/2025-01-zaros-part-2/blob/main/src/perpetuals/branches/SettlementBranch.sol#L499
```solidity
        if (ctx.pnlUsdX18.gt(SD59x18_ZERO)) {
            IMarketMakingEngine marketMakingEngine = IMarketMakingEngine(perpsEngineConfiguration.marketMakingEngine);

            ctx.marginToAddX18 =
499:            marketMakingEngine.getAdjustedProfitForMarketId(marketId, ctx.pnlUsdX18.intoUD60x18().intoUint256());

            tradingAccount.deposit(perpsEngineConfiguration.usdToken, ctx.marginToAddX18);

            // mint settlement tokens credited to trader; tokens are minted to
            // address(this) since they have been credited to the trader's margin
            marketMakingEngine.withdrawUsdTokenFromMarket(marketId, ctx.marginToAddX18.intoUint256());
        }
```
As a result, Traders receive their full pnls when `marketDebtRatio = autoDeleverageEndThresholdX18`,but none when `marketDebtRatio = autoDeleverageStartThresholdX18`.

## Impact
Traders do not receive their PnLs at all when the state enters the ADL state.

## Recommendations
https://github.com/Cyfrin/2025-01-zaros-part-2/blob/main/src/market-making/leaves/Market.sol#L174
```diff
    function getAutoDeleverageFactor(
        ...
    )   ...
    {   ...
        UD60x18 unscaledDeleverageFactor = Math.min(marketDebtRatio, autoDeleverageEndThresholdX18).sub(
            autoDeleverageStartThresholdX18
        ).div(autoDeleverageEndThresholdX18.sub(autoDeleverageStartThresholdX18));

        // finally, raise to the power scale
-174:    autoDeleverageFactorX18 = unscaledDeleverageFactor.pow(autoDeleverageExponentZX18);
+174:    autoDeleverageFactorX18 = UD60x18_UNIT.sub(unscaledDeleverageFactor).pow(autoDeleverageExponentZX18);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | 0xtimefliez, kupiasec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

