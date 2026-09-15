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
solodit_id: 57927
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#3-stakingindicesbyprincipalunstaker-mapping-not-updated-in-updateprincipalunstaker-function
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

`stakingIndicesByPrincipalUnstaker` mapping not updated in `updatePrincipalUnstaker` function

### Overview


The bug report states that there is an issue with the `stakingIndicesByPrincipalUnstaker` mapping in the `DIAExternalStaking` and `DIAWhitelistedStaking` contracts. This mapping is not being updated properly when a new principal unstaker is set using the `updatePrincipalUnstaker` function. This results in the mapping not accurately reflecting the current stakes for both the old and new principal unstaker. To fix this, it is recommended to update the `updatePrincipalUnstaker` function to properly update the mapping for both addresses. The client has confirmed that this update has been made.

### Original Finding Content

##### Description
In both `DIAExternalStaking` and `DIAWhitelistedStaking` contracts, the `stakingIndicesByPrincipalUnstaker` mapping is not updated when a new principal unstaker is set via the `updatePrincipalUnstaker` function. This means that the mapping will not correctly reflect the current stakes for the old and new principal unstaker.
<br/>
##### Recommendation
We recommend modifying the `updatePrincipalUnstaker` function to update the `stakingIndicesByPrincipalUnstaker` mapping for both the old and new principal unstaker addresses. The staking store index for the old address should be removed from the corresponding array and added to the new one (identified by the new principal unstaker address).

> **Client's Commentary:**
> mapping update has been added

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#3-stakingindicesbyprincipalunstaker-mapping-not-updated-in-updateprincipalunstaker-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

