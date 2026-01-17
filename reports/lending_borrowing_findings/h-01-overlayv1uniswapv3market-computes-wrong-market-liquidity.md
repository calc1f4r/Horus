---
# Core Classification
protocol: Overlay Protocol
chain: everychain
category: logic
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1062
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-overlay-protocol-contest
source_link: https://code4rena.com/reports/2021-11-overlay
github_link: https://github.com/code-423n4/2021-11-overlay-findings/issues/83

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:
  - wrong_math
  - business_logic

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - payments
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-01] OverlayV1UniswapV3Market computes wrong market liquidity

### Overview


This bug report is about the `OverlayV1UniswapV3Market.fetchPricePoint` function, which tries to compute the market depth in OVL terms. The code uses the `ethIs0` boolean to get the market liquidity _in ETH_ (and not the other token pair), however, `ethIs0` refers to the `ovlFeed`, whereas the `_liquidity` refers to the `marketFeed`, and thus the boolean has nothing to do with the _market_ feed where the liquidity is taken from.

The impact of this bug is that if the `ovlFeed` and `marketFeed` do not have the same token position for the ETH pair (ETH is either token 0 or token 1 for **both** pairs), then the market liquidity & depth is computed wrong (inverted). For example, the `OverlayV1Market.depth()` function will return a wrong depth which is used in the market cap computation.

The recommended mitigation step is that `marketFeed.token0() == WETH` should be used in `fetchPricePoint` to compute the liquidity instead of `ovlFeed.token0() == WETH`.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `OverlayV1UniswapV3Market.fetchPricePoint` tries to compute the market depth in OVL terms as `marketLiquidity (in ETH) / ovlPrice (in ETH per OVL)`.
To get the market liquidity _in ETH_ (and not the other token pair), it uses the `ethIs0` boolean.

```solidity
_marketLiquidity = ethIs0
    ? ( uint256(_liquidity) << 96 ) / _sqrtPrice
    : FullMath.mulDiv(uint256(_liquidity), _sqrtPrice, X96);
```

However, `ethIs0` boolean refers to the `ovlFeed`, whereas the `_liquidity` refers to the `marketFeed`, and therefore the `ethIs0` boolean has nothing to do with the _market_ feed where the liquidity is taken from:

```solidity
// in constructor, if token0 is eth refers to ovlFeed
ethIs0 = IUniswapV3Pool(_ovlFeed).token0() == _eth;

// in fetchPricePoint, _liquidity comes from different market feed
( _ticks, _liqs ) = IUniswapV3Pool(marketFeed).observe(_secondsAgo);
_marketLiquidity = ethIs0
    ? ( uint256(_liquidity) << 96 ) / _sqrtPrice
    : FullMath.mulDiv(uint256(_liquidity), _sqrtPrice, X96);
```

## Impact
If the `ovlFeed` and `marketFeed` do not have the same token position for the ETH pair (ETH is either token 0 or token 1 for **both** pairs), then the market liquidity & depth is computed wrong (inverted).
For example, the `OverlayV1Market.depth()` function will return a wrong depth which is used in the market cap computation.

## Recommended Mitigation Steps
It seems that `marketFeed.token0() == WETH` should be used in `fetchPricePoint` to compute the liquidity instead of `ovlFeed.token0() == WETH`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Overlay Protocol |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-overlay
- **GitHub**: https://github.com/code-423n4/2021-11-overlay-findings/issues/83
- **Contest**: https://code4rena.com/contests/2021-11-overlay-protocol-contest

### Keywords for Search

`Wrong Math, Business Logic`

