---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53337
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] Missing slippage protection in `deposit()`,` mint()`, and `redeem()` functions

### Overview


The report describes a bug in the `OmoRouter` contract and the `OmoVault` contract. These contracts do not have a slippage mechanism, which can cause users to receive less assets or shares than expected. This can result in unexpected losses for users. The recommendation is to implement a slippage protection mechanism in the `OmoVault` contract, allowing users to specify an acceptable slippage when interacting with the contract.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

- The `deposit()`, `mint()`, and `redeem()` functions in the `OmoRouter` contract lack a slippage mechanism to safeguard against significant deviations in the assets received or shares minted, which would result in users getting less assets/shares and incur unexpected losses during these operations.

- The same issue exists when whitelisted users interact directly with the `OmoVault.deposit()`, `OmoVault.mint()`, and `OmoVault.redeem()` functions.

## Recommendation

Implement slippage protection mechanisms in the vault contract itself rather than in the `OmoRouter` contract, by introducing a parameter for acceptable slippage (minimum assets received or maximum shares burnt when redeeming) that users can specify when interacting with the vault.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

