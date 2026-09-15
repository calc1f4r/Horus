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
solodit_id: 37706
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-07-06-Vaultka.md
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
  - Zokyo
---

## Vulnerability Title

Debt could be relieved without repayment

### Overview


The bug report states that there is a critical issue in the code that has been resolved. The issue was found in a specific file called "lib.rs" in the "lending/programs/water" folder. The problem is with the "repay" function, which is supposed to increase the balance of a vault and decrease the borrowed amount. However, it is not receiving any payments to do so. The recommendation is to add a Transfer function to receive the payment from the borrower.

### Original Finding Content

**Description**

the 'repay' function increases a vault_sol_balance and decreases a borrowed_amount without receiving any payments
File: lending/programs/water/src/lib.rs: 614

**Recommendation**

add a Transfer function to get the payment from the borrower

**Re-audit comment**

Resolved

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-07-06-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

