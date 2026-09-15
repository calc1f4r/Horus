---
# Core Classification
protocol: Lumin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27236
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Lumin.md
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
  - Pashov
---

## Vulnerability Title

[M-02] Instant liquidations can happen after unpausing the protocol

### Overview


This bug report is about the `LoanManagerDelegator` contract, which is used by the Lumin protocol to manage loan interactions. If the protocol is paused for a long time, borrowers' collateral assets can decrease in value, and their loans may become liquidateable without a way for them to repay them or to add collateral, or even their loan term can pass. This can result in users losing value when the protocol is unpaused and their loan is instantly liquidated. The impact of this bug is high as users can be instantly liquidated and lose value, while the likelihood of this happening is low as it requires a long pause from the protocol admin.

To fix this issue, it is recommended to add a post-unpause grace period for liquidations to give time for users to repay their loans or add collateral. This will give users a chance to take action before their loan is liquidated.

### Original Finding Content

**Severity**

**Impact:**
High, as users can be instantly liquidated and lose value

**Likelihood:**
Low, as it requires a long pause from the protocol admin

**Description**

The `LoanManagerDelegator` contract through which all protocol interactions happen is pausable by the Lumin admin. In the case that the protocol is paused for a long time, borrowers' collateral assets can fall in price and their loans might become liquidateable without a way for them to repay them or to add collateral, or even their loan term can pass. This means when the protocol is unpaused the loan can get instantly liquidated resulting in a loss for the borrower.

**Recommendations**

Add a post-unpause grace period for liquidations to give time for users to repay their loans or add collateral.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Lumin |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Lumin.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

