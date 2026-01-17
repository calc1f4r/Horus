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
solodit_id: 37519
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro Finance.md
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

Repay allows to deposit without any upper limit

### Overview


The bug report is about a problem in two contracts, Contract Branch.sol and Contract Core.sol. The problem is that the method "repayRequest" in Contract Branch.sol allows users to repay their loan amount without checking the amount being repaid. This means that any user can repay any amount, even if it is more than the loan amount. In Contract Core.sol, the "repay" method allows users to deposit and mint ceTokens for any amount without any limit, even after the deposit cap has been reached. The recommendation is to add a check in the "repayRequest" method to prevent users from depositing more than the deposit cap. The bug has been marked as resolved.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

In Contract Branch.sol, the method repayRequest(...) allows any user to repay their loan amount. However, there is no check on the amount being repaid. 

In Contract Core.sol, the repay(..) has the logic to deposit any extra amount other than the repay amount and mint ceTokens for the user.
Any user can use this method to deposit and mint ceTokens for any amount without any upper limit even after the deposit cap has been reached.

**Recommendation**: Add a check on `repayRequest(...)` method to not allow deposit amount more than the deposit cap.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

