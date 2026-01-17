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
solodit_id: 28175
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#1-public-access-to-all-functions
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

Public access to all functions

### Overview


This bug report is about a contract called `Controller` which can be exploited due to all of its functions having public access. The contract can be found at the given link. The recommendation is that access modificators should be added to the contract in order to prevent exploitation. Access modificators are used to define who is allowed to access certain parts of a contract, and can be used to protect contracts from malicious actors. Adding access modificators to the `Controller` contract will help to ensure that it is not exploited.

### Original Finding Content

##### Description
In contract `Controller` all functions have public access which can be exploited:
https://github.com/mixbytes/lido-dot-ksm/blob/76a10efa5f223c4c613f26794802b8fb9bb188e1/contracts/Controller.sol

##### Recommendation
We recommend adding access modificators.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20KSM/README.md#1-public-access-to-all-functions
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

