---
# Core Classification
protocol: Hyperstable_2025-02-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57794
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
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

[M-03] User deposits may be vulnerable to sandwich attacks

### Overview


The `PositionManager` contract has a bug that could lead to users receiving fewer shares than expected when depositing or withdrawing their assets. This is because there is no minimum amount of shares specified in the `deposit()` and `withdraw()` functions, leaving users vulnerable to sandwich attacks. To fix this, a `minAmountOut` parameter should be added to ensure that users receive at least a minimum amount of shares and prevent malicious actors from manipulating the share price.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the `PositionManager` contract, the `deposit()` function allows users to deposit the underlying asset of a specified vault and lock them for collateral. However, the function does not introduce `minAmountOut` (the minimum amount of shares a user is willing to receive) .

The lack of this parameter exposes the depositors to **sandwich attacks**, where a malicious actor could front-run the deposit transaction to manipulate the share price, resulting in depositors receiving fewer shares than expected, reducing their effective collateral.

Same issue with `withdraw()` function, where there's no minimum amount of redeemed assets acceptable to be received by the user.

## Recommendations

Introduce a `minAmountOut` parameter to ensure that the user is only willing to accept a minimum amount of shares for the deposit (and for withdrawals), and if the final amount of shares is less than `minAmountOut`, the transaction should be reverted.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-02-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

