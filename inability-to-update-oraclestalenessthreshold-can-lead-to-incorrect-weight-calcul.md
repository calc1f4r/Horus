---
# Core Classification
protocol: QuantAMM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49712
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm4qsgohz00002pfyew98t8u4
source_link: none
github_link: https://github.com/Cyfrin/2024-12-quantamm

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - tejaswarambhe
---

## Vulnerability Title

Inability to update `oracleStalenessThreshold` can lead to incorrect weight calculations

### Overview

See description below for full details.

### Original Finding Content

## Summary

The [`QuantAMMWeightedPool::oracleStalenessThreshold`](https://github.com/Cyfrin/2024-12-quantamm/blob/a775db4273eb36e7b4536c5b60207c9f17541b92/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L167) cannot be updated due to lack of a setter function inside `QuantAMMWeightedPool.sol`, which will lead to an incorrect `oracleStalenessThreshold` in case of `heartbeat`/`deviation` change by chainlink or due to any requirement of the protocol.

## Vulnerability Details

The [`QuantAMMWeightedPool::oracleStalenessThreshold`](https://github.com/Cyfrin/2024-12-quantamm/blob/a775db4273eb36e7b4536c5b60207c9f17541b92/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L167) is set inside the [`QuantAMMWeightedPool::initialize`](https://github.com/Cyfrin/2024-12-quantamm/blob/a775db4273eb36e7b4536c5b60207c9f17541b92/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L712) when the pool is deployed.

```solidity
    function initialize(
        int256[] memory _initialWeights,
        PoolSettings memory _poolSettings,
        int256[] memory _initialMovingAverages,
        int256[] memory _initialIntermediateValues,
        uint _oracleStalenessThreshold
    ) public initializer {
        // . . . Rest of the code . . .
        oracleStalenessThreshold = _oracleStalenessThreshold;
        // . . . Rest of the code . . .
    }
```

There's no other way to set this threshold again due to lack of a setter function. The rationale behind determining a `oracleStalenessThreshold` includes but not limited to `heartbeat` and `deviation`.
It's public info as well as chainlink team confrimed this in the public discord that a price feed's `heartbeat` and `deviation` can be changed as per demand and volatility, which has been done in past to several pairs, below text is by the official from the public discord channel of chainlink (reference to the **public** chat can be provided when asked, not providing here to avoid revealing anonimity)

```text
Q: I have a question, has it ever happened in past where a pair had let's say X% of deviation and Y seconds of heartbeat, was any of X or Y here was ever changed for improvement or some other purposes.
A: I think, Yes, Chainlink price feed settings like deviation thresholds and heartbeat intervals can be adjusted based on market demand, user needs, or customized for specific projects. Chainlink Data Feeds are regularly updated to add new features or handle changes like token migrations, protocol rebrands, or extreme market events. These updates, including aggregator changes, ensure smooth operation through proxies.
```

```text
Q: How do I as a smart contract developer mitigate this, as one way I was thinking of doing is to have a staleness threshold inside the smart contract itself, do I keep it updatable via a setter function?
A: I think yes, you can add a setter function in your smart contract to define a staleness threshold, like checking against X seconds for price updates. Alternatively, compare the current price and new price, and if the difference exceeds X%, reject the update. This ensures your protocol only consumes prices that meet your conditions.
```

Along with this, We can also consider the fact that the rationale of using certain threshold at the time of deployment is no longer valid after certain time has been passed.
The current contract clearly lacks a setter function required to mitigate this, this would allow stale values and incorrect circuit breaking.

## Impact

1. Incorrect staleness threshold would be used as it would not align with the `heartbeat` or `deviation` or any criteria which the protocol even intended to impose as it's immuatable now, leading to improper weights calculation which is done at intervals, eventually allowing loss of funds.
2. Incorrect circuit breaking would take place here, which breaks the purpose of having a `oracleStalenessThreshold`.

## Tools Used

Manual Review

## Recommendations

It is recommended to add a setter function for `oracleStalenessThreshold` inside the `QuantAMMWeightedPool.sol`

```solidity
    function setOracleStalenessThreshold(uint _oracleStalenessThreshold) external {
        require(msg.sender == quantammAdmin, "ONLYADMIN");
        oracleStalenessThreshold = _oracleStalenessThreshold;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | QuantAMM |
| Report Date | N/A |
| Finders | tejaswarambhe |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-12-quantamm
- **Contest**: https://codehawks.cyfrin.io/c/cm4qsgohz00002pfyew98t8u4

### Keywords for Search

`vulnerability`

