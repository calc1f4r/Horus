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
solodit_id: 29057
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

[L-03] Dropping a dust to grief the staking process

### Overview

See description below for full details.

### Original Finding Content

After an amount of lst being transferred to a specified `NodeDelegator`, the stake on EigenLayer is expected to happen. However, if there is a possibility to grief `depositAssetIntoStrategy`, adversary might drop some dust and front-run the tx submitted by `LRTManager`. This forces to transfer some assets back to the pool in order to successfully stake at EigenLayer.
  
### Example of an occurrence

It's better to provide an opportunity for `LRTManager` to decide, how much lst amount is about to be transferred and not blindly rely on the total balance [here](https://github.com/code-423n4/2023-11-kelp/blob/main/src/NodeDelegator.sol#L63).



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

