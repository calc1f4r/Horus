---
# Core Classification
protocol: Conic Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29929
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#19-potential-delays-in-updatepoolweights-leading-to-unfair-reward-distribution-in-conic-pools
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Potential delays in `updatePoolWeights()` leading to unfair reward distribution in conic pools

### Overview


The bug report discusses an issue with the `InflationManager.updatePoolWeights()` function in the ConicFinance protocol. This function is responsible for updating the proportion of funds locked in different conic pools, which is used to determine the amount of CNC tokens to be minted for each pool. However, the current system does not have a reliable way to ensure that this function is called in a timely manner. It is currently only called from two places, one of which is not designed for frequent execution. The other place has a set time interval of 365 days, which can lead to delays and unfair distribution of rewards. The report recommends implementing a more frequent and automated mechanism for calling the `updatePoolWeights()` function to ensure fair distribution of rewards across conic pools.

### Original Finding Content

##### Description

`InflationManager.updatePoolWeights()` updates `currentPoolWeights` proportionally to the dollar-equivalent of funds locked in conic pools. This value is used in `getCurrentPoolInflationRate()` to determine how much CNC should be minted for a specific conic pool.

However, the system lacks guarantees for the timely invocation of `updatePoolWeights()`. Currently, this function is called from two places: `Controller.shutdownPool()` and `InflationManager._executeInflationRateUpdate()`.

`Controller.shutdownPool()` is not designed for frequent execution.

`InflationManager._executeInflationRateUpdate()` will trigger an update no more often than `_INFLATION_RATE_PERIOD = 365 days`:
```
function _executeInflationRateUpdate() internal {
    if (
        block.timestamp >= lastInflationRateDecay + _INFLATION_RATE_PERIOD
        ) {
        updatePoolWeights();
        currentInflationRate = 
            currentInflationRate.mulDown(_INFLATION_RATE_DECAY);
        lastInflationRateDecay = block.timestamp;
    }
}
```

- https://github.com/ConicFinance/protocol/blob/7a66d26ef84f93059a811a189655e17c11d95f5c/contracts/tokenomics/InflationManager.sol#L193-L200

This means that the `updatePoolWeights()` function must be called manually which can occur with a significant delay relative to the real distribution of funds in different conic pools. This will lead to an unfair distribution of rewards.

##### Recommendation

We recommend implementing an automated and more frequent mechanism for invoking the `updatePoolWeights()` function to ensure timely and fair distribution of rewards across conic pools.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Conic Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#19-potential-delays-in-updatepoolweights-leading-to-unfair-reward-distribution-in-conic-pools
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

