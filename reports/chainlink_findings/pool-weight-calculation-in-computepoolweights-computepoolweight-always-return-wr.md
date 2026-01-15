---
# Core Classification
protocol: OpalProtocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54299
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007
source_link: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
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
finders_count: 3
finders:
  - 8olidity
  - kustrun
  - pks271
---

## Vulnerability Title

Pool weight calculation in computepoolweights /computepoolweight always return wrong an- swer because totalusdvalue returns 0 

### Overview


The bug report describes an issue in the OmnipoolController.sol code, specifically in the calculation of the pool's weight. The code uses the `Price-Feed.getUSDPrice` function to get the pool's underlying token, but this function always returns a value much smaller than the actual price. As a result, the `totalUSDValue` always returns 0, leading to an incorrect `poolWeight` calculation. The recommendation is to use `bptOracle.getUSDPrice` instead of `priceFeed.getUSDPrice` to fix the issue.

### Original Finding Content

## Context
OmnipoolController.sol#L313

## Description
When calculating the pool's weight, it first gets the pool's `underlyingToken` by calling `Price-Feed.getUSDPrice`:

```solidity
function getUSDPrice(address token) public view returns (uint256) {
    IOracle priceFeed = _priceFeedMapping[token];
    uint256 decimals = IERC20Metadata(token).decimals();
    if (address(priceFeed) == address(0)) revert PriceFeedNotFound();
    (, int256 price,,,) = priceFeed.latestRoundData();
    return uint256(price / int256(10 ** decimals));
}
```

The return data is always much smaller than the actual price. Then `currentPool.getTotalUnderlying()` returns the total number of underlying Balancer pools, and `convertScale` will format the result with decimals. `ScaledMath.mulDown` is equal to `a * b / 1e18`.

For example, if the underlying token is USDC and the decimal is 6, `currentPool.getTotalUnderlying()` returns 3, and the price = (ChainLink USDC price / 1e6) = 1e8 / 1e6 = 100 (the ChainLink return price decimals is 1e8). Thus:

```
usdValue = 3 * 1e12 * 100 / 1e18 == 0
```

The `totalUSDValue` always returns 0, so `poolWeight` will always return `ScaledMath.ONE / pools.length`, which is obviously a wrong answer.

## Recommendation
Use `bptOracle.getUSDPrice` instead of `priceFeed.getUSDPrice`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OpalProtocol |
| Report Date | N/A |
| Finders | 8olidity, kustrun, pks271 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007

### Keywords for Search

`vulnerability`

