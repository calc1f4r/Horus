---
# Core Classification
protocol: Audius Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11332
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/audius-contracts-audit/
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
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M09] Ties in governance proposals are approved

### Overview


This bug report is about a governance proposal in the Audius protocol which is a decentralized platform for streaming music. The issue is that when the stake in favor of a governance proposal is equal to the stake against it, the proposal is considered approved and can be executed. This can be a problem if the proposal is too contentious, as it could cause major issues if it is executed without a majority of supporting votes. The issue has now been fixed in pull request #576.

### Original Finding Content

When the [stake in favor a governance proposal is equal to the stake against it](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L371), the proposal is considered approved and can be executed. In cases when critical updates to the system are so contentious to the point of reaching a tie, the safest course of action is to prepare a new proposal that can be discussed further and be more easily approved later.


Consider executing proposals only when they have a majority of supporting votes.


***Update:** Fixed in [pull request #576](https://github.com/AudiusProject/audius-protocol/pull/576).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Audius Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/audius-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

