---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53325
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-07] OmoOracle wrong use of Uniswap interface to get pool address

### Overview


This bug report highlights a problem in the function `getLiquidityAmounts()` which incorrectly uses the Uniswap interface to obtain the pool address. This can cause high impact and has a medium likelihood of occurring. The recommended solution is to use the correct interface to get the pool address by catching the `token0`, `token1` and `fee` from a specific call and using it in the code. This will resolve the issue.

### Original Finding Content

## **Severity**

**Impact:** High

**Likelihood:** Medium

## **Description**

The function `getLiquidityAmounts()` incorrectly uses the Uniswap interface to obtain the pool address:

```solidity
    function getLiquidityAmounts(
        address positionManager,
        uint256 tokenId,
        uint128 liquidity
    ) internal view returns (uint256 amount0, uint256 amount1) {
        if (liquidity == 0) return (0, 0); // Handle zero liquidity case
        INonfungiblePositionManager nftManager = INonfungiblePositionManager(positionManager);

        --snip--

        IUniswapV3Pool pool = IUniswapV3Pool(nftManager.factory()); //Wrong pool address
        (uint160 sqrtPriceX96,,,,,,) = pool.slot0();

        // Calculate amounts using UniswapV3 math
        (amount0, amount1) = LiquidityAmounts.getAmountsForLiquidity(
            sqrtPriceX96,
            TickMath.getSqrtRatioAtTick(tickLower),
            TickMath.getSqrtRatioAtTick(tickUpper),
            liquidity
        );
    }
```

## Recommendations

Use correct interface to get pool address

To resolve this, get the pool that belongs to `tokenId`, you need to catch the `token0`, `token1` and `fee` from this call `nftManager.positions(tokenId);`
and use it like this

```diff
File: OmoOracle.sol#getLiquidityAmounts()

         INonfungiblePositionManager nftManager = INonfungiblePositionManager(positionManager);
         /*code*/

-        IUniswapV3Pool pool = IUniswapV3Pool(nftManager.factory());
+        address poolAddress = IUniswapV3Factory(nftManager.factory()).getPool(token0, token1, fee);
+        IUniswapV3Pool pool = IUniswapV3Pool(poolAddress);
        (uint160 sqrtPriceX96,,,,,,) = pool.slot0();
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

