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
solodit_id: 28128
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#5-incorrect-event
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

Incorrect event

### Overview


This bug report is about an issue with the cover of `stETH` not burning. The problem occurs when the `stETH` amount is included in the event. It is recommended that the `stETH` amount be excluded from the event to solve the issue.

### Original Finding Content

##### Description
In case of cover, `stETH` doesn't burn 
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.4.24/StETH.sol#L461
##### Recommendation
It is necessary to exclude the `stETH` amount from the event.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#5-incorrect-event
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

