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
solodit_id: 28364
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track/README.md#1-duplicate-voting-functionality
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

Duplicate voting functionality

### Overview


The EVMScriptExecutor has permissions to make financial transactions to both the EasyTrack and Voting contracts. This allows token holders to create voting with their own purposes in the Voting contract. To prevent this potential security risk, it is recommended to split up the functionality between the EasyTrack and Voting contracts.

### Original Finding Content

##### Description
EVMScriptExecutor has permissions for EasyTrack and Voting contracts to make financial transactions (finance contract). It is possible to create voting in this contracts at the same time. EasyTrack has permissions only for TrustedCaller. In voting contract every token holder able to do it and create Voting with own purposes
at line https://github.com/lidofinance/easy-track/blob/ec694adb872877db814da960d96ce767ccbdf462/contracts/EvmScriptExecutor.sol#L71
##### Recommendation
We recommend to split up functionality between EasyTrack and Voting contacts

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track/README.md#1-duplicate-voting-functionality
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

