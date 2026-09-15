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
solodit_id: 28177
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#3-incorrect-condition
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

Incorrect condition

### Overview


This bug report is about an infinite loop issue in the Lido.sol file. The condition in line 748 of the file is incorrect and can lead to an infinite loop. To fix this issue, the developer should change the operator "||" to "&&". This change will prevent the code from entering an infinite loop and will ensure that the code runs as expected.

### Original Finding Content

##### Description
The condition is incorrect here that can lead to an infinite loop: https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Lido.sol#L748

##### Recommendation
We recommend changing `||` into `&&`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#3-incorrect-condition
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

