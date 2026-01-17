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
solodit_id: 28176
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#2-controller-can-be-initialized-several-times
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

Controller can be initialized several times

### Overview


This bug report is about the `Controller` contract in the `lido-dot-ksm` repository on Github. The `initialize` function in this contract can be called multiple times, which can cause unexpected behavior. To fix this issue, the developers suggest adding a `initializer` modifier to the `initialize` function. This modifier will prevent the function from being called more than once.

### Original Finding Content

##### Description
In contract `Controller` the `initialize` function can be called several times: https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Controller.sol#L140

##### Recommendation
We recommend adding the `initializer` modifier.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#2-controller-can-be-initialized-several-times
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

