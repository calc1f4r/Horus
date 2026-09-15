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
solodit_id: 25566
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-sushitrident-2
source_link: https://code4rena.com/reports/2021-09-sushitrident-2
github_link: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/53

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

[H-06] `ConcentratedLiquidityPosition.sol#collect()` Users may get double the amount of yield when they call `collect()` before `burn()`

### Overview


This bug report is about the ConcentratedLiquidityPosition.sol#collect() function, which is used to collect yield from a pool. The bug is that when there are enough tokens in the bento.balanceOf, the function will not call position.pool.collect() to collect fees from the pool. This causes the user who calls collect() to get double yield when they call burn() to remove liquidity.

The impact of this bug is that the yield that belongs to other users will be diluted.

Recommended mitigation steps are to consider making ConcentratedLiquidityPosition.sol#burn() call position.pool.collect() before position.pool.burn(). The user will then need to call ConcentratedLiquidityPosition.sol#collect() to collect unclaimed fees after burn(). Alternatively, ConcentratedLiquidityPosition.sol#collect() can be changed to a public method and ConcentratedLiquidityPosition.sol#burn() can call it after position.pool.burn().

### Original Finding Content

_Submitted by WatchPug_

When a user calls `ConcentratedLiquidityPosition.sol#collect()` to collect their yield, it calcuates the yield based on `position.pool.rangeFeeGrowth()` and `position.feeGrowthInside0, position.feeGrowthInside1`:

[`ConcentratedLiquidityPosition.sol#L75` L101](https://github.com/sushiswap/trident/blob/c405f3402a1ed336244053f8186742d2da5975e9/contracts/pool/concentrated/ConcentratedLiquidityPosition.sol#L75-L101)

When there are enough tokens in `bento.balanceOf`, it will not call `position.pool.collect()` to collect fees from the pool.

This makes the user who `collect()` their yield when there is enough balance to get double yield when they call `burn()` to remove liquidity. Because `burn()` will automatically collect fees on the pool contract.

#### Impact
The yield belongs to other users will be diluted.

#### Recommended Mitigation Steps
Consider making `ConcentratedLiquidityPosition.sol#burn()` call `position.pool.collect()` before `position.pool.burn()`. User will need to call `ConcentratedLiquidityPosition.sol#collect()` to collect unclaimed fees after `burn()`.

Or `ConcentratedLiquidityPosition.sol#collect()` can be changed into a `public` method and `ConcentratedLiquidityPosition.sol#burn()` can call it after `position.pool.burn()`.

**[sarangparikh22 (Sushi) confirmed](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/53)**



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
- **GitHub**: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/53
- **Contest**: https://code4rena.com/reports/2021-09-sushitrident-2

### Keywords for Search

`vulnerability`

