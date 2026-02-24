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
solodit_id: 57214
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
finders_count: 1
finders:
  - amow
---

## Vulnerability Title

Gauge emissions revert when emissions are higher than the leftover buffer instead of depositing the difference

### Overview


The report discusses a bug in the Gauge reward distribution system, where instead of filling the buffer, the emissions are reverted when they are higher than the leftover buffer. This results in a loss of rewards for gauge voters and stakers. The bug occurs because the amount being supplied is checked against the state max emission, which is incorrect as the amount fluctuates constantly based on gauges' weights. The impact of this bug is a loss of rewards and a logic error. To mitigate this, the buffer should be filled instead of reverting the emissions.

### Original Finding Content

## Summary

Gauge reward distribution will fail instead of filling the buffer, despite the gauge being eligible for the buffer

## Details

Whenever `distributeRewards` is called in `GaugeController.sol`, fixed emissions are split across all active gauges, according to their weight

```solidity
    function _calculateReward(address gauge) internal view returns (uint256) {
        Gauge storage g = gauges[gauge];
        uint256 totalWeight = getTotalWeight();
        if (totalWeight == 0) return 0;
        uint256 gaugeShare = (g.weight * WEIGHT_PRECISION) / totalWeight;
        uint256 typeShare = (typeWeights[g.gaugeType] * WEIGHT_PRECISION) / MAX_TYPE_WEIGHT;
        
        uint256 periodEmission = g.gaugeType == GaugeType.RWA ? _calculateRWAEmission() : _calculateRAACEmission();
        return (periodEmission * gaugeShare * typeShare) / (WEIGHT_PRECISION * WEIGHT_PRECISION);
    }
```

Afterwards, the gauge receives it's rewards through `notifyRewardAmount`. During the execution, the amount being supplied is checked whether it surpasses the state max emission

```solidity
        if (amount > maxEmission) revert RewardCapExceeded();
    @>  if (amount + state.distributed > state.emission) {
            revert RewardCapExceeded();
        }
```

This is incorrect since `amount` is an arbitrary number which fluctuates constantly based on gauges' weights. There is no guarantee that all `notifyRewardAmount` calls will always sum up perfectly.
An example:

1. Gauge has `state.emission = 2000`, `state.distributed = 1500`, all previous emissions supplied in 500 token increments
2. Gauge's weight increases (due to user voting) and is now eligible for `rewards = 550`
3. `distributeRewards` is called, 550 tokens are attempted to be sent to the gauge, yet it reverts in the snippet above since `550 + 1500 > 2000`

Gauges will hardly ever hit their max emissions, despite being eligible to do so. These rewards are lost for the gauge voters and stakers.

## Impact

Loss of rewards, logic error

## Mitigation

Instead of reverting, fill the buffer

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | amow |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

