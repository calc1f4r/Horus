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
solodit_id: 43837
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Genesis%20Staking/README.md#1-missing-validation-for-input-parameters-in-createnewepoch-function
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

Missing Validation for Input Parameters in `createNewEpoch` Function

### Overview


The `createNewEpoch` function in the `Prestaking` contract has a bug where input parameters are not properly checked. This can cause issues such as incorrect configurations, indefinite token lockups, and excessive yields. To fix this, validation checks should be added for each of the input parameters. This will ensure the correct initialization of epochs and prevent any unintended behavior.

### Original Finding Content

##### Description
This issue has been identified in the `createNewEpoch` function of the `Prestaking` contract.
The input parameters for creating a new epoch are not validated, which could lead to incorrect or unintended initialization. Specifically:
- `newStartDepositTime` should be greater than or equal to `block.timestamp`.
- `newEndDepositTime` should be greater than `newStartDepositTime`.
- The sum of `newEndDepositTime` and `newDuration` should not be set too far in the future to prevent indefinite token lockups.
- `newBasisPoints` should be capped at a reasonable maximum value to avoid excessively high yields.
Without these checks, it could lead to epochs with incorrect or undesirable configurations that might lock tokens indefinitely or apply excessive yields.
The issue is classified as **Medium** severity because it affects the integrity of the prestaking process and could lead to operational issues for both the contract and its users.
##### Recommendation
We recommend adding validation checks for each of the input parameters to ensure:
- `newStartDepositTime >= block.timestamp`;
- `newEndDepositTime > newStartDepositTime`;
- `newEndDepositTime + newDuration` is not too far in the future;
- `newBasisPoints` is capped at a reasonable maximum.
This will ensure the correct initialization of epochs and prevent unintended behavior.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Genesis%20Staking/README.md#1-missing-validation-for-input-parameters-in-createnewepoch-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

