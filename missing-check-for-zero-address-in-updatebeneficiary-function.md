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
solodit_id: 43842
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Genesis%20Staking/README.md#3-missing-check-for-zero-address-in-updatebeneficiary-function
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

Missing Check for Zero Address in `updateBeneficiary` Function

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified in the `updateBeneficiary` function of the `Prestaking` contract.
The function allows the current beneficiary to update the wallet that will receive the staked tokens. However, there is no check to ensure that the `newBeneficiary` address is not the zero address.
##### Recommendation
We recommend adding a validation check to ensure that the `newBeneficiary` address is not the zero address (`require(newBeneficiary != address(0), "Beneficiary cannot be zero address.");`) before updating the staking wallet's beneficiary.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Genesis%20Staking/README.md#3-missing-check-for-zero-address-in-updatebeneficiary-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

