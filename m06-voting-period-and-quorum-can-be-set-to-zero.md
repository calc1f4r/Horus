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
solodit_id: 11329
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

[M06] Voting period and quorum can be set to zero

### Overview


This bug report is about the `Governance` contract of the Audius protocol. The contract is initialized with two variables, `votingPeriod` and `votingQuorum`, which are both checked to make sure that they are greater than 0. However, the corresponding setter functions, `setVotingPeriod` and `setVotingQuorum`, allow these two variables to be reset to 0. 

Setting the `votingPeriod` to zero would cause spurious proposals that cannot be voted on. Setting the `quorum` to zero is worse because it would allow proposals with 0 votes to be executed. The bug report suggests adding validation to the setter functions to prevent this from happening.

The bug has since been fixed in pull request #568.

### Original Finding Content

When the `Governance` contract is initialized, the values of [`votingPeriod`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L132) and [`votingQuorum`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L135) are checked to make sure that they are greater than 0. However, the corresponding setter functions [`setVotingPeriod`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L457) and [`setVotingQuorum`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L467) allow these to variables to be reset to 0.


Setting the `votingPeriod` to zero would cause spurious proposals that cannot be voted. Setting the `quorum` to zero is worse because it would allow proposals with 0 votes to be executed.


Consider adding the validation to the setter functions.


***Update:** Fixed in [pull request #568](https://github.com/AudiusProject/audius-protocol/pull/568).*

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

