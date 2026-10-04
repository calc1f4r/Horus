---
# Core Classification
protocol: Resolv_2024-12-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44391
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Resolv-security-review_2024-12-09.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-01] Missing upper limit validation

### Overview

See description below for full details.

### Original Finding Content

The `setUpperBoundPercentage` and `setLowerBoundPercentage` functions in `RlpPriceStorage` contract lack validation to ensure bound percentages don't exceed the `BOUND_PERCENTAGE_DENOMINATOR` (1e18).

Especially if `lowerBoundPercentage` > `BOUND_PERCENTAGE_DENOMINATOR`, the `setPrice` function will always revert because: `currentPrice` < `(currentPrice * lowerBoundPercentage / BOUND_PERCENTAGE_DENOMINATOR)`.

It's recommended to add validation to ensure bound percentages don't exceed `BOUND_PERCENTAGE_DENOMINATOR`. Otherwise, setPrice() will revert due to underflow in the lower bound percentage calculation. This would prevent the SERVICE_ROLE from updating the prices in a timely manner, leading to possible stale prices.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Resolv_2024-12-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Resolv-security-review_2024-12-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

