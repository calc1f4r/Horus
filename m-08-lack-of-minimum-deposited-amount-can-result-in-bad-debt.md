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
solodit_id: 57799
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

[M-08] Lack of minimum deposited amount can result in bad debt

### Overview


The PositionManager contract has a function called "deposit()" that lets users deposit assets into a supported vault with no minimum deposit size. This allows for the creation of very small positions, known as "dust deposits", that can be used as collateral for borrowing. However, if the health factor of these small positions falls below the minimum collateral ratio threshold, there is no incentive for liquidators to liquidate them. This leads to the accumulation of bad debt in the protocol. To prevent this, it is recommended to introduce a minimum deposit size for collateral so that users cannot open positions with very small amounts of assets.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the `PositionManager` contract, the `deposit()` function allows users to deposit assets into any supported vault with no minimum deposit size. This enables the creation of very small deposit positions, referred to as "dust deposits", where these small deposits can then be used as collateral to borrow against them.

However, if the **health factor** of these small positions falls below the **minimum collateral ratio (MCR)** threshold, there is **no incentive for liquidators** to liquidate them due to the low value of the collateral. As a result, these dust deposit positions remain open, causing the protocol to accumulate **bad debt**.

## Recommendations

Introduce a minimum deposit size for collateral to ensure that users cannot open positions with very small amounts of assets.

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

