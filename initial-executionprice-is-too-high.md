---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6742
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - derivatives

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Emanuele Ricci
  - Christoph Michel
  - Rusty (f7dd60e9cfad19996d73)
  - Gerard Persoon
---

## Vulnerability Title

Initial executionPrice is too high

### Overview


This bug report is about the PoolKeeper.sol#L73 code. When a pool is deployed, the initial executionPrice is calculated as firstPrice * 1e18, where firstPrice is ILeveragedPool(_poolAddress).getOraclePrice() and all other updates to executionPrice use the result of getPriceAndMetadata() directly without scaling. The problem is that the price after the firstPrice will always be lower, resulting in funding rate payment to the shorts and a loss for the long pool token holders.

The recommendation is to remove the 1e18 scaling for the initial executionPrice. The code should be changed from: int256 startingPrice = ABDKMathQuad.toInt(ABDKMathQuad.mul(ABDKMathQuad.fromInt(firstPrice), FIXED_POINT)); , ! to int256 startingPrice = firstPrice;

The bug has been fixed in commit 445377f, and has been acknowledged by Spearbit.

### Original Finding Content

## High Risk Vulnerability Report

## Severity
**High Risk**

## Context
**File:** PoolKeeper.sol  
**Line:** L73

## Description
When a pool is deployed, the initial `executionPrice` is calculated as `firstPrice * 1e18`, where `firstPrice` is retrieved using the `ILeveragedPool(_poolAddress).getOraclePrice()`:

```solidity
contract PoolKeeper is IPoolKeeper, Ownable {
    function newPool(address _poolAddress) external override onlyFactory {
        int256 firstPrice = ILeveragedPool(_poolAddress).getOraclePrice();
        int256 startingPrice = ABDKMathQuad.toInt(ABDKMathQuad.mul(ABDKMathQuad.fromInt(firstPrice), FIXED_POINT));
        executionPrice[_poolAddress] = startingPrice;
    }
}
```

All other updates to `executionPrice` use the result of `getPriceAndMetadata()` directly without scaling:

```solidity
function performUpkeepSinglePool() {
    ...
    (int256 latestPrice, ...) = pool.getUpkeepInformation();
    ...
    executionPrice[_pool] = latestPrice;
    ...
}
```

```solidity
contract LeveragedPool is ILeveragedPool, Initializable, IPausable {
    function getUpkeepInformation() {
        (int256 _latestPrice, ...) = IOracleWrapper(oracleWrapper).getPriceAndMetadata();
        return (_latestPrice, ...);
    }
}
```

The price after `firstPrice` will always be lower, therefore its funding rate payment will always go to the shorts and long pool token holders will incur a loss.

## Recommendation
The `1e18` scaling should be removed for the initial `executionPrice`:

```solidity
- int256 startingPrice = ABDKMathQuad.toInt(ABDKMathQuad.mul(ABDKMathQuad.fromInt(firstPrice), FIXED_POINT));
+ int256 startingPrice = firstPrice;
```

## Tracer
Valid. Fixed in commit `445377f`.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | Emanuele Ricci, Christoph Michel, Rusty (f7dd60e9cfad19996d73), Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

