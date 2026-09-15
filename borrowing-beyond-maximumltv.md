---
# Core Classification
protocol: Liquorice
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49442
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#2-borrowing-beyond-maximumltv
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
  - MixBytes
---

## Vulnerability Title

Borrowing beyond `MaximumLTV`

### Overview


The bug report states that there is a discrepancy in the LTV (loan-to-value) limits for two functions, `borrow()` and `withdraw()`. While `borrow()` has a limit of 80%, `withdraw()` allows withdrawals up to 90%. This means that an attacker can use both functions together to bypass the 80% limit and effectively borrow up to 90%. The recommendation is to use the same LTV threshold for both functions to prevent this vulnerability.

### Original Finding Content

##### Description
`LendingPool.borrow()` has a limit up to `TypeofLTV.MaximumLTV` (set at `80%` in the project tests). However, `LendingPool.withdraw()` allows withdrawals up to `TypeofLTV.LiquidationThreshold` (set at `90%` in the tests).

An attacker could call `borrow() + withdraw()` in a single transaction to effectively borrow up to `TypeofLTV.LiquidationThreshold`, bypassing the `MaximumLTV` limit.

##### Recommendation
We recommend using the same LTV threshold for both `borrow()` and `withdraw()`.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Liquorice |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#2-borrowing-beyond-maximumltv
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

