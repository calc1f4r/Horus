---
# Core Classification
protocol: Debt DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42954
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-11-debtdao
source_link: https://code4rena.com/reports/2022-11-debtdao
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
  - dexes
  - services
  - liquidity_manager
  - payments
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-07]  Numeric values having to do with time should use time units for readability

### Overview

See description below for full details.

### Original Finding Content


There are [units](https://docs.soliditylang.org/en/latest/units-and-global-variables.html#time-units) for seconds, minutes, hours, days, and weeks, and since they're defined, they should be used.

*There is 1 instance of this issue:*
```solidity
File: contracts/modules/factories/LineFactory.sol

/// @audit 3000
14:       uint32 constant defaultMinCRatio = 3000; // 30.00% minimum collateral ratio

```
https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/modules/factories/LineFactory.sol#L14



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Debt DAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-debtdao
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-11-debtdao

### Keywords for Search

`vulnerability`

