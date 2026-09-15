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
solodit_id: 36212
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#1-add-a-check-for-the-allowed-range-for-maxpositivetokenrebase
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

Add a check for the allowed range for `maxPositiveTokenRebase`

### Overview

See description below for full details.

### Original Finding Content

##### Description
There is a `maxPositiveTokenRebase` parameter check at the [following line](https://github.com/lidofinance/core/blob/efeff81c18f85451ebf98e8fd8bb78b8eb0095f6/contracts/0.8.9/sanity_checks/OracleReportSanityChecker.sol#L880). This check allows `maxPositiveTokenRebase` to be assigned a value between `1` and `type(uint64).max`. But `maxPositiveTokenRebase` should be in range from `1` to `1e9` or equal to `type(uint64).max`.

##### Recommendation
We recommend adding a more strict check for the `maxPositiveTokenRebase` parameter.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#1-add-a-check-for-the-allowed-range-for-maxpositivetokenrebase
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

