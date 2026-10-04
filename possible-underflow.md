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
solodit_id: 28182
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#7-possible-underflow
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
---

## Vulnerability Title

Possible underflow

### Overview


This bug report is about a discrepancy between the free balance reported in the ledger and the free balance from the previous era. The ledger in question is https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Ledger.sol#L297. The free balance from the report can be less than the free balance from the previous era, which can lead to discrepancies.

The recommendation given in this report is to add a variable to control which amount should be bonded on the next era. This variable will ensure that the free balance reported is correct and that discrepancies between the free balance from the report and the free balance from the previous era are avoided.

### Original Finding Content

##### Description
It is possible that free balance from the report can be less than free balance from the previous era: https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Ledger.sol#L297

##### Recommendation
We recommend to add a variable to control which amount should be bonded on the next era.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#7-possible-underflow
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

