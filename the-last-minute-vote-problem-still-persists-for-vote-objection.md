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
solodit_id: 28113
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#9-the-last-minute-vote-problem-still-persists-for-vote-objection
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

The "last-minute" vote problem still persists for vote objection

### Overview

See description below for full details.

### Original Finding Content

##### Description
The problem with the "last-minute" vote in this scheme is not fully mitigated, because a possibility of a vote to be denied at the last moment still persists. An attacker can object and deny the voting at the last moment like it could be done with the previous version of voting.

##### Recommendation
Should be simply acknowledged by the Lido team.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#9-the-last-minute-vote-problem-still-persists-for-vote-objection
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

