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
solodit_id: 53326
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

[H-08] OmoOracle `getLiquidityAmounts()` uses spot price making it manipulatable

### Overview


The bug report describes a potential issue in the `getPositionValue()` and `getLiquidityAmounts()` functions in the `OmoOracle` contract. These functions rely on the spot price on Uniswap to calculate token amounts in a position, which makes the system vulnerable to price manipulation. The severity of this bug is classified as high, with a medium likelihood of occurring. The report recommends using a Time-Weighted Average Price (TWAP) instead of relying on the spot price to mitigate this vulnerability.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

`getPositionValue()` / `getLiquidityAmounts()` in `OmoOracle` rely on the spot price on Uniswap to calculate token amounts in a position. It makes the system vulnerable to **price manipulation**.

```solidity
    function getLiquidityAmounts(
        address positionManager,
        uint256 tokenId,
        uint128 liquidity
    ) internal view returns (uint256 amount0, uint256 amount1) {

--snip--

        IUniswapV3Pool pool = IUniswapV3Pool(nftManager.factory());
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

Use Time-Weighted Average Price (TWAP) Instead

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

