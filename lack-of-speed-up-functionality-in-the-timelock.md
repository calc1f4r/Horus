---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34264
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#2-lack-of-speed-up-functionality-in-the-timelock
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

Lack of speed-up functionality in the `TimeLock`

### Overview


The report describes an issue with the `TimeLock` feature, which is used to enforce a delay before a certain action can be taken. If the delay is longer than intended, the only solution is to replace the `TimeLock` implementation. The report recommends adding a feature to speed up the delay in order to address unintentionally long delays.

### Original Finding Content

##### Description
Once created, an agreement in the `TimeLock` enforces a delay until the expiration time specified during the agreement's creation. If the delays are unintentionally long, the only remedy is to replace the `TimeLock` implementation.

Related code - procedure of agreement execution: https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/DefaultTimeLock.sol#L83
##### Recommendation
We recommend implementing speed-up functionality in the `TimeLock` to address unintentionally prolonged delays.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#2-lack-of-speed-up-functionality-in-the-timelock
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

