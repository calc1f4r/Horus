---
# Core Classification
protocol: MetaLeX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43880
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#12-missing-validation-for-vestingstarttime-and-unlockstarttime-in-all-the-allocations-contracts-constructor
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

Missing Validation for `vestingStartTime` and `unlockStartTime` in All the Allocation's Contracts' Constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified in the constructor of all the allocation's contracts. The `vestingStartTime` and `unlockStartTime` fields are not checked to ensure that they are not set to values in the past or to unreasonably distant future dates.
##### Recommendation
We recommend implementing validation  checks to ensure that both `vestingStartTime` and `unlockStartTime` are set within a reasonable range — not earlier than the current timestamp and not in the distant future — to maintain predictable and secure vesting behavior.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | MetaLeX |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#12-missing-validation-for-vestingstarttime-and-unlockstarttime-in-all-the-allocations-contracts-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

