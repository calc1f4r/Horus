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
solodit_id: 41245
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#23-lack-of-index-validation-in-at-function
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

Lack of Index Validation in `at` Function

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [at](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/lib/QueueLib.sol#L229-L234) function of the `QueueLib` library. The function currently does not validate whether the provided `index` falls within the allowable range between `head` and `tail`. This could result in the function returning incorrect data or even accessing uninitialized memory, leading to unpredictable behavior.

##### Recommendation
We recommend adding a check to ensure that the `index` falls within the range between `self.head` and `self.tail`. This will prevent out-of-bounds access and ensure that the function only returns valid data.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#23-lack-of-index-validation-in-at-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

