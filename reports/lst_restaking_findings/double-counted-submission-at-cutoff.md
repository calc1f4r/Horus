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
solodit_id: 53584
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
github_link: none

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
  - Sigma Prime
---

## Vulnerability Title

Double-Counted Submission At Cutoff

### Overview

See description below for full details.

### Original Finding Content

## Description

If the first submission is triggered at `firstSubmissionTriggerCutoff`, then the rewards for the period ending at `firstSubmissionTriggerCutoff` can be double-counted. The first submission can be triggered at `firstSubmissionTriggerCutoff` due to the equality in the following check:

```javascript
if (block.timestamp <= firstSubmissionTriggerCutoff) {
    // ...
}
```

This will account for the rewards for the periods from `[firstSubmissionStartTimestamp, firstSubmissionTriggerCutoff)` (ending at `firstSubmissionTriggerCutoff - 1`). However, after the first submission, all subsequent submissions will count rewards only for the previous period:

```javascript
duration = CALCULATION_INTERVAL_SECONDS;
// find the correct startTimestamp.
// RewardsSubmissions must start at a multiple of CALCULATION_INTERVAL_SECONDS
uint32 calculationIntervalNumber = uint32(block.timestamp) / CALCULATION_INTERVAL_SECONDS;
// after rounding to the latest completed calculation interval to find the end, we subtract out the duration to get the start
startTimestamp = (calculationIntervalNumber * CALCULATION_INTERVAL_SECONDS) - duration;
```

This means that if `generateHopperActions()` is called at `firstSubmissionTriggerCutoff` and then at `firstSubmissionTriggerCutoff + 1`, the rewards for the period ending at `[firstSubmissionTriggerCutoff - CALCULATION_INTERVAL_SECONDS, firstSubmissionTriggerCutoff)` will be double-counted.

This issue has an informational rating, as the TokenHopper will be deployed with a cooldown period of 1 week, which is the same as `CALCULATION_INTERVAL_SECONDS`. This makes it impossible for `TokenHopper::pressButton()` to be called more than once in the same period and hence the double-counted rewards cannot be exploited.

## Recommendations

Remove the equality from the if statement in `generateHopperActions` in `RewardAllStakersActionGenerator.sol`:

```javascript
if (block.timestamp < firstSubmissionTriggerCutoff) {
    // ...
}
```

An alternative solution is to make sure the `firstSubmissionTriggerCutoff` is at the end of a period, instead of being at the start of a new period. This can be achieved by subtracting 1 from the current `firstSubmissionTriggerCutoff` value.

## Resolution

The EigenLayer team has removed the equality from the `firstSubmissionTriggerCutoff` check as recommended above. This issue has been resolved in commit `a554e28`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

