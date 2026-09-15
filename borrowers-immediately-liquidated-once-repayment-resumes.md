---
# Core Classification
protocol: Cedro Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37525
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro Finance.md
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

Borrowers immediately liquidated once Repayment resumes

### Overview


A bug has been reported that could potentially cause borrowers to be unfairly liquidated due to market fluctuations. This happens when both repayment and liquidation are paused, and then resumed at the same time. To avoid this issue, it is recommended to add a grace period after repayment resumes where borrowers cannot be liquidated. The client has also suggested informing users to keep their position healthy by depositing more collateral or repaying debt, even during a repayment pause.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

Given that liquidation is also paused along with repayment, if repayment is paused, during the pause the borrowers can become subject to liquidation due to market fluctuations. Now when repayment and liquidation are resumed simultaneously, borrowers will be liquidated immediately by liquidation bots unless they can front-run the bots transactions.

This will lead to borrowers being liquidated due to no fault of their own. 

**Recommendation**: 

It is advised to add a grace period after repayment resumes during which they can not be liquidated.

**Client commented**: 

We will inform users through our documents that users should always keep their position healthy either by depositing more collateral or repaying debt. Even if repay pauses, the borrower can keep health factor healthy by depositing.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Cedro Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

