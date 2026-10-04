---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28124
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#1-extra-function
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

Extra function

### Overview


A bug report has been submitted regarding the Lido.sol code in the Lido.DAO repository. It has been identified that similar actions are being performed at two different locations in the code, however one of them is redundant as it does not include a change in the TOTAL_MEV_TX_FEE_COLLECTED_POSITION variable. It is recommended that the redundant feature be removed.

### Original Finding Content

##### Description
At lines
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.4.24/Lido.sol#L139-L142
and at lines
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.4.24/Lido.sol#L158-L165
similar actions are performed.
But in one case there is a change in the `TOTAL_MEV_TX_FEE_COLLECTED_POSITION` variable, and in the other case there is none.
One of these functions is redundant.
##### Recommendation
Need to remove the redundant feature.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#1-extra-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

