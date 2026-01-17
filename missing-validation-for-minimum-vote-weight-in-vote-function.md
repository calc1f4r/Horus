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
solodit_id: 57256
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 11
finders:
  - 0xw3
  - 0xdarko
  - cipherhawk
  - xcrypt
  - 0xshoonya
---

## Vulnerability Title

Missing Validation for Minimum Vote Weight in `vote` Function

### Overview

See description below for full details.

### Original Finding Content

## Summary

The `GaugeController.sol` contract defines a `MIN_VOTE_WEIGHT` constant, which sets the minimum allowable vote weight. However, the `vote` function does not enforce this constraint, allowing users to submit votes with a weight below the minimum requirement. This could lead to unintended behavior and manipulation of gauge voting.

## Vulnerability Details

The  `vote`  function takes a `weight` parameter but only validates that:

1. The `gauge` exists (`isGauge(gauge)`).

2. The `weight` does not exceed `WEIGHT_PRECISION`.

3. The caller has voting power (`veRAACToken.balanceOf(msg.sender) > 0`).

\[[https://github.com/Cyfrin/2025-02-raac/blob/89ccb062e2b175374d40d824263a4c0b601bcb7f/contracts/core/governance/gauges/GaugeController.sol#L190 ](https://github.com/Cyfrin/2025-02-raac/blob/89ccb062e2b175374d40d824263a4c0b601bcb7f/contracts/core/governance/gauges/GaugeController.sol#L190)]

```JavaScript

function vote(address gauge, uint256 weight) external override whenNotPaused {
        if (!isGauge(gauge)) revert GaugeNotFound();
    //  @audit-issue : Missing check for weight should not be less then MIN_VOTE_WEIGHT
  @->    if (weight > WEIGHT_PRECISION) revert InvalidWeight();
        
        uint256 votingPower = veRAACToken.balanceOf(msg.sender);
        if (votingPower == 0) revert NoVotingPower();

        uint256 oldWeight = userGaugeVotes[msg.sender][gauge];
        userGaugeVotes[msg.sender][gauge] = weight;
        
        _updateGaugeWeight(gauge, oldWeight, weight, votingPower);
        
        emit WeightUpdated(gauge, oldWeight, weight);
  
```

* **Missing Check:** The function does **not** verify that `weight` is at least `MIN_VOTE_WEIGHT`.

  ```JavaScript
  if (weight < MIN_VOTE_WEIGHT) revert WeightTooLow();
  ```

## Impact

A user could submit a vote with `weight = 0` or any value below `MIN_VOTE_WEIGHT`, which:

* Might cause **unexpected distribution of votes**.
* Could be exploited for **strategic voting manipulation**.
* Might allow users to **artificially shift voting results** with low-impact votes.

## Tools Used

Manual Review.

## Recommendations

Modify the `vote` function to include a **minimum weight check**:

```diff
function vote(address gauge, uint256 weight) external override whenNotPaused {
        if (!isGauge(gauge)) revert GaugeNotFound();
        if (weight > WEIGHT_PRECISION) revert InvalidWeight();
++      if (weight < MIN_VOTE_WEIGHT) revert WeightTooLow();
        
        uint256 votingPower = veRAACToken.balanceOf(msg.sender);
        if (votingPower == 0) revert NoVotingPower();

        uint256 oldWeight = userGaugeVotes[msg.sender][gauge];
        userGaugeVotes[msg.sender][gauge] = weight;
        
        _updateGaugeWeight(gauge, oldWeight, weight, votingPower);
        
        emit WeightUpdated(gauge, oldWeight, weight);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | 0xw3, 0xdarko, cipherhawk, xcrypt, 0xshoonya, josh4324, whitekittyhacker, recur, falendar, mahivasisth, 0xbc000 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

