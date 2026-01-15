---
# Core Classification
protocol: Plaza Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49249
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/682
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/561

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

# Audit Details
report_date: unknown
finders_count: 14
finders:
  - Ryonen
  - stuart\_the\_minion
  - bretzel
  - 0x52
  - tinnohofficial
---

## Vulnerability Title

M-9: Market rate never used due to decimal discrepancy

### Overview


The bug report is about a decimal precision mismatch in a code called `Pool.sol` which causes the market rate to never be used. This means that the intended functionality of considering the market rate for redemptions is not working. This bug was found by multiple people and the root cause is due to a difference in decimal precision between the `marketRate` and `redeemRate`. This causes a comparison between the two rates to always be false, resulting in the incorrect amount of reserve tokens being received by users when redeeming tokens. The impact of this bug is that users may receive more reserve tokens than expected. To fix this issue, the normalization in the code needs to be changed to use the same decimal precision as the `redeemRate`. This can be done by using `bondToken.SHARES_DECIMALS()` instead of `oracleDecimals`. The protocol team has already fixed this issue in a recent update.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/561 

## Found by 
0x52, 0xadrii, 0xc0ffEE, Hueber, Ryonen, X0sauce, ZoA, bretzel, farman1094, future, fuzzysquirrel, shui, stuart\_the\_minion, tinnohofficial

### Summary

A decimal precision mismatch between `marketRate ` (18 decimal precision) and `redeemRate ` (6 decimal precision) in `Pool.sol` will cause the market rate to never be used.

### Root Cause

In [`Pool.sol#L512-L516`](https://github.com/sherlock-audit/2024-12-plaza-finance/blob/main/plaza-evm/src/Pool.sol#L512-L516), the `redeemRate` is calculated and implicitly uses a precision of 6 decimal precision : 
- [Pool#512](https://github.com/sherlock-audit/2024-12-plaza-finance/blob/main/plaza-evm/src/Pool.sol#L512)
- [Pool#516](https://github.com/sherlock-audit/2024-12-plaza-finance/blob/main/plaza-evm/src/Pool.sol#L514)
- [Pool#516](https://github.com/sherlock-audit/2024-12-plaza-finance/blob/main/plaza-evm/src/Pool.sol#L516) : The constant `BOND_TARGET_PRICE = 100` multiplied by `PRECISION = 1e6` = 100e6.

However, the `marketRate` will be [normalized](https://github.com/sherlock-audit/2024-12-plaza-finance/blob/main/plaza-evm/src/Pool.sol#L447) to 18dp : 
       The BPT token itself has 18 decimals ([`BalancerPoolToken.sol`](https://github.com/balancer/balancer-v2-monorepo/blob/master/pkg/pool-utils/contracts/BalancerPoolToken.sol)) so `totalSupply()` is 18dp.
     When calculating the price of a BPT it will formalize each price of the asset of the BPT pool to 18dp :  "balancer math works with 18 dec" [BalancerOracleAdapter.sol#L109](https://github.com/sherlock-audit/2024-12-plaza-finance/blob/main/plaza-evm/src/BalancerOracleAdapter.sol#L109). 
    It implies that the `decimals` of  [BalancerOracleAdapter](https://github.com/sherlock-audit/2024-12-plaza-finance/blob/main/plaza-evm/src/BalancerOracleAdapter.sol#L51) is set to 18.
Then the final value will have a precision of 18dp.

The comparison `marketRate < redeemRate` will always be false due to this difference in decimal precision.

### Internal Pre-conditions

1. A Chainlink price feed for the bond token must exist and be registered in `OracleFeeds`.
2. The `marketRate` from the Balancer oracle is lower than the calculated `redeemRate` when both are expressed with the same decimal precision.
3. `getOracleDecimals(reserveToken, USD)` returns 18

### External Pre-conditions

N/A

### Attack Path

1. A user initiates a redeem transaction.
2. The `simulateRedeem` and `getRedeemAmount` functions are called.
3. The condition `marketRate < redeemRate` evaluates to false due to the decimal mismatch.
4. The `redeemRate`, which might be higher than the actual market rate, is used to calculate the amount of reserve tokens the user receives.

### Impact

The intended functionality of considering the market rate for redemptions is completely bypassed.
Users redeeming tokens might receive more reserve tokens than expected if the true market rate (with correct decimals) is lower than the calculated `redeemRate`.

### PoC

N/A

### Mitigation

Change the normalization in `simulateRedeem` to use the  `bondToken.SHARES_DECIMALS()` instead of `oracleDecimals`.

```solidity
uint256 marketRate;
address feed = OracleFeeds(oracleFeeds).priceFeeds(address(bondToken), USD);
uint8 sharesDecimals = bondToken.SHARES_DECIMALS(); // Get the decimals of the shares

if (feed != address(0)) {
    marketRate = getOraclePrice(address(bondToken), USD).normalizeAmount(
        getOracleDecimals(address(bondToken), USD), 
        sharesDecimals // Normalize to sharesDecimals
    );
}
```

Modify the normalization of `marketRate` in `Pool.sol`'s `simulateRedeem` function to use the same decimal precision as `redeemRate` (6 decimals).  Specifically, change the normalization to use `bondToken.SHARES_DECIMALS()` instead of `oracleDecimals`:

```diff
 if (feed != address(0)) {
+ uint8 sharesDecimals = bondToken.SHARES_DECIMALS(); // Use sharesDecimals for consistent precision
  marketRate = getOraclePrice(address(bondToken), USD)
        .normalizeAmount(
          getOracleDecimals(address(bondToken), USD),
-          oracleDecimals // this is the decimals of the reserve token chainlink feed
+         sharesDecimals
        );


 }
 return getRedeemAmount(tokenType, depositAmount, bondSupply, levSupply, poolReserves, getOraclePrice(reserveToken, USD), oracleDecimals, marketRate)
         .normalizeAmount(COMMON_DECIMALS, IERC20(reserveToken).safeDecimals());

```

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/Convexity-Research/plaza-evm/pull/156

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Plaza Finance |
| Report Date | N/A |
| Finders | Ryonen, stuart\_the\_minion, bretzel, 0x52, tinnohofficial, X0sauce, future, fuzzysquirrel, ZoA, 0xc0ffEE, 0xadrii, shui, Hueber, farman1094 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/561
- **Contest**: https://app.sherlock.xyz/audits/contests/682

### Keywords for Search

`vulnerability`

