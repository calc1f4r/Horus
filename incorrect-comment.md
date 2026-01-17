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
solodit_id: 41248
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#26-incorrect-comment
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

Incorrect Comment

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [`discardConsensusReport` function](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/lib/base-oracle/BaseOracle.sol#L268) of the contract `BaseOracle`. There are duplicate list numbers in the comment and info about the check for report processing deadline, but it is not implemented. 

The issue is classified as **Low** severity because this missing check doesn't affect contract functionality.

##### Recommendation
We recommend fixing the mentioned comment and removing info about the deadline check.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#26-incorrect-comment
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

