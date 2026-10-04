---
# Core Classification
protocol: Venus Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20786
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-venus
source_link: https://code4rena.com/reports/2023-05-venus
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

[01] `PoolRegistry.supportMarket()` cannot be paused

### Overview

See description below for full details.

### Original Finding Content


Most actions in `PoolRegistry` can be paused, e.g. `_addToMarket()`, `exitMarket()`, `preMintHook()` etc.

Consider adding a "support" field in the enum Action and allowing `supportMarket()` to be paused. Not allowing `supportMarket()` to be paused could result in irregular behavior if everything else (mint, redeeming, borrowing enter market, exit market, etc) is paused but `supportMarket()` is open.

https://github.com/code-423n4/2023-05-venus/blob/main/contracts/Comptroller.sol#L801-L824

https://github.com/code-423n4/2023-05-venus/blob/main/contracts/Comptroller.sol#L1177

https://github.com/code-423n4/2023-05-venus/blob/main/contracts/Comptroller.sol#L188

https://github.com/code-423n4/2023-05-venus/blob/main/contracts/Comptroller.sol#L254

https://github.com/code-423n4/2023-05-venus/blob/main/contracts/ComptrollerStorage.sol#L44-L54



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Venus Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-venus
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-05-venus

### Keywords for Search

`vulnerability`

