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
solodit_id: 29633
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
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

UniswapV2Library.getAmountIn uses hardcoded fees, but Velodrome Pools have custom fees

### Overview


The bug report states that there is a medium risk bug in the UniswapV2Library.sol file, specifically in lines 121-132. The function getAmountIn is not accounting for custom fees set by the factory, which may cause incorrect calculations. The recommendation is to add functionality to adapt to custom fees and this issue has been fixed in a commit by Velodrome. Spearbit has also fixed the bug by passing the pair and factory to the getAmountIn and getAmountOut functions.

### Original Finding Content

## Severity: Medium Risk

## Context
`UniswapV2Library.sol#L121-L132`

## Description
The `getAmountIn` function uses fees to determine the necessary `amountIn` to receive a given `amountOut` (refer to `UniswapV2Library.sol#L121-L132`):

```solidity
function getAmountIn(uint256 amountOut, uint256 reserveIn, uint256 reserveOut, Route memory route)
internal
view
returns (uint256 amountIn)
{
    if (reserveIn == 0 || reserveOut == 0) revert InvalidReserves();
    if (!route.stable) {
        amountIn = (amountOut * 1000 * reserveIn) / ((reserveOut - amountOut) * 997) + 1;
    } else {
        revert StableExactOutputUnsupported();
    }
}
```

This function is cognizant of fees (997), but the fees are hardcoded. This may cause the math to be incorrect since the Pool allows custom fees to be set via the factory (see `Pool.sol#L372-L373`):

```solidity
if (amount0In > 0) _update0((amount0In * IPoolFactory(factory).getFee(address(this), stable)) / 10000);
// accrue fees for token0 and move them out of pool
if (amount1In > 0) _update1((amount1In * IPoolFactory(factory).getFee(address(this), stable)) / 10000);
```

## Recommendation
Consider whether the router needs to support all pools, and add functionality to adapt to custom fees.

## Velodrome
Support for custom fees on v2 pools has been added in commit `f6185838`.

## Spearbit
Fixed by passing pair and factory to `getAmountIn` and `getAmountOut`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
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

