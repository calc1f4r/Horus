---
# Core Classification
protocol: GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27201
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
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
  - Guardian Audits
---

## Vulnerability Title

POSU-1 | Cannot Liquidate 0 Remaining Collateral

### Overview


The bug report describes a potential issue where a position with $0 of remainingCollateral can avoid liquidation. This is due to two conditions, where the first one can be avoided if the MIN_COLLATERAL_USD was not set, and the second one reverts due to division by 0. The recommendation to resolve this issue was to add zero checks for such a scenario. The GMX Team implemented this recommendation and the issue has been resolved.

### Original Finding Content

**Description**

There is potential for a position with $0 of `remainingCollateral` to avoid liquidation. This is due to the fact that the first conditional can avoid being triggered if the `MIN_COLLATERAL_USD` was not set. If so, the second conditional would revert due to division by 0. Thus, a position that is liquidatable cannot be liquidated.

**Recommendation**

Add zero checks for such a scenario.

`if (remainingCollateralUsd == 0) return true;`

**Resolution**

GMX Team: The recommendation was implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | GMX |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

