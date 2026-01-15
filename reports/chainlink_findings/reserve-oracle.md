---
# Core Classification
protocol: Divergence Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29445
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Divergence%20Protocol/README.md#2-reserve-oracle
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

Reserve oracle

### Overview


A bug report has been filed concerning Chainlink oracle and its instability. It is believed that gaps in the price history are causing the `settle` function call to revert. A recommendation has been made to add a reserve price source for the `Oracle` contract to address this issue. This will help to ensure that the `settle` function call does not revert due to price history gaps.

### Original Finding Content

##### Description
In case of some instability with Chainlink oracle gaps in a price history are probably present. These gaps cause the `settle` function call to revert.
##### Recommendation
We recommend adding some reserve price source for the `Oracle` contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Divergence Protocol |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Divergence%20Protocol/README.md#2-reserve-oracle
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

