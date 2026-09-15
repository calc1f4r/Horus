---
# Core Classification
protocol: USSD - Autonomous Secure Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19143
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/82
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/111

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
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 13
finders:
  - Juntao
  - PokemonAuditSimulator
  - toshii
  - Dug
  - twicek
---

## Vulnerability Title

M-3: rebalance process incase of  selling the collateral, could revert because of underflow calculation

### Overview


This bug report is about a rebalance process that can revert because of an underflow calculation. The rebalance process is triggered when the system tries to sell the collateral in case of a peg-down. The calculation of the asset to be sold (`amountToSellUnits`) is first calculated, then swapped to `baseAsset` via Uniswap. However, when subtracting `amountToBuyLeftUSD` with the result of `(IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)`, there is no guarantee that `amountToBuyLeftUSD` will always be bigger than `(IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)`, which can cause the call to revert. 

This bug was found by 0xHati, Dug, GimelSec, Juntao, PokemonAuditSimulator, T1MOH, WATCHPUG, XDZIBEC, ast3ros, saidam017, toshii, tsvetanovv, and twicek. The code snippets related to this bug can be found at https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L116-L125 and https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L132-L138.

The impact of this bug is that the rebalance process can revert due to an underflow calculation. The recommended fix is to check if `(IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)` is greater than `amountToBuyLeftUSD`, and if so, set `amountToBuyLeftUSD` to 0. The tool used to find this bug was manual review.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/111 

## Found by 
0xHati, Dug, GimelSec, Juntao, PokemonAuditSimulator, T1MOH, WATCHPUG, XDZIBEC, ast3ros, saidam017, toshii, tsvetanovv, twicek
## Summary

rebalance process, will try to sell the collateral in case of peg-down. However, the process can revert because the calculation can underflow.

## Vulnerability Detail

Inside `rebalance()` call, if `BuyUSSDSellCollateral()` is triggered, it will try to sell the current collateral to `baseAsset`. The asset that will be sold (`amountToSellUnits`) first calculated. Then swap it to `baseAsset` via uniswap. However, when subtracting `amountToBuyLeftUSD`, it with result of `(IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)`. There is no guarantee `amountToBuyLeftUSD` always bigger than `(IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)`.

This causing the call could revert in case `(IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)` > `amountToBuyLeftUSD`.

There are two branch where `amountToBuyLeftUSD -= (IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)` is performed : 

1. Incase `collateralval > amountToBuyLeftUSD`

https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L116-L125

`collateralval` is calculated using oracle price, thus the result of swap not guaranteed to reflect the proportion of `amountToBuyLefUSD` against `collateralval` ratio, and could result in returning `baseAsset` larger than expected. And potentially  `(IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)` > `amountToBuyLeftUSD`

```solidity
        uint256 collateralval = IERC20Upgradeable(collateral[i].token).balanceOf(USSD) * 1e18 / (10**IERC20MetadataUpgradeable(collateral[i].token).decimals()) * collateral[i].oracle.getPriceUSD() / 1e18;
        if (collateralval > amountToBuyLeftUSD) {
          // sell a portion of collateral and exit
          if (collateral[i].pathsell.length > 0) {
            uint256 amountBefore = IERC20Upgradeable(baseAsset).balanceOf(USSD);
            uint256 amountToSellUnits = IERC20Upgradeable(collateral[i].token).balanceOf(USSD) * ((amountToBuyLeftUSD * 1e18 / collateralval) / 1e18) / 1e18;
            IUSSD(USSD).UniV3SwapInput(collateral[i].pathsell, amountToSellUnits);
            amountToBuyLeftUSD -= (IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore);
            DAItosell += (IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore);
          } else {
```

2. Incase `collateralval < amountToBuyLeftUSD`

https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L132-L138

This also can't guarantee `(IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)` < `amountToBuyLeftUSD`.

```solidity
          if (collateralval >= amountToBuyLeftUSD / 20) {
            uint256 amountBefore = IERC20Upgradeable(baseAsset).balanceOf(USSD);
            // sell all collateral and move to next one
            IUSSD(USSD).UniV3SwapInput(collateral[i].pathsell, IERC20Upgradeable(collateral[i].token).balanceOf(USSD));
            amountToBuyLeftUSD -= (IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore);
            DAItosell += (IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore);
          }
```

## Impact

Rebalance process can revert caused by underflow calculation.

## Code Snippet

https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L116-L125
https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L132-L138

## Tool used

Manual Review

## Recommendation

Check if `(IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore)` > `amountToBuyLeftUSD`, in that case, just set `amountToBuyLeftUSD` to 0.

```solidity
          ...
            uint baseAssetChange = IERC20Upgradeable(baseAsset).balanceOf(USSD) - amountBefore);
            if (baseAssetChange > amountToBuyLeftUSD) {
                amountToBuyLeftUSD = 0;
            } else {
                amountToBuyLeftUSD -= baseAssetChange;
           }
            DAItosell += baseAssetChange;
          ...
```




## Discussion

**hrishibhat**

This is a valid medium

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USSD - Autonomous Secure Dollar |
| Report Date | N/A |
| Finders | Juntao, PokemonAuditSimulator, toshii, Dug, twicek, T1MOH, WATCHPUG, tsvetanovv, saidam017, 0xHati, XDZIBEC, GimelSec, ast3ros |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/111
- **Contest**: https://app.sherlock.xyz/audits/contests/82

### Keywords for Search

`vulnerability`

