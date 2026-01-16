---
# Core Classification
protocol: Pods Finance Ethereum Volatility Vault Audit #1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10424
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-1/
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

protocol_categories:
  - dexes
  - yield
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Parallel share cap setting

### Overview


This bug report is about a Configuration Manager that determines the maximum vault shares available for minting. When setting a new cap through the setCap function, the target contract address is checked for the zero address, and a SetCap event is emitted. However, the underlying setParameter function can be called directly to change the maximum vault shares available. This will bypass the zero address check and emit a ParameterSet event instead of the expected SetCap event. 

To fix this, the setParameter function should be removed and individual get and set functions should be added for all necessary configuration parameters. This will ensure consistency between the two mechanisms in setting the share cap. This issue has been fixed in commit cbe61d0.

### Original Finding Content

The configuration manager determines the maximum vault shares available for minting. When setting a new cap through the [`setCap`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/configuration/ConfigurationManager.sol#L55) function, the target contract address is checked for the zero address, and a `SetCap` event is emitted.


However, the underlying [`setParameter`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/configuration/ConfigurationManager.sol#L25) function can be called directly to change the maximum vault shares available. This will bypass the zero address check and emit a `ParameterSet` event instead of the expected `SetCap` event.


Consider ensuring consistency between the two mechanisms in setting the share cap. Depending on the desired outcome, this could involve removing the `setParameter` function and adding individual get and set functions for all necessary configuration parameters.


**Update:** *Fixed in commit [`cbe61d0`](https://github.com/pods-finance/yield-contracts/pull/44/commits/cbe61d00834aafcbcc9c342dc80dd97d65a4b5b8).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Pods Finance Ethereum Volatility Vault Audit #1 |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-1/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

