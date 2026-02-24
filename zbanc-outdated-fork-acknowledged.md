---
# Core Classification
protocol: Zer0 - zBanc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13397
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/05/zer0-zbanc/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - David Oz Kashi
  - Martin Ortner
---

## Vulnerability Title

zBanc - outdated fork  Acknowledged

### Overview


This bug report is about a system that was forked off from Bancor's version 0.6.18, which was released in October 2020. The current version of Bancor is 0.6.36, which was released in April 2021. It is recommended to check if any security fixes were released after version 0.6.18 and to consider rebasing the system with the current stable release.

### Original Finding Content

#### Description


According to the client the system was forked off bancor [v0.6.18 (Oct 2020)](https://github.com/bancorprotocol/contracts-solidity/releases/tag/v0.6.18). The current version 0.6.x is [v0.6.36 (Apr 2021)](https://github.com/bancorprotocol/contracts-solidity/releases/tag/v0.6.36).


#### Recommendation


It is recommended to check if relevant security fixes were released after v0.6.18 and it should be considered to rebase with the current stable release.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Zer0 - zBanc |
| Report Date | N/A |
| Finders | David Oz Kashi, Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/05/zer0-zbanc/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

