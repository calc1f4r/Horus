---
# Core Classification
protocol: Bunni v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57130
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-01-bacon-labs-bunniv2-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-01-bacon-labs-bunniv2-securityreview.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Priyanka Bose
  - Elvis Skoždopolj
  - Michael Colburn
---

## Vulnerability Title

Lack of systematic approach to rounding and arithmetic errors

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

### Description
While reviewing the codebase, we noted several areas with seemingly excessive input validation that may hint at underlying issues stemming from improper rounding directions or other arithmetic errors. While we did not identify root causes or ways to exploit these instances, they warrant further investigation and testing. If the root cause is determined to be truly benign, it should be documented. Operations that suggest a lack of a systematic approach to rounding and arithmetic errors include the following:

- **The computeSwap function of the BunniSwapMath library computes the outputAmount multiple times**, which indicates that there is a rounding or arithmetic error that is improperly handled:

    ```solidity
    // compute first pass result
    (updatedSqrtPriceX96, updatedTick, inputAmount, outputAmount) = _computeSwap(input, amountSpecified);
    
    // ensure that the output amount is lte the output token balance
    if (outputAmount > outputTokenBalance) {
        // exactly output the output token's balance
        // need to recompute swap
        amountSpecified = outputTokenBalance.toInt256();
        (updatedSqrtPriceX96, updatedTick, inputAmount, outputAmount) = _computeSwap(input, amountSpecified);
        
        if (outputAmount > outputTokenBalance) {
            // somehow the output amount is still greater than the balance due to rounding errors
            // just set outputAmount to the balance
            outputAmount = outputTokenBalance;
        }
    }
    ```
    
    ![A snippet of the computeSwap function that may result in two trial swaps before a cap is applied to outputAmount](src/lib/BunniSwapMath.sol#L62–L77)

- **The _computeSwap function of the BunniSwapMath library allows a user to get up to 2 wei of tokens for free**:

    ```solidity
    if (exactIn) {
        uint256 inputAmountSpecified = uint256(-amountSpecified);
        
        if (inputAmount > inputAmountSpecified && inputAmount < inputAmountSpecified + 3) {
            // if it's an exact input swap and inputAmount is greater than the specified input amount by 1 or 2 wei,
            // round down to the specified input amount to avoid reverts. this assumes that it's not feasible to
            // extract significant value from the pool if each swap can at most extract 2 wei.
            inputAmount = inputAmountSpecified;
        }
    }
    ```
    
    ![A snippet of the _computeSwap function that shows the input amount being rounded down in certain situations, favoring the user instead of the pool](src/lib/BunniSwapMath.sol#L336–L344)

- **The _computeRebalanceParams function of the BunniHookLogic library has a case where both tokens have excess liquidity**, indicating a rounding or arithmetic error in the way excess liquidity is computed:

    ```solidity
    // decide which token will be rebalanced (i.e., sold into the other token)
    bool willRebalanceToken0 = shouldRebalance0 && (!shouldRebalance1 || excessLiquidity0 > excessLiquidity1);
    ```
    
    ![A snippet of the _computeRebalanceParams function](src/lib/BunniHookLogic.sol#L651–L652)

- **The token densities in the queryLDF function are rounded down.** However, the density is later used as a denominator, which can result in the totalLiquidityEstimates rounding up. The getAmountsForLiquidity function always rounds down throughout the codebase, which may be incorrect in some cases, as shown in the following snippet:

    ```solidity
    (uint256 density0OfRoundedTickX96, uint256 density1OfRoundedTickX96) = LiquidityAmounts.getAmountsForLiquidity(
        sqrtPriceX96, roundedTickSqrtRatio, nextRoundedTickSqrtRatio,
        uint128(liquidityDensityOfRoundedTickX96), false
    );

    totalDensity0X96 = density0RightOfRoundedTickX96 + density0OfRoundedTickX96;
    totalDensity1X96 = density1LeftOfRoundedTickX96 + density1OfRoundedTickX96;

    uint256 totalLiquidityEstimate0 = (balance0 == 0 || totalDensity0X96 == 0) 
        ? 0 
        : balance0.fullMulDiv(Q96, totalDensity0X96);
        
    uint256 totalLiquidityEstimate1 = (balance1 == 0 || totalDensity1X96 == 0) 
        ? 0 
        : balance1.fullMulDiv(Q96, totalDensity1X96);
    ```
    
    ![A snippet of the queryLDF function](src/lib/QueryLDF.sol#L69–L77)

- **If the cumulativeAmounts0/cumulativeAmounts1 functions round down, the resulting excess liquidity is rounded up since the cumulative amounts are used as the denominator**:

    ```solidity
    uint256 excessLiquidity0 = balance0 > currentActiveBalance0
        ? (balance0 - currentActiveBalance0).divWad(
            bunniState.liquidityDensityFunction.cumulativeAmount0(
              input.key,
              minUsableTick,
              WAD,
              input.arithmeticMeanTick,
              input.updatedTick,
              bunniState.ldfParams,
              input.newLdfState
            )
        )
        : 0;

    uint256 excessLiquidity1 = balance1 > currentActiveBalance1
        ? (balance1 - currentActiveBalance1).divWad(
            bunniState.liquidityDensityFunction.cumulativeAmount1(
              input.key,
              maxUsableTick,
              WAD,
              input.arithmeticMeanTick,
              input.updatedTick,
              bunniState.ldfParams,
              input.newLdfState
            )
        )
        : 0;
    ```
    
    ![A snippet of the _computeRebalanceParams function](src/lib/BunniHookLogic.sol#L591–L616)

### Recommendations
- **Short term:** Review the system arithmetic and devise a systematic approach to rounding, ensuring rounding always favors the protocol. Implement smart contract fuzzing to determine the relative error bounds of each operation.

- **Long term:** Explore whether exposing the rounding direction as an explicit parameter in higher-level functions may help to prevent these types of issues.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Bunni v2 |
| Report Date | N/A |
| Finders | Priyanka Bose, Elvis Skoždopolj, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-01-bacon-labs-bunniv2-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-01-bacon-labs-bunniv2-securityreview.pdf

### Keywords for Search

`vulnerability`

