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
solodit_id: 41235
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#13-_treecid-is-not-checked-for-duplicate-value
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

`_treeCid` is not checked for duplicate value

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [processOracleReport](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSFeeDistributor.sol#L129) function of the `CSFeeDistributor` contract. `_treeCid` should be checked against the previously stored value as it should also be changed when the tree root changes.

The issue is classified as **Low** severity because it is possible to start processing an oracle report with an unchanged `treeCID`.

##### Recommendation
We recommend adding a `revert` statement for cases when `_treeCid == treeCid`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#13-_treecid-is-not-checked-for-duplicate-value
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

