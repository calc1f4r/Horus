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
solodit_id: 28180
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#5-insufficient-xcksm-balance-on-lido
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

Insufficient xcKSm balance on `Lido`

### Overview


This bug report is about the Lido contract on the MixBytes Github repository. On line 563 of the Lido.sol file, it is possible that the contract can have less tokens than the "_readyToClaim" variable. This could lead to an issue where the contract would not have enough tokens to transfer. To prevent this, the report recommends adding a requirement that the contract would have enough tokens to transfer.

### Original Finding Content

##### Description
It is possible that `Lido` can have less than `_readyToClaim` : https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Lido.sol#L563

##### Recommendation
We recommend to add a requirement that `Lido` would have enough tokens to transfer.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#5-insufficient-xcksm-balance-on-lido
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

