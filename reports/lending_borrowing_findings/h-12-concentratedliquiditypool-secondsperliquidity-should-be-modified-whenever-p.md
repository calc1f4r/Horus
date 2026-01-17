---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25572
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-sushitrident-2
source_link: https://code4rena.com/reports/2021-09-sushitrident-2
github_link: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/15

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-12] `ConcentratedLiquidityPool`: `secondsPerLiquidity` should be modified whenever pool liquidity changes

### Overview


A bug was discovered in the `mint()` and `burn()` functions of a smart contract, where the `secondsPerLiquidity` value is not updated prior to liquidity addition or removal. This affects the case where liquidity changes when `lowerTick <= currentTick < upperTick`.

The `secondsPerLiquidity` is updated as such: `secondsPerLiquidity += uint160((diff << 128) / liquidity);` where `diff = timestamp - uint256(lastObservation)`. Therefore, the latest `secondsPerLiquidity` value should be calculated and used in `Ticks.insert()` prior to liquidity addition or removal.

The recommended mitigation steps are to apply the `secondsPerLiquidity` increment logic prior to liquidity addition in `mint()` and removal in `burn()`. This was initially disputed, but later confirmed by a judge.

### Original Finding Content

_Submitted by hickuphh3_

##### Impact
`secondsPerLiquidity` is updated as such: `secondsPerLiquidity += uint160((diff << 128) / liquidity);` where `diff = timestamp - uint256(lastObservation)`. Hence, whenever liquidity changes, `secondsPerLiquidity` should be updated prior to the change.

In particular, this affects the `mint()` and `burn()` functions, in the case where liquidity changes when `lowerTick <= currentTick < upperTick`.

In fact, the latest `secondsPerLiquidity` value should be calculated and used in `Ticks.insert()`. For comparison, notice how UniswapV3 fetches the latest value by calling `observations.observeSingle()` in its `_updatePosition()` function.

##### Recommended Mitigation Steps
The `secondsPerLiquidity` increment logic should be applied prior to liquidity addition in `mint()` and removal in `burn()`.

```jsx
// insert logic before these lines in mint()
unchecked {
  if (priceLower < currentPrice && currentPrice < priceUpper) liquidity += uint128(_liquidity);
}

nearestTick = Ticks.insert(
ticks,
feeGrowthGlobal0,
feeGrowthGlobal1,
secondsPerLiquidity, // should calculate and use latest secondsPerLiquidity value
    ...
);

// insert logic before before these lines in burn()
unchecked {
  if (priceLower < currentPrice && currentPrice < priceUpper) liquidity -= amount;
}
```

**[sarangparikh22 (Sushi) disputed](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/15#issuecomment-954274917):**
 > The secondsPerLiquidity is same, changing the order of that will not affect anything, since it is not getting calculated at the mint or burn function.

**[alcueca (judge) commented](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/15#issuecomment-967159284):**
 > @sarangparikh22 (Sushi), could you please elaborate on why this isn't an issue?

**[sarangparikh22 (Sushi) confirmed](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/15#issuecomment-970862817):**
 > @alcueca (judge) my apologies, this is an issue. I could confirm this.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-sushitrident-2
- **GitHub**: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/15
- **Contest**: https://code4rena.com/reports/2021-09-sushitrident-2

### Keywords for Search

`vulnerability`

