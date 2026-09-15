---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29638
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
github_link: none

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

protocol_categories:
  - dexes
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Jeiwan
  - Alex The Entreprenerd
  - Optimum
  - D-Nice
---

## Vulnerability Title

NFT cannot be withdrawn after all liquidity was removed from the position

### Overview


This bug report discusses an issue in the CLGauge contract where withdrawing liquidity from a position can fail and result in the NFT position being locked in the contract. This happens when all liquidity has been removed using CLGauge.decreaseStakedLiquidity() and then CLGauge.withdraw() is called. The error occurs because a function called Position.update() fails when the position has 0 liquidity and the liquidityDelta is also 0. The report recommends fixing this issue by skipping a certain function call in CLGauge.withdraw() when the liquidityToStake is 0. The fix has been implemented in a recent commit by Velodrome and Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
- `CLGauge.sol#L280`
- `CLPool.sol#L539`
- `Position.sol#L55`

## Description
`CLGauge.withdraw()` fails when all liquidity from a position has been removed using `CLGauge.decreaseStakedLiquidity()`. The NFT position remains locked in the Gauge contract and cannot be removed until some new liquidity is provided.

The error happens because `Position.update()` fails when a position has 0 liquidity and the `liquidityDelta` is also 0:

```solidity
if (liquidityDelta == 0) {
    require(_self.liquidity > 0, "NP"); // disallow pokes for 0 liquidity positions
    liquidityNext = _self.liquidity;
    // ...
}
```

Calling `CLGauge.withdraw()` on an empty position triggers `CLPool.stake()` with the value of `stakedLiquidity - Delta` equal to 0, which calls `update()` on the empty Gauge's position and also passes 0 in the `liquidityDelta` parameter.

## Recommendation
In `CLGauge.withdraw()`, consider skipping the call to `pool.stake()` when `liquidityToStake` is 0.

## Velodrome
The recommended fix has been applied in commit `5c0eae52` (i.e. if the position is empty, a call to `pool.stake()` will be skipped).

## Spearbit
Fixed as recommended in commit `5c0eae52`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | Jeiwan, Alex The Entreprenerd, Optimum, D-Nice |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf

### Keywords for Search

`vulnerability`

