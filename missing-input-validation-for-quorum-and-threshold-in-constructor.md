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
solodit_id: 43528
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/Borg/README.md#70-missing-input-validation-for-quorum-and-threshold-in-constructor
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

Missing Input Validation for `quorum` and `threshold` in Constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified within the constructor of the `daoVetoImplant` and `daoVoteImplant` contracts.
The constructor does not validate the input parameters `_quorum` and `_threshold`. Lack of validation could lead to invalid or nonsensical values (e.g., a quorum or threshold exceeding 100%) being set, which could disrupt the governance process or make proposal execution impossible.
##### Recommendation
We recommend adding input validation checks to ensure that `_quorum` and `_threshold` are within appropriate ranges (e.g., between 0 and 100).

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/Borg/README.md#70-missing-input-validation-for-quorum-and-threshold-in-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

