---
# Core Classification
protocol: Ouroboros_2025-06-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63454
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2025-06-30.md
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

[L-08] Missing validation for `stagingDuration` in `UniswapV3Staker`

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

In `UniswapV3Staker.createIncentive`, the `stagingDuration` parameter is only validated when the emission style is `Vested`, but not when it is `Dripped`. This is inconsistent with the documentation, which clearly states that both `Dripped` and `Vested` emissions support `stagingDuration`.

As a result, invalid values (e.g., excessive durations) may be set for `Dripped` emissions, leading to unexpected behavior during reward claiming. This issue is avoided in `ERC20Staker.createERC20Incentive`, which correctly validates `stagingDuration` for both emission styles.


Consider updating `UniswapV3Staker.createIncentive` to validate `stagingDuration` regardless of whether the emission style is `Dripped` or `Vested`, as long as it is not `Regular`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ouroboros_2025-06-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2025-06-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

