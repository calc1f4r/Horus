---
# Core Classification
protocol: Tangent_2025-10-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63884
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
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

[L-16] Incorrect Unit Validation for `startCutPrice`

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The RewardAccumulator contract validates startCutPrice and endCutPrice parameters against 1e18, implying that these values should be in 18-decimal precision.
`        require(_rcParam.startCutPrice <= 1e18, StartCutPriceTooHigh());
`
However, in the function _calculateRC, both values are multiplied by 1e12, meaning the implementation actually expects them to be stored as 6-decimal prices. This inconsistency means the upper-bound validation check (<= 1e18) is applied in the wrong scale, allowing overly large input values and breaking the intended reward cut curve.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tangent_2025-10-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

