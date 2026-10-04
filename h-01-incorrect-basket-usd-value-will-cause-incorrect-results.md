---
# Core Classification
protocol: Cove_2024-12-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57953
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Cove-security-review_2024-12-30.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Incorrect basket USD value will cause incorrect results

### Overview


The report describes a bug in a token swap function that causes the total value of a basket to be inaccurate due to fees being applied during the internal trades process. This results in the deviation weight check being inaccurate and potentially causing errors in the swap. The recommendation is to provide the total values array during the internal trades process and account for the fees applied.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

Upon proposing a token swap, we have the following sequence of function calls:

```solidity
uint256[] memory totalValues = new uint256[](numBaskets);
// 2d array of asset balances for each basket
uint256[][] memory basketBalances = new uint256[][](numBaskets);
_initializeBasketData(self, baskets, basketAssets, basketBalances, totalValues);
// NOTE: for rebalance retries the internal trades must be updated as well
_processInternalTrades(self, internalTrades, baskets, basketBalances);
_validateExternalTrades(self, externalTrades, baskets, totalValues, basketBalances);
if (!_isTargetWeightMet(self, baskets, basketTargetWeights, basketAssets, basketBalances, totalValues)) {
         revert TargetWeightsNotMet();
}
```

The `totalValues` array is the total USD value of a basket, a basket per element of the array. It is populated upon calling `_initialBasketData()`, then it is provided in `_validateExternalTrades()` where the array is manipulated based on the trades. Afterwards, it is used upon checking the deviation in `_isTargetWeightMet()`:

```solidity
uint256 afterTradeWeight = FixedPointMathLib.fullMulDiv(assetValueInUSD, _WEIGHT_PRECISION, totalValues[i]);
if (MathUtils.diff(proposedTargetWeights[j], afterTradeWeight) > _MAX_WEIGHT_DEVIATION) {
         return false;
}
```

The code functions correctly assuming that the USD value of a basket stays stationary during the `_processInternalTrades()` during the call. However, that is not actually the case due to the fact that there is a fee upon processing the internal trades:

```solidity
if (swapFee > 0) {
                info.feeOnSell = FixedPointMathLib.fullMulDiv(trade.sellAmount, swapFee, 20_000);
                self.collectedSwapFees[trade.sellToken] += info.feeOnSell;
                emit SwapFeeCharged(trade.sellToken, info.feeOnSell);
            }
if (swapFee > 0) {
                info.feeOnBuy = FixedPointMathLib.fullMulDiv(initialBuyAmount, swapFee, 20_000);
                self.collectedSwapFees[trade.buyToken] += info.feeOnBuy;
                emit SwapFeeCharged(trade.buyToken, info.feeOnBuy);
            }
```

This results in the USD value of both the `fromBasket` and the `toBasket` going down based on the fee amount, thus the deviation weight check will be inaccurate as the `totalValues` array is not changed during the internal trades processing, it is out-of-sync.

## Recommendations

Provide the total values array upon processing the internal trades and account for the fees applied.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Cove_2024-12-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Cove-security-review_2024-12-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

