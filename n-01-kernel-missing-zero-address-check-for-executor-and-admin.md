---
# Core Classification
protocol: Olympus DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24193
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-08-olympus
source_link: https://code4rena.com/reports/2022-08-olympus
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
  - liquid_staking
  - yield
  - cross_chain
  - leveraged_farming
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-01] Kernel: missing zero address check for `executor` and `admin`

### Overview

See description below for full details.

### Original Finding Content


*   <https://github.com/code-423n4/2022-08-olympus/blob/b5e139d732eb4c07102f149fb9426d356af617aa/src/Kernel.sol#L250-L253>

The `executor` and `admin` are not checked for the zero address when set by the `Kernel::executeAction`.

```solidity
// Kernel::executeAction
250         } else if (action_ == Actions.ChangeExecutor) {
251             executor = target_;
252         } else if (action_ == Actions.ChangeAdmin) {
253             admin = target_;
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Olympus DAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-olympus
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-08-olympus

### Keywords for Search

`vulnerability`

