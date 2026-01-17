---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53581
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

First Submission Can Be Triggered Multiple Times

### Overview


The bug report states that the first submission multiplier can be applied multiple times if a certain function is called repeatedly before a specific cutoff time. This happens because the function does not keep track of whether the initial submission has been made and relies on the cutoff time to determine if it should be counted as the first submission. To fix this, the team recommends checking the configurations and deployment times and changing the function to take in a parameter to track if it is the first submission. The team has resolved the issue in a code update.

### Original Finding Content

## Description

The first submission multiplier can be applied multiple times if `TokenHopper.pressButton()` is called repeatedly before reaching the `firstSubmissionTriggerCutoff`. This occurs because the `generateHopperActions()` is view-only and does not maintain state of whether the initial submission has been made. Instead, it relies on the `firstSubmissionTriggerCutoff` to determine if the current submission should be treated as the first one:

```solidity
if (block.timestamp <= firstSubmissionTriggerCutoff) {
    // ...
}
```

`TokenHopper::pressButton()` is called on a cooldown that is set during deployment in the `HopperConfiguration` struct. Depending on the time of deployment, the configured cooldown, and the `firstSubmissionTriggerCutoff`, it may be possible to submit rewards multiple times before `firstSubmissionTriggerCutoff`, allowing for these subsequent submissions to distribute more EIGEN tokens than intended due to the multiple calculation:

```solidity
uint32 multiple = (uint32(block.timestamp) - firstSubmissionStartTimestamp) / CALCULATION_INTERVAL_SECONDS;
duration = CALCULATION_INTERVAL_SECONDS * multiple;
startTimestamp = firstSubmissionStartTimestamp;
amountsToUse[0] = amounts[0] * multiple;
amountsToUse[1] = amounts[1] * multiple;
```

## Recommendations

Ensure that the configurations and deployment times of both `TokenHopper` and `RewardAllStakersActionGenerator` are correct such that `TokenHopper::pressButton()` can only be called once before and up to `firstSubmissionTriggerCutoff`. An alternative fix involves changing the behaviour of the `generateHopperActions()` function such that it takes in a `boolean isFirstSubmission` parameter instead of relying on a timestamp cutoff. The `TokenHopper` would also need to keep track of whether `pressButton()` has been previously called to generate the correct hopper actions.

## Resolution

The EigenLayer team has ensured that the first submission can only be triggered once by requiring in the deployment script that the `TokenHopper` start time is at most 1 week before the `firstSubmissionTriggerCutoff`. This issue has been resolved in commit `9cf6f41`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf

### Keywords for Search

`vulnerability`

