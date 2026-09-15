---
# Core Classification
protocol: FireBTC
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34372
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/FireBTC/FBTC/README.md#3-the-_getfee-function-is-not-monotonic
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

The `_getFee` function is not monotonic

### Overview


The developer has stated that the `_getFee` function should always increase or stay the same. However, if multiple fee levels are set up, the function may not follow this rule. This issue cannot be fixed through configuration and the function needs to be changed to match its intended behavior.

### Original Finding Content

##### Description
According to the developer's statement, the `_getFee` function is intended to be monotonic. However, the current implementation might not be monotonic if several fee tiers are configured. This issue cannot be corrected by any configuration due to the nature of the current implementation of the `_getFee` function.

##### Recommendation
We recommend adjusting the implementation of the `_getFee` function to comply with the intended behavior.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | FireBTC |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/FireBTC/FBTC/README.md#3-the-_getfee-function-is-not-monotonic
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

