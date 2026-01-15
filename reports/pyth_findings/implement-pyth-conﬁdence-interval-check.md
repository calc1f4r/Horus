---
# Core Classification
protocol: Layer N
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53999
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2
source_link: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
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
finders_count: 3
finders:
  - zigtur
  - Rikard Hjort
  - defsec
---

## Vulnerability Title

Implement pyth conﬁdence interval check 

### Overview


This bug report is about a system that uses price data from Pyth without checking if it falls within the provided confidence interval. This could lead to using unreliable data and potentially cause financial loss or system instability during volatile market conditions. The recommendation is to implement a check for the confidence interval and take appropriate action if the price falls outside the interval. The fix is in progress and the market will be frozen if the confidence interval is too wide. The accepted width is currently set to 10% on either side and can be adjusted. The bug has been fixed by freezing the market when the confidence interval is too large and implementing more conservative calculations for account health.

### Original Finding Content

## Context: pyth.rs#L192

## Description
Currently, the system uses price data from Pyth without explicitly checking if the price falls within the provided confidence interval. This could lead to using potentially unreliable price data in volatile market conditions or during unusual events.

## Impact
- Risk of using inaccurate or unreliable price data.
- Potential for financial loss or system instability during high market volatility.
- Missed opportunity to implement protective measures for users during uncertain market conditions.

## Recommendation
Implement a check to ensure the price falls within the confidence interval provided by Pyth. If the price is outside this interval or if the interval is unusually wide, take appropriate action (e.g., use a conservative price, pause certain operations). Check Pyth's confidence intervals documentation.

## LayerN
Fix in progress. The market will be frozen if the 95% confidence interval is too wide. The accepted width is parametric, currently set to 10% on either side, and can be adjusted.

## Cantina Managed
Fixed. Freezing the market when price confidence interval is too large. Using confidence interval for more conservative account health calculations is also in progress.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Layer N |
| Report Date | N/A |
| Finders | zigtur, Rikard Hjort, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2

### Keywords for Search

`vulnerability`

