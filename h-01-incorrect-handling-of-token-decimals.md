---
# Core Classification
protocol: Dinari_2024-12-07
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49118
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Dinari-security-review_2024-12-07.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

[H-01] Incorrect handling of token decimals

### Overview


The bug report states that there is a problem with the `previewDeposit()`, `previewMint()`, `previewWithdraw()` and `previewRedeem()` functions in a program. These functions are used to calculate amounts for different operations but do not take into account the decimals of the `paymentToken` being used. This can lead to incorrect amounts being processed and can have a significant impact on the user. For example, in one scenario, the `usdPlusAmount` is overestimated by a large amount, while in another, the user may end up paying less than intended. The report recommends that the program should handle the decimals of the payment token properly to avoid such issues.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The `previewDeposit()`, `previewMint()`, `previewWithdraw()` and `previewRedeem()` calculate returned amounts without accounting for the decimals of the `paymentToken`.

This can result in precision discrepancies during operations, leading to incorrect amounts being processed.

Assume the following scenario:

- The `paymentToken` has `18` decimals (e.g., `DAI`).
- The `USD`+ token has `6` decimals.

Impact on using each functions:

- `previewDeposit()`:

The `usdPlusAmount` to mint is calculated using the `paymentToken` decimals (18), resulting in an overestimated USD+ amount for the user (scaled up by `1e12`).

- `previewMint()`

The `paymentTokenAmount` required to mint is calculated using the USD+ decimals (6), causing the user to pay less than intended to mint USD+.

- `previewWithdraw()`

The transaction may revert due to insufficient funds, as the returned `usdPlusAmount` is calculated in 18 decimals, representing an unrealistically large amount.

- `previewRedeem()`

The `paymentTokenAmount` is tracked with the smaller USD+ decimals (6), leading to users receiving less value than expected when their redemption is fulfilled.

## Recommendations

Consider handling accepted payment token decimals across all calculations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Dinari_2024-12-07 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Dinari-security-review_2024-12-07.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

