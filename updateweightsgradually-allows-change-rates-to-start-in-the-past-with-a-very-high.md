---
# Core Classification
protocol: Gauntlet
chain: everychain
category: uncategorized
vulnerability_type: update_state_after_admin_action

# Attack Vector Details
attack_type: update_state_after_admin_action
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7092
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
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
  - update_state_after_admin_action

protocol_categories:
  - dexes
  - cdp
  - yield
  - insurance
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Emanuele Ricci
  - Eric Wang
  - Gerard Persoon
---

## Vulnerability Title

updateWeightsGradually allows change rates to start in the past with a very high maximumRatio

### Overview


This bug report is about the AeraVaultV1.sol in which the function updateWeightsGradually is using startTime instead of the minimal start time that should be Math.max(block.timestamp, startTime). This allows the startTime to be in the past and targetWeights[i] to be higher than allowed. The recommendation is to update the code to correctly initialize the startTime value and add a check to prevent having endTime in the past (startTime > endTime). A possible solution is provided in the report. The recommendation is tested in PR #146 and acknowledged.

### Original Finding Content

## Severity: High Risk

## Context
AeraVaultV1.sol#L599-L639

## Description
The current `updateWeightsGradually` is using `startTime` instead of the minimal start time that should be `Math.max(block.timestamp, startTime)`. Because internally Balancer will use `startTime = Math.max(currentTime, startTime);` as the `startTime`, this allows for:

- Having a `startTime` in the past.
- Having a `targetWeights[i]` higher than allowed.

We also suggest adding another check to prevent `startTime > endTime`. Although Balancer replicates the same check, it is still needed in the Aera implementation to prevent transactions from reverting because of an underflow error on 

```solidity
uint256 duration = endTime - startTime;
```

## Recommendation
Update the code to correctly initialize the `startTime` value and add a check to prevent having `endTime` in the past (`startTime > endTime`). A possible solution looks as follows:

```solidity
function updateWeightsGradually( ... ) ... {
    startTime = Math.max(block.timestamp, startTime);
    if (startTime > endTime) {
        revert Aera__WeightChangeEndBeforeStart();
    }
    if (
        Math.max(block.timestamp, startTime) +
        MINIMUM_WEIGHT_CHANGE_DURATION > endTime
    ) {
        revert Aera__WeightChangeDurationIsBelowMin(
            endTime - startTime, // no longer reverts
            MINIMUM_WEIGHT_CHANGE_DURATION
        );
    }
    ...
}
```

## Gauntlet
Recommendation implemented in PR #146

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Gauntlet |
| Report Date | N/A |
| Finders | Emanuele Ricci, Eric Wang, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf

### Keywords for Search

`Update State After Admin Action`

