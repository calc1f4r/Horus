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
solodit_id: 28421
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#6-storage-collisions-between-implementation-versions
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

Storage collisions between implementation versions

### Overview

See description below for full details.

### Original Finding Content

##### Description
In future, if a developer changes order or types of variables in a new logic contract, it may be broken. More information about Storage Collisions you can find [here](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies#unstructured-storage-proxie).
##### Recommendation
We recommend to add comment in the code of a logic contract about this collisions.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#6-storage-collisions-between-implementation-versions
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

