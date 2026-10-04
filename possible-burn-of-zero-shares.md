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
solodit_id: 28178
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#4-possible-burn-of-zero-shares
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

Possible burn of zero shares

### Overview


This bug report is about a rounding error that can allow a user to burn zero shares. This error is located in the Lido.sol file, line 522. To fix this issue, it is recommended to add a check that would prevent a user from burning zero shares. This will ensure that the rounding error does not cause any issues for users.

### Original Finding Content

##### Description
Due to rounding errors a user can burn zero shares: https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Lido.sol#L522

##### Recommendation
We recommend adding a check so that a user couldn't burn zero shares.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#4-possible-burn-of-zero-shares
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

