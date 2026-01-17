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
solodit_id: 41211
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Oracle/README.md#2-incorrect-comment-for-framecheckpoint
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

Incorrect comment for `FrameCheckpoint`

### Overview

See description below for full details.

### Original Finding Content

##### Description
`FrameCheckpoint.slot` is the first slot of `max(duty_epochs) + 2` epoch, not [the last slot of the epoch](https://github.com/lidofinance/lido-oracle/blob/4e1e2210483fb44926d751049ea2d21561779dc8/src/modules/csm/checkpoint.py#L29).

##### Recommendation
We recommend clarifying the comment.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Oracle/README.md#2-incorrect-comment-for-framecheckpoint
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

