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
solodit_id: 20925
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

Significant Rounding Error in Loan-to-Value Calculation

### Overview


This bug report discusses an issue with the getLTVOfLoan function in which the calculation of the loan-to-value (LTV) ratio involves a division by 1e18 for both tokenLendingTotalValue and tokenCollateralTotalValue. This division could cause a significant loss of precision, leading to the LTV ratio being rounded down to zero, even when the actual value should be higher. This could prevent loans from being liquidated when they should be, leading to potential loss of funds for lenders.

To solve this problem, it is recommended to remove the division by 1e18 as it is not necessary due to the fact that we divide tokenLendingTotalValue by tokenCollateralTotalValue afterwards, which cancels out the decimal effect. This will help to increase the LTV precision and get an accurate value of the borrower's position.

### Original Finding Content

**Description:**

In the getLTVOfLoan function, the calculation of the loan-to-value (LTV) ratio involves a division by 1e18 for both tokenLendingTotalValue and tokenCollateralTotalValue. This division can lead to a significant loss of precision, especially for small amounts of tokens. This could potentially result in the LTV ratio being rounded down to zero, even when the actual value should be higher. This could prevent loans from being liquidated when they should be, leading to potential loss of funds for lenders.

**Recommendations:** 

To mitigate this issue, remove division by 1e18 as it is not necessary due to the fact that we divide tokenLendingTotalValue by tokenCollateralTotalValue afterwards, which cancel the decimal effect. This will help to increase the LTV precision, to get an accurate value of the borrower's position.

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

