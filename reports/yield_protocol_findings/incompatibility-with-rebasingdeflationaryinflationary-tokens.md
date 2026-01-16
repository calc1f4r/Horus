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
solodit_id: 20928
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

Incompatibility With Rebasing/Deflationary/Inflationary tokens

### Overview


This bug report is about the protocol not supporting rebasing/deflationary/inflationary tokens whose balance changes during transfers or over time. This means that the necessary checks are not being made to verify the amount of tokens transferred to contracts before and after the actual transfer to infer any fees/interest. Two recommendations are made to address the issue. Firstly, ensure that to check previous balance/after balance equals to amount for any rebasing/inflation/deflation. Secondly, add support in contracts for such tokens before accepting user-supplied tokens. Additionally, consider supporting deflationary / rebasing / etc tokens by extra checking the balances before/after or strictly inform users not to use such tokens if they don't want to lose them.

### Original Finding Content

**Description:**

 The protocol do not appear to support rebasing/deflationary/inflationary tokens whose balance changes during transfers or over time. The necessary checks include at least verifying the amount of tokens transferred to contracts before and after the actual transfer to infer any fees/interest.

**Recommendations:** 

Ensure that to check previous balance/after balance equals to amount for any rebasing/inflation/deflation

Add support in contracts for such tokens before accepting user-supplied tokens

Consider supporting deflationary / rebasing / etc tokens by extra checking the balances before/after or strictly inform your users not to use such tokens if they don't want to lose them.

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

