---
# Core Classification
protocol: Compound Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11828
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-audit/
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
  - cdp
  - services
  - liquidity_manager
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Outdated Interest Rates

### Overview


This bug report is about the `CToken` contract, a part of the Compound Protocol. The two functions, `borrowRatePerBlock` and `supplyRatePerBlock`, are meant to return the current rates, but they may be outdated. This is because they rely on variables that are updated when the `accrueInterest` function is called. To fix this issue, the `accrueInterest` function should be called at the beginning of the `borrowRatePerBlock` and `supplyRatePerBlock` functions.

### Original Finding Content

In the `CToken` contract, [borrowRatePerBlock](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/CToken.sol#L410) and [supplyRatePerBlock](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/CToken.sol#L420) are supposed to return the current rates but they may be outdated. This is because those rates depend on variables that are updated when `accrueInterest` is called. Consider calling [`accrueInterest`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/CToken.sol#L597) at the beginning of these functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

