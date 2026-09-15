---
# Core Classification
protocol: Mellow Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28392
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Mellow%20Finance/README.md#2-unability-to-withdraw-profits-from-position-manager
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

Unability to withdraw profits from Position Manager

### Overview


Bug reports are documents that provide detailed information about software errors. This particular bug report is about the call parameters of the positionManager.collect() function, which is preventing the collection of profit. Instead, only the liquidity value is being collected. The recommendation is to not use the undesired limitation of the amount to be collected. To summarize, the positionManager.collect() function is not allowing the collection of profit, and the recommendation is to not use the undesired limitation of the amount to be collected.

### Original Finding Content

##### Description
The call parameters of positionManager.collect() prohibits collecting of profit. Only liquidity value will be collected.
##### Recommendation
It is recommended to not use undesired limitation of amount to be collected

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Mellow Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Mellow%20Finance/README.md#2-unability-to-withdraw-profits-from-position-manager
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

