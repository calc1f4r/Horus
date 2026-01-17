---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43844
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Genesis%20Staking/README.md#5-missing-validation-for-newendtime-in-updateenddeposittime-function
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
  - MixBytes
---

## Vulnerability Title

Missing Validation for `newEndTime` in `updateEndDepositTime` Function

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified in the `updateEndDepositTime` function of the `Prestaking` contract.
The function currently allows updating the `endDepositTime` without validating whether the new time is between the `startDepositTime` and `releaseTime` of the epoch.
##### Recommendation
We recommend adding validation to ensure that `newEndTime` is between the `startDepositTime` and `releaseTime` of the epoch.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Genesis%20Staking/README.md#5-missing-validation-for-newendtime-in-updateenddeposittime-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

