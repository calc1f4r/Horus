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
solodit_id: 41236
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#14-unused-function-_checkprocessingdeadline
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

Unused function `_checkProcessingDeadline()`

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified at the [following line](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/lib/base-oracle/BaseOracle.sol#L410) in the `BaseOracle` contract. The `_checkProcessingDeadline()` function, which doesn't accept parameters, is never used.

The issue is classified as **Low** severity because there is an alternative function `_checkProcessingDeadline(uint256 deadlineTime)` which is used inside the `_startProcessing` function.

##### Recommendation
We recommend removing the mentioned unused function.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#14-unused-function-_checkprocessingdeadline
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

