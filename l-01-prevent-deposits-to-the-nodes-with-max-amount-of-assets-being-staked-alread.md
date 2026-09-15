---
# Core Classification
protocol: Kelp DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29055
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-11-kelp
source_link: https://code4rena.com/reports/2023-11-kelp
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
finders_count: 0
finders:
---

## Vulnerability Title

[L-01] Prevent deposits to the nodes with max amount of assets being staked already

### Overview

See description below for full details.

### Original Finding Content


If the node has staked already 1e23 of assets, it should not receive any transfers, since there is no more space to stake at EigenLayer.

### Example of an occurrence

Could be implied [here](https://github.com/code-423n4/2023-11-kelp/blob/main/src/LRTDepositPool.sol#L183-L197).



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kelp DAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-11-kelp
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-11-kelp

### Keywords for Search

`vulnerability`

