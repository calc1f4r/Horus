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
solodit_id: 53583
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

Incorrect newCooldownHorizon Calculation

### Overview

See description below for full details.

### Original Finding Content

## Description
The calculation for `newCooldownHorizon` in the `pressButton()` function does not add back `configuration.startTime` after calculating the number of seconds since the start time, resulting in a `newCooldownHorizon` value that is too small.

```solidity
uint256 newCooldownHorizon =
    ((block.timestamp - configuration.startTime) / configuration.cooldownSeconds + 1) * configuration.cooldownSeconds;
```

## Recommendations
Fix the calculation to add back `configuration.startTime` after calculating the number of seconds since the start time.

```solidity
uint256 newCooldownHorizon =
    ((block.timestamp - configuration.startTime) / configuration.cooldownSeconds + 1) * configuration.cooldownSeconds +
    configuration.startTime;
```

## Resolution
The EigenLayer team has implemented the recommended fix in commit 3084969.

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

