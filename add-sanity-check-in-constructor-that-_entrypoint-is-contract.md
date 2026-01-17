---
# Core Classification
protocol: Coinbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40952
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/f2f052d8-edfb-496f-9014-98a1bc8cadb8
source_link: https://cdn.cantina.xyz/reports/cantina_coinbase_oct2023.pdf
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
finders_count: 2
finders:
  - chris
  - Denis Miličević
---

## Vulnerability Title

Add sanity check in constructor that _entryPoint is contract 

### Overview

See description below for full details.

### Original Finding Content

## Context 
BasePaymaster.sol#L21-L23

## Description 
The setting of the `entryPoint` variable currently lacks any validation. It could be set to the null address or an EOA while the Paymaster contract gets successfully deployed.

## Recommendation 
Adding a sanity check that the `_entryPoint` parameter passed to the constructor indeed points to a contract would remove the aforementioned concerns. This can be done via a simple addition of: 

```solidity
require(address(_entryPoint).code.length > 0, "Passed _entryPoint is not currently a contract");
```

to ideally the `BasePaymaster` in the upstream dependency or within the Paymaster contract's constructor itself. Additionally, OZ's Address library could be utilized, which implements an `isContract()` function that works similar to the above.

## Coinbase 
Fixed in PR 14.

## Cantina Managed 
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Coinbase |
| Report Date | N/A |
| Finders | chris, Denis Miličević |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_coinbase_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/f2f052d8-edfb-496f-9014-98a1bc8cadb8

### Keywords for Search

`vulnerability`

