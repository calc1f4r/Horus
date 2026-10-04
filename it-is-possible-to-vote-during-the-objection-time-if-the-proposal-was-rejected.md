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
solodit_id: 28104
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#1-it-is-possible-to-vote-during-the-objection-time-if-the-proposal-was-rejected
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

It is possible to vote during the objection time if the proposal was rejected

### Overview


A bug has been reported in the code of the Aragon Apps Voting project. At line 192 of the Voting.sol file, the `vote()` function checks if the vote is `no`, if the vote is open for objection and if the voter has balance. However, it does not check if the vote was rejected or not, which means it is possible to vote `no` for a proposal even if it was rejected during the voting time. It is recommended to add a check if the vote was rejected in order to prevent this issue.

### Original Finding Content

##### Description
At line https://github.com/lidofinance/aragon-apps/blob/7e5cd1961697a1bc514bfebdeab08a296e51d700/apps/voting/contracts/Voting.sol#L192 during the objection time, the `vote()` function checks if the vote is `no`, if the vote is open for objection and if the voter has balance. But there is no check wether the vote was rejected or not. So it is possible to vote `no` for a proposal even if it was rejected during the voting time.

##### Recommendation
It is recommended to add a check if the vote was rejected.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#1-it-is-possible-to-vote-during-the-objection-time-if-the-proposal-was-rejected
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

