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
solodit_id: 28445
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#1-block-header-incorrect-input
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

Block header incorrect input

### Overview


This bug report is about a function for extracting data from a block header tx. The function can fail without any information in case of incorrect input. To fix this issue, the developers recommend adding a check that requires the headerFields.length to be greater than 11. This check will ensure that the input is correct and the function will not fail without any information.

### Original Finding Content

##### Description
In the function for extracting data from block header tx can fail without any information in case of incorrect input:
https://github.com/lidofinance/curve-merkle-oracle/blob/ae093b308999a564ed3f23d52c6c5dce946dbfa7/contracts/StateProofVerifier.sol#L65

##### Recommendation
We recommend to add following check:
```solidity=
require(headerFields.length > 11, "INCORRECT_HEADER");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#1-block-header-incorrect-input
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

