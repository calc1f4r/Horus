---
# Core Classification
protocol: g8keep_2024-12-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45306
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/g8keep-security-review_2024-12-12.md
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

[H-01] Migration will fail trying to swap 1 wei of tokens to reach the target price

### Overview


This bug report discusses an issue with migrating tokens to a Uniswap V3 pool. The severity of the bug is considered medium and the likelihood of it occurring is high. The problem occurs when the code attempts to change the pool's price by adding temporary liquidity and performing a swap. If the pool's price does not reach the target price, the code will not complete the migration. This is because the code only tries to swap with 1 wei of ETH, which is not enough to reach the target price. To fix this issue, it is recommended to calculate the exact amount needed to reach the target price and allow for some margin of error when checking the pool's price.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

When the code wants to migrate tokens to Uniswap V3 pool, first it tries to change the pool's price by adding temporary liquidity and performing a swap in `_adjustPoolPrice()`:

```solidity
       uint256 tmpLPTokenId =
            _addTemporaryLiquidity(ethAmount / 100, tokenAmount / 100, constainedTickLower, constrainedTickUpper);

        if (sqrtPriceX96Start > sqrtPriceX96) {
            IUniswapV3Pool(poolAddress).swap(address(this), true, int256(uint256(tokenAmount)), sqrtPriceX96, "");
        } else {
            IUniswapV3Pool(poolAddress).swap(address(this), false, int256(uint256(1)), sqrtPriceX96, "");
        }
----snip
        (uint160 sqrtPriceX96New,,,,,,) = IUniswapV3Pool(poolAddress).slot0();
        adjustFailed = sqrtPriceX96 != sqrtPriceX96New;
```

And if the pool's price doesn't reach the target price then the code doesn't migrate. The issue is that the code tries to swap with 1 wei of ETH and it won't be enough to reach the target price the price would only reach the `constrainedTickUpper` and as a result the `adjustFailed ` would be true and migration can't be completed and it would revert always.

## Recommendations

Calculate the exact amount required to reach that target price level and use it in the swap and also allows for some percentage of error when checking the pool's price and target price.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | g8keep_2024-12-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/g8keep-security-review_2024-12-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

