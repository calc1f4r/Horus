---
# Core Classification
protocol: Steakhut
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44172
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/SteakHut-Security-Review.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[H-01] Usage Of `slot0` To Get `sqrtPriceLimitX96` Is Extremely Prone To Manipulation

### Overview


This bug report highlights a potential vulnerability in the `EnigmaZapper.sol` contract and `EnigmaHelper` library. The code uses the `slot0` method from the UniswapV3 pool to calculate the price of token0, which can be easily manipulated by bots and flashloans. This could result in incorrect calculations and potential loss of funds for the protocol and its users. The affected code can be found in the `src/EnigmaZapper.sol` and `src/libs/EnigmaHelper.sol` files. The recommendation is to use the `TWAP` function instead, which calculates the average price of an asset over a set period. The team has acknowledged the issue.

### Original Finding Content

## Severity

High Risk

## Description

In the `_calculatePriceFromLiquidity()` function in the `EnigmaZapper.sol` contract and `getLiquidityForAmounts()` and `getAmountsForLiquidity()` in `EnigmaHelper` the UniswapV3.slot0 is used to get the value of `sqrtPriceX96`, which is used to calculate the price of token0 and then performs the swap in `performZap()`.

The usage of `slot0` is extremely prone to manipulation. The [slot0](https://docs.uniswap.org/contracts/v3/reference/core/interfaces/pool/IUniswapV3PoolState#slot0) in the pool stores many values, and is exposed as a single method to save gas when accessed externally. The data can change with any frequency including multiple times per transaction.

## Impact

The `sqrtPriceX96` is pulled from `Uniswap.slot0`, which is the most recent data point and can be manipulated easily via MEV bots and Flashloans with sandwich attacks, which can cause the loss of funds when interacting with `Uniswap.swap` function. This could lead to wrong calculations and loss of funds for the protocol and other users.

## Location of Affected Code

File: [`src/EnigmaZapper.sol`](https://github.com/0xSirloin/enigma_contracts/blob/2ec77b1b38aa981143823568b1ccc6d668beeffe/src/libs/EnigmaHelper.sol)

```solidity
function _calculatePriceFromLiquidity(address _pool) internal view returns (uint256) {
  IUniswapV3Pool pool = IUniswapV3Pool(_pool);
  (uint160 sqrtPriceX96,,,,,,) = pool.slot0(); // @audit-issue can be easily manipulated

  uint256 _sqrtPriceX96_1 = uint256(sqrtPriceX96) * (uint256(sqrtPriceX96)) * (1e18) >> (96 * 2);
  return _sqrtPriceX96_1;
}
```

File: [`src/libs/EnigmaHelper.sol#L26-#L56`](github.com/0xSirloin/enigma_contracts/blob/2ec77b1b38aa981143823568b1ccc6d668beeffe/src/libs/EnigmaHelper.sol#L26-#L56)

```solidity
function getLiquidityForAmounts(address _pool, int24 tickLower, int24 tickUpper, uint256 amount0, uint256 amount1) public view returns (uint128) {
  (uint160 sqrtRatioX96,,,,,,) = IUniswapV3Pool(_pool).slot0(); // @audit-issue can be easily manipulated

  return LiquidityAmounts.getLiquidityForAmounts(
    sqrtRatioX96,
    TickMath.getSqrtRatioAtTick(tickLower),
    TickMath.getSqrtRatioAtTick(tickUpper),
    amount0,
    amount1
  );
}

function getAmountsForLiquidity(address _pool, int24 tickLower, int24 tickUpper, uint128 liquidity) public view returns (uint256, uint256) {
  (uint160 sqrtRatioX96,,,,,,) = IUniswapV3Pool(_pool).slot0(); // @audit-issue can be easily manipulated
  return LiquidityAmounts.getAmountsForLiquidity(
    sqrtRatioX96, TickMath.getSqrtRatioAtTick(tickLower), TickMath.getSqrtRatioAtTick(tickUpper), liquidity
  );
}
```

## Recommendation

Use the [`TWAP`](https://tienshaoku.medium.com/a-guide-on-uniswap-v3-twap-oracle-2aa74a4a97c5) function instead of `slot0` to get the value of `sqrtPriceX96`. `TWAP` is a pricing algorithm used to calculate the average price of an asset over a set period. It is calculated by summing prices at multiple points across a set period and then dividing this total by the total number of price points.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Steakhut |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/SteakHut-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

