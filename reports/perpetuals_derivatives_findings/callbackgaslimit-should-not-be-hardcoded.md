---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37447
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

`CallbackGasLimit` Should Not Be Hardcoded

### Overview


The report describes a bug in the GMX protocol where the configurable parameter `Keys.MAX_CALLBACK_GAS_LIMIT` can be set to a value smaller than 2 million. This causes an issue when Vaultka creates `createDeposit` and `createWithdrawal` requests on the GMX side, as the `callbackGasLimit` is hardcoded to 2 million. This results in all deposit and withdrawal requests from Vaultka being reverted. The suggested solution is to make `callbackGasLimit` configurable. The bug has been resolved.

### Original Finding Content

**Severity** - Medium

**Status** - Resolved

**Description**

`Keys.MAX_CALLBACK_GAS_LIMIT` is configurable param inside GMX protocol, which can be changed to value that is smaller than 2 millions. 
Vaultka creates `createDeposit` and `createWithdrawal` on the GMX side and sends `CallbackGasLimit` alongside the call which is hardcoded to 2 million.When deposit or withdraw request is handled on GMX side, then `callbackGasLimit` is validated to be not bigger than it's allowed. `Keys.MAX_CALLBACK_GAS_LIMIT` value is configurable and can be changed by GMX team. And in case if it will be less than 2 million, then all deposits and withdraws requests from vaultka will be reverted.

**Remediation**:

Make `callbackGasLimit` to be configurable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

