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
solodit_id: 20920
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
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
  - AuditOne
---

## Vulnerability Title

Loans can be liquidated without checking loan duration

### Overview


This bug report concerns the forceLiquidateExpiredLoan function in a system. The function is responsible for liquidating loans that have expired. However, the function does not take into account the loan's duration and may prematurely mark a loan for liquidation if the current timestamp is beyond the loan's expiration buffer. To fix this bug, the report recommends including a check to ensure that the loan has exceeded its duration before proceeding with the liquidation.

### Original Finding Content

**Description**: 

In the provided forceLiquidateExpiredLoan function, it appears that loans are automatically liquidated if the current timestamp is beyond the loan's expiration buffer. However, the function does not account for the loan's duration before proceeding to the liquidation process. The loan might be within its valid duration but due to an insufficient expiration buffer, it may be prematurely marked for liquidation.

**Recommendations**: 

We recommend including a check to ensure that the loan has exceeded its duration before proceeding with the liquidation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

