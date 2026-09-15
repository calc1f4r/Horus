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
solodit_id: 34406
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#1-expired-proposals-can-be-executed
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

Expired proposals can be executed

### Overview


The bug report states that there is an issue with an expired proposal being able to be executed when using the `_gracePeriod` extension. The recommendation is to save `_gracePeriod` as a parameter of the action to prevent this issue from affecting the protocol.

### Original Finding Content

##### Description
An expired proposal can be executed in case of the `_gracePeriod` extension: https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/Lido/contracts/BridgeExecutorBase.sol#L233.

##### Recommendation
We recommend saving `_gracePeriod` as a parameter of the action, so the parameter updates will not affect the protocol.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#1-expired-proposals-can-be-executed
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

