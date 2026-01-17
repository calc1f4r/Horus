---
# Core Classification
protocol: Forgotten Runes
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22430
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-runes
source_link: https://code4rena.com/reports/2022-05-runes
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
  - services
  - launchpad
  - synthetics
  - payments

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[04] Missing zero-address check in the setter functions and initializers

### Overview

See description below for full details.

### Original Finding Content


Missing checks for zero-addresses may lead to infunctional protocol, if the variable addresses are updated incorrectly.

### Proof of Concept

Navigate to the following contracts.

[ForgottenRunesWarriorsMinter.sol#L544](https://github.com/code-423n4/2022-05-runes/blob/main/contracts/ForgottenRunesWarriorsMinter.sol#L544)<br>
[ForgottenRunesWarriorsMinter.sol#L528](https://github.com/code-423n4/2022-05-runes/blob/main/contracts/ForgottenRunesWarriorsMinter.sol#L528)<br>

### Recommended Mitigation Steps

Consider adding zero-address checks in the discussed constructors:
require(newAddr != address(0));.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Forgotten Runes |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-runes
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-05-runes

### Keywords for Search

`vulnerability`

