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
solodit_id: 28110
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#6-a-malicious-voter-can-potentially-block-a-vote
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

A malicious voter can potentially block a vote

### Overview

See description below for full details.

### Original Finding Content

##### Description
At line https://github.com/lidofinance/aragon-apps/blob/7e5cd1961697a1bc514bfebdeab08a296e51d700/apps/voting/contracts/Voting.sol#L368 a voter can change their vote.
The malicious voter can initially vote `yes` misleading other users about their intention, then change their vote to `no` at the last moment potentially blocking the proposal.

##### Recommendation
It is recommended to check to prevent the last-minute `no` attacks against proposals.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#6-a-malicious-voter-can-potentially-block-a-vote
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

