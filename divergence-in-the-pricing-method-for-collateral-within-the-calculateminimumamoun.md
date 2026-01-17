---
# Core Classification
protocol: The Standard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41598
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl
source_link: none
github_link: https://github.com/Cyfrin/2023-12-the-standard

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
finders_count: 11
finders:
  - carrotsmuggler
  - Aamirusmani1552
  - EVDocPhantom
  - KupiaSec
  - Tricko
---

## Vulnerability Title

Divergence in the pricing method for collateral within the `calculateMinimumAmountOut()` may result in vaults transitioning into an uncollateralized state after executing swaps.

### Overview


The report discusses a bug in the `calculateMinimumAmountOut()` function of the `SmartVaultV3` contract. This function calculates the minimum amount of collateral needed for a swap to occur. The bug is caused by using the `calculator.tokenToEur()` method instead of `calculator.tokenToEurAvg()`, leading to incorrect values for `collateralValueMinusSwapValue` when there are recent changes in the price of the swapped token. This can result in the vault becoming uncollateralized after executing a swap, especially during periods of market volatility. The impact of this bug is high and it is recommended to use `calculator.tokenToEurAvg()` instead to mitigate the issue. 

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/SmartVaultV3.sol#L206-L212">https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/SmartVaultV3.sol#L206-L212</a>


## Summary
In the `SmartVaultV3.calculateMinimumAmountOut()` function, the variable `collateralValueMinusSwapValue` is computed using `calculator.tokenToEur()` instead of `calculator.tokenToEurAvg()`. This leads to inaccurate values for `collateralValueMinusSwapValue` when there are recent changes in the price of the swapped token. In extreme cases, this miscalculation can result in the `SmartVaultV3.swap()` function instantly placing the vault in an uncollaterized position after the swap.

## Vulnerability Details
Before any swap is done, the swap parameters need to be calculated on-chain, especially the `minAmountOut` parameter. This parameter is calculated in `SmartVaultV3.calculateMinimumAmountOut()`, as shown in the code snippet from `calculateMinimumAmountOut()` below.

```
function calculateMinimumAmountOut(bytes32 _inTokenSymbol, bytes32 _outTokenSymbol, uint256 _amount) private view returns (uint256) {
    ISmartVaultManagerV3 _manager = ISmartVaultManagerV3(manager);
    uint256 requiredCollateralValue = minted * _manager.collateralRate() / _manager.HUNDRED_PC();
    uint256 collateralValueMinusSwapValue = euroCollateral() - calculator.tokenToEur(getToken(_inTokenSymbol), _amount);
    return collateralValueMinusSwapValue >= requiredCollateralValue ?
        0 : calculator.eurToToken(getToken(_outTokenSymbol), requiredCollateralValue - collateralValueMinusSwapValue);
}
```

As we can see, when `collateralValueMinusSwapValue` is calculated it gets the current vault collateral from `euroCollateral()`.Internally, this function uses `calculator.tokenToEurAvg()` to fetch the value of collaterals. The method `tokenToEurAvg()` computes the average value of the specified token over the last four hours. However, immediately following this, `euroCollateral()` subtracts the result by `calculator.tokenToEur`, which instead utilizes the most recent value of the token, not the averaged one.

This mismatch from using `tokenToEur` instead of `tokenToEurAvg()` makes `collateralValueMinusSwapValue` susceptible to rapid price fluctuations. Consequently, under volatile market conditions, `collateralValueMinusSwapValue` might be overestimated or underestimated, depending on whether the token prices are rising or falling.

If `tokenToEurAvg()` > `tokenToEur()`, such as when the token price is falling, `collateralValueMinusSwapValue` will be overestimated. Conversely, if `tokenToEurAvg()` < `tokenToEur()`, such as when the price is increasing, `collateralValueMinusSwapValue` will be underestimated. This discrepancy can lead to issues; for instance, an overestimated `collateralValueMinusSwapValue` can result in a smaller `minAmountOut` calculated in `SmartVaultV3.calculateMinimumAmountOut()`. In extreme cases, this can cause the swap output to be less collateral than required, putting the vault in an uncollaterized state.

This is particularly problematic during situations when vault owners are more likely to perform swaps, such as swapping one collateral for another during periods of market volatility to shield themselves from declining asset values. In such cases, the difference between `tokenToEurAvg()` and `tokenToEur()` becomes more significant due to the rapid price fluctuations.

Consider the following example: If the price of WBTC has significantly decreased over the last few hours, a vault owner swaps their WBTC collateral to another asset to safeguard against undercollateralization in case the WBTC keeps falling. However, due to the recent fall in the WBTC price, `tokenToEurAvg()` > `tokenToEur()`, leading to an overestimated `collateralValueMinusSwapValue`. As a result, the `minAmountOut` calculated from the swap is reduced, making the vault less collateralized, contrary to the owner's intention of protecting the vault through the swap.

## Impact
During volatile market conditions, `collateralValueMinusSwapValue` will be calculated incorrectly. In extreme cases, this can cause swaps to place the vault in an uncollaterized state.

## Tools Used 
Manual Review.

## Recommended Mitigation
Consider using `calculator.tokenToEurAvg` instead of `calculator.tokenToEur` in `SmartVaultV3.calculateMinimumAmountOut()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | The Standard |
| Report Date | N/A |
| Finders | carrotsmuggler, Aamirusmani1552, EVDocPhantom, KupiaSec, Tricko, khramov, greatlake, 0xCiphky, Tripathi |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-12-the-standard
- **Contest**: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl

### Keywords for Search

`vulnerability`

