---
# Core Classification
protocol: Zap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35422
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-11-Zap.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Missing `disableInitializers` Call in Proxy Upgradeable Contract Constructor

### Overview


This bug report discusses a medium severity issue that has been resolved. The problem was found in three contracts - Vesting.sol, TokenSale.sol, and Admin.sol. The issue was caused by not calling `disableInitializers` in the constructor of a proxy upgradeable contract. This could potentially allow attackers to initialize the implementation contract, posing a serious risk. The recommendation is to include a call to `disableInitializers` in the constructor, as suggested by OpenZeppelin. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

Location: Vesting.sol, TokenSale.sol, Admin.sol

**Description**

A concern arises due to the usage of a proxy upgradeable contract without calling `disableInitializers` in the constructor of the logic contract. This oversight introduces a severe risk, allowing potential attackers to initialize the implementation contract itself.

**Recommendation** 

Call disableInitializers: Include a call to `disableInitializers` in the constructor of the logic contract as recommended by OpenZeppelin here .

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Zokyo |
| Protocol | Zap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-11-Zap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

