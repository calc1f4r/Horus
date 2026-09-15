---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57325
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 3
finders:
  - 0xshoonya
  - hard1k
  - oluwaseyisekoni
---

## Vulnerability Title

Incorrect Weight Scaling in `GaugeController` Leads to Inaccurate Time-Weighted Calculations

### Overview


The `GaugeController` has a bug that causes incorrect weight calculations, leading to inaccurate time-weighted calculations. This is a high-risk issue that affects all time-weighted calculations in the gauge system. The bug occurs because the `GaugeController` passes unscaled weight values to the `TimeWeightedAverage` library, which expects scaled values. This means that gauge weights are divided by 1e18 in all calculations, significantly undervaluing their impact. The bug can be fixed by scaling the weight values by 1e18 before passing them to the library. 

### Original Finding Content

## Summary

The `GaugeController`'s `addGauge` function incorrectly passes unscaled weight values to the `TimeWeightedAverage` library's `createPeriod` function, which expects weights to be scaled by 1e18. This scaling mismatch results in significantly undervalued time-weighted calculations for gauge weights.

## Vulnerability Details

In the `GaugeController` contract, gauges can be added with an initial weight of zero, which are then converted to a minimum weight of 1:

```js
function addGauge(
    address gauge,
    GaugeType gaugeType,
    uint256 initialWeight
) external onlyGaugeAdmin {
    // Zero weight is allowed and converted to 1
@>  uint256 periodWeight = initialWeight == 0 ? 1 : initialWeight;
    
    TimeWeightedAverage.createPeriod(
        period,
        block.timestamp,
        duration,
         // Uses unscaled value
        periodWeight,
        // Should be scaled by 1e18 
        periodWeight   
    );
}
```

The `TimeWeightedAverage` library's weight parameter in `createPeriod` expects values scaled by 1e18, as documented in the library. This scaling is crucial for precise time-weighted calculations similar to how Curve and Balancer handle weights in their gauge systems

```js
struct Period {
    // ...
    uint256 weight;   // Weight applied to period (scaled by 1e18)
}
```

However, the `GaugeController` passes the raw `periodWeight` value without scaling it by 1e18 for both the `initialValue` and `weight` parameters.

The same unscaled value is used for both parameters.
The `weight` parameter should be scaled by 1e18

This scaling mismatch means that gauge weights are effectively divided by 1e18 in all time-weighted calculations, severely undervaluing their impact.

## Impact

All time-weighted calculations in the gauge system are off by a factor of 1e18.

## Tools Used

Manual Review

## Recommendations

```js
function addGauge(
    address gauge,
    GaugeType gaugeType,
    uint256 initialWeight
) external onlyGaugeAdmin {
    // [...]
    uint256 baseWeight = initialWeight == 0 ? 1 : initialWeight;
    
     // Scale by 1e18
    uint256 scaledWeight = baseWeight * 1e18;
    
    TimeWeightedAverage.createPeriod(
        period,
        block.timestamp,
        duration,
        baseWeight, // Use unscaled value for initial value
        scaledWeight // Use scaled value for weight
    );
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | 0xshoonya, hard1k, oluwaseyisekoni |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

