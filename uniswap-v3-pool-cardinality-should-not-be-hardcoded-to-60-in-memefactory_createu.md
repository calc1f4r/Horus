---
# Core Classification
protocol: Valory
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46169
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7787c839-f921-4897-ab2e-8cbc9a5f131c
source_link: https://cdn.cantina.xyz/reports/cantina_olas_december2024.pdf
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0x4non
  - MiloTruck
---

## Vulnerability Title

Uniswap V3 pool cardinality should not be hardcoded to 60 in MemeFactory._createUniswap- Pair() 

### Overview


Summary:

The bug report is about an issue in the MemeFactory contract where a hardcoded value of 60 is used to increase the observation cardinality of a Uniswap V3 pool. This causes two problems - the cardinality is too small and it is the same for all chains. The recommendation is to use a virtual function to set the appropriate cardinality for each chain. The bug has been fixed in a pull request and smaller cardinality values have been implemented to maintain reasonable gas costs. The team can manually change the cardinality in the future if needed. 

### Original Finding Content

## Context: MemeFactory.sol#L229

## Description
In `MemeFactory._createUniswapPair()`, whenever a new Uniswap V3 pool is created, `increaseObservationCardinalityNext()` is called with a hardcoded value of 60:

```solidity
// Increase observation cardinality
IUniswapV3(pool).increaseObservationCardinalityNext(60);
```

However, this leads to two issues:
1. A cardinality of 60 is too small.
2. Cardinality should not be hardcoded to the same value across different chains.

Calling `increaseObservationCardinalityNext()` increases the cardinality of the pool, which is the maximum number of observations that can be stored. Considering that an observation is stored at most once per block, the cardinality of the pool must be large enough to cover the desired TWAP window when `observe()` is called (i.e., should be at least `twapWindowSeconds / secondsPerBlock`).

### Issue (1)
Base produces a block every 2 seconds. Assuming an observation is stored every block, setting cardinality = 60 limits the oldest observation to `2 * 60 = 120` seconds ago, which is extremely short and susceptible to manipulation.

### Issue (2)
The cardinality should be set depending on the block time of each chain. Since `BuyBackBurner` uses an observation window of 1800 seconds (`BuyBackBurner.sol#L57-L58`), the minimum cardinality for Base and Celo should be:
- **Base** - `1800 / 2 = 900`.
- **Celo** - `1800 / 5 = 360`.

## Recommendation
Consider calling `increaseObservationCardinalityNext()` with a virtual `_observationCardinalityNext()` function that is overridden in `MemeBase` and `MemeCelo` to return the appropriate values:

```solidity
// Increase observation cardinality
- IUniswapV3(pool).increaseObservationCardinalityNext(60);
+ IUniswapV3(pool).increaseObservationCardinalityNext(_observationCardinalityNext());
```

## Valory
Fixed in PR 110. Since calling `increaseObservationCardinalityNext()` with a large cardinality costs a huge amount of gas (e.g., cardinality = 900 for Base as recommended above would exceed the block gas limit), we have decided to go with the following values for `_observationCardinalityNext()`:
- **Arbitrum**: 240.
- **Base**: 120.
- **All other chains**: 60.

## Cantina Managed
**Verified**. The recommendation above has been implemented with smaller cardinality values to maintain reasonable gas costs. This is an acceptable risk as it still leaves a minimum observation window of 240 seconds, and the TWAP oracle would be non-trivial to manipulate.

Additionally, the currently deployed contracts on Base and Celo, which have their cardinality set to 60, have a minimum observation window of 120 seconds, which is considered acceptable.

As a last resort, should the team decide that the current cardinality values are too small in the future, they can directly call `increaseObservationCardinalityNext()` of the respective Uniswap V3 pool.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Valory |
| Report Date | N/A |
| Finders | 0x4non, MiloTruck |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_olas_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7787c839-f921-4897-ab2e-8cbc9a5f131c

### Keywords for Search

`vulnerability`

