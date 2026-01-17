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
solodit_id: 28106
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#2-the-vote-is-open-for-objection-during-the-main-voting-time
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

The vote is open for objection during the main voting time

### Overview

See description below for full details.

### Original Finding Content

##### Description
At line https://github.com/lidofinance/aragon-apps/blob/7e5cd1961697a1bc514bfebdeab08a296e51d700/apps/voting/contracts/Voting.sol#L475
the `_isVoteOpenForObjection()` function returns `true` during the main voting time. It can be potentially misleading in functions `canObject()` and `getVote()` at the following lines:
- https://github.com/lidofinance/aragon-apps/blob/7e5cd1961697a1bc514bfebdeab08a296e51d700/apps/voting/contracts/Voting.sol#L267
- https://github.com/lidofinance/aragon-apps/blob/7e5cd1961697a1bc514bfebdeab08a296e51d700/apps/voting/contracts/Voting.sol#L316.

##### Recommendation
It is recommended to change the  `_isVoteOpenForObjection()` function to return `true` only during the objection time or to rename the function to better indicate its purpose.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#2-the-vote-is-open-for-objection-during-the-main-voting-time
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

