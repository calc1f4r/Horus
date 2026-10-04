---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28719
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#inaccurate-liquidityadded-parameter-before-flashloan-transfer
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Inaccurate `liquidityAdded` Parameter Before Flashloan Transfer

### Overview


This bug report is about the `updateInterestRates` call in the `LendingPool.sol` file. The `liquidityAdded` parameter of this call is incorrect, as it does not take into account the flashloan body that needs to be transferred. To fix this bug, it is recommended to update the `liquidityAdded` parameter.

### Original Finding Content

##### Description

https://github.com/aave/protocol-v2/blob/56d25e81cb0fdfcac785d669d3577b1ef2d9286e/contracts/lendingpool/LendingPool.sol#L511

The `liquidityAdded` parameter of the `updateInterestRates` call seems to be incorrect as the flashloan body is yet to be transferred thus it will not be included in the interest rates calculation.

##### Recommendation

It is recommended to fix the `liquidityAdded` parameter.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#inaccurate-liquidityadded-parameter-before-flashloan-transfer
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

