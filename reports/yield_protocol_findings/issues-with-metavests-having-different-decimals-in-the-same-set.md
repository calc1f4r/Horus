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
solodit_id: 43858
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#5-issues-with-metavests-having-different-decimals-in-the-same-set
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
  - MixBytes
---

## Vulnerability Title

Issues with MetaVesTs Having Different Decimals in the Same Set

### Overview


The bug report states that there is an issue with the calculation of governing power for MetaVesTs with different decimals in the same set. This results in an incorrect voting process and may lead to errors when using certain functions. The bug is classified as high priority and the recommendation is to not allow MetaVesTs with different decimals in the same set.

### Original Finding Content

##### Description
If MetaVesTs with different decimals are included in the same set, MetaVesTs with higher decimals will have an exponential advantage over those with lower decimals [during the calculation of the governing power](https://github.com/MetaLex-Tech/MetaVesT/blob/b614405e60bce8b852e46d06c03fd47b04d86dde/src/MetaVesTController.sol#L583-L589), resulting in an incorrect voting process. Additionally, using `updateExerciseOrRepurchasePrice()`, `updateMetavestUnlockRate()`, and `updateMetavestVestingRate()` in the case of sets with different decimals may lead to errors. 

This issue is classified as **High**, as the voting functionality works incorrectly in certain cases, and fixing it requires redeployment.

##### Recommendation
We recommend prohibiting the inclusion of MetaVesTs with different decimals in the same set.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | MetaLeX |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#5-issues-with-metavests-having-different-decimals-in-the-same-set
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

