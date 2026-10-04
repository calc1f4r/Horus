---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55407
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#2-message-verification
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

Message Verification

### Overview


The report describes a serious problem with the `ISM` contract, specifically with the `verify` function. This vulnerability could allow untrusted addresses to manipulate data processed by the `Mailbox` `process` function. There is also a dangerous parameter called `allowAll` which, if enabled, could allow malicious users to submit oracle data. This issue is considered critical because it could result in disruptions or losses for the protocols using the `ISM` contract. The report recommends adding caller verification for the `Mailbox` contract in the `verify` function and removing the `allowAll` logic to improve security.

### Original Finding Content

##### Description
A critical security vulnerability has been identified within the `verify` function of the `ISM` (Interchain Security Module) contract. The ISM doesn't verify the caller of the `Mailbox` `process` function, which could allow untrusted addresses to pass an arbitrary message to the `Mailbox`, ultimately leading to potential manipulation of the data that will be processed.
There is also a dangerous parameter `allowAll`, which may lead to anyone malicious submitting oracle data if enabled.
This issue is classified as **Critical** because it could lead to manipulation of critical data processed by the `process` function, which could result in unpredictable disruptions or severe losses in the integrated protocols.

##### Recommendation
We recommend adding caller verification of the `Mailbox` contract within the `verify` function. It should ensure that the caller is indeed a trusted address. We also recommend removing the logic related to the `allowAll` flag as it may affect the protocol security badly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#2-message-verification
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

