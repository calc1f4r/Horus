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
solodit_id: 28183
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#1-possible-free-tokens-on-ledger
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

Possible free tokens on Ledger

### Overview


This bug report is about a problem with sending funds to Ledger. If someone sends the code `xcKSM` to the Ledger, it will cause an issue. To solve this problem, it is recommended to send excess funds to the treasury. This will help to prevent any potential issues with sending funds to the Ledger.

### Original Finding Content

##### Description
If someone sends `xcKSM` to Ledger: https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Ledger.sol#L282

##### Recommendation
We recommend sendig excess in funds to treasury.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#1-possible-free-tokens-on-ledger
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

