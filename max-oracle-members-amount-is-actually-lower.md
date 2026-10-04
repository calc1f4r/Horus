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
solodit_id: 28126
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#3-max-oracle-members-amount-is-actually-lower
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

Max oracle members amount is actually lower

### Overview


This bug report is regarding the Max members of a quorum. The current Max members are 255 instead of 256 which may affect the quorum. This issue can be found in the link provided in the report. The recommendation is that the check needs to be corrected. 

In simple terms, the bug report is referring to a quorum which is a group of people who make decisions. This quorum should have 256 members but it currently has 255. This might affect the decisions made by the quorum. The recommendation is to correct the check to ensure that the quorum has the correct number of members.

### Original Finding Content

##### Description
Max members are 255 instead of 256 which may affect the quorum:
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.4.24/oracle/LidoOracle.sol#L432
##### Recommendation
The check needs to be corrected.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#3-max-oracle-members-amount-is-actually-lower
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

