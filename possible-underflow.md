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
solodit_id: 28173
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#1-possible-underflow
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

Possible underflow

### Overview


This bug report is about an issue with a ledger in a system. The ledger's stake can decrease due to a rebalance, and if it then receives a large slash, an underflow can occur. This can cause problems in the system. The recommendation is to distribute slashes across all the ledgers, so that no one ledger is receiving a large slash. This should prevent the underflow from occurring.

### Original Finding Content

##### Description
If a ledger's stake drammaticaly decreases due to rebalance and after that the ledger receives a huge slash, then underflow can occur: https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Lido.sol#L608

##### Recommendation
We recommend distributing slashes across all the ledgers.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#1-possible-underflow
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

