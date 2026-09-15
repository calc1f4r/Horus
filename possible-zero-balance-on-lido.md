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
solodit_id: 28181
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#6-possible-zero-balance-on-lido
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

Possible zero balance on `Lido`

### Overview


This bug report is about the blockchain protocol Lido. The issue is that it is possible for the Lido protocol to have a zero balance on reward distribution. This is a problem because it can cause errors and prevent users from accessing their rewards. The recommendation is to add a check for the case when Lido has a zero balance on reward distribution. This would ensure that users can access their rewards and that the system runs smoothly.

### Original Finding Content

##### Description
It is possible that `Lido` can have zero balance on reward distribution: https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Lido.sol#L588

##### Recommendation
We recommend to add a check for the case when `Lido` has zero balance on reward distribution.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#6-possible-zero-balance-on-lido
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

