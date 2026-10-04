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
solodit_id: 29631
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
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

CLGauge.deposit() doesn't verify that the liquidity to stake is from the pool the gauge integrates with

### Overview


This report discusses a bug found in the CLGauge contract, which allows a malicious actor to stake liquidity from a fake pool and earn rewards from the CLGauge pool. The recommendation is to add a check in the deposit function to ensure that the staked NFT provides liquidity in the correct pool. The bug has been fixed in the Velodrome commit b3b0f8a1. An alternative fix has also been implemented by adding a new storage variable to the CLGauge contract and checking the token values during deposit. This has also been fixed in the Spearbit commit b3b0f8a1.

### Original Finding Content

## High Risk Vulnerability Report

**Severity:** High Risk  
**Context:** CLGauge.sol#L160  

## Description
`CLGauge.deposit()` allows staking an NFT that provides liquidity to a different pool (i.e., a pool the gauge doesn't integrate with). This allows a malicious actor to stake liquidity into a `CLGauge` from a fake `CLPool` and earn gauge rewards, stealing them from the liquidity providers of the gauge's pool.

## Recommendation
In `CLGauge.deposit()`, consider ensuring that the `tokenId` provides liquidity in the pool:
1. First, `CLGauge` needs to know the address of the `CLFactory` that deployed the pool.
2. Then, the values of `token0`, `token1`, and `tickSpacing` of the staked NFT's pool can be read from `NonfungiblePositionManager.positions()`.
3. Finally, the pool address can be computed using `PoolAddress.computeAddress()` and compared to the value of `pool`.

## Velodrome
The issue has been fixed in commit `b3b0f8a1`.  
As the `NonfungiblePositionManager`, `CLPoolFactory`, and `CLGauge` are bound to one another in a way that is immutable post-deployment, the following alternative fix was implemented:
- Adding a new storage variable to `CLGauge` that caches the pool's `tickSpacing`.
- On deposit, check that the position's `token0`, `token1`, and `tickSpacing` values match with the same values stored in the gauge, with a revert otherwise.

## Spearbit
Fixed in commit `b3b0f8a1`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

