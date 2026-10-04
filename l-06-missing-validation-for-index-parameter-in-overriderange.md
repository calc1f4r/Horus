---
# Core Classification
protocol: Ondo Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27022
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-09-ondo
source_link: https://code4rena.com/reports/2023-09-ondo
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

protocol_categories:
  - leveraged_farming
  - rwa
  - services
  - cdp
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-06] Missing validation for index parameter in `overrideRange()`

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2023-09-ondo/blob/main/contracts/rwaOracles/RWADynamicOracle.sol#L186

The `overrideRange()` function should validate that `indexToModify` is within bounds, i.e. `require(indexToModify < rangeLength)`.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ondo Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-09-ondo
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-09-ondo

### Keywords for Search

`vulnerability`

