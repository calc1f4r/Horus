---
# Core Classification
protocol: Coinlend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20935
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
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
  - AuditOne
---

## Vulnerability Title

New fee should not be applied to ACTIVE loans Severity: Medium

### Overview


This bug report is about the setFeePercent() function in the protocol. This function allows the owner to change the fee, but the issue is that this new fee is also applied to ACTIVE loans. This is a problem because the users did not agree to pay the new fee when they created the loan, so the existing loans should not be applied with the new feePercent.

The recommendation is to record the current fee to the Loan struct at the time of creation. This will help avoid the issue of the new fee being applied to existing loans.

### Original Finding Content

**Description:** 

The owner can change the fee by using the setFeePercent() function. The problem is that this new fee is also applied to ACTIVE loans, which is not agreed upon by the users at the time of creation. Users only agreed to pay the old fee when they created a loan in the protocol, so existing loans in the protocol should not be applied with the new feePercent.

**Recommendations:** 

Consider recording the current fee to the Loan struct at the creation time to avoid this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Coinlend |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

