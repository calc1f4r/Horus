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
solodit_id: 27200
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

DPU-1 | Unable to Decrease Collateral

### Overview


This bug report deals with the `processCollateral` function, which does not allow users to decrease their collateral without closing their position. This is because the `collateralDeltaAmount` is initially set to `params.order.initialCollateralDeltaAmount().toInt256()`, which does not work for decrease orders. To address this issue, a recommendation was made to allow for `initialCollateralDeltaAmount` to be set for decrease orders. The GMX Team implemented this recommendation and the issue has been resolved.

### Original Finding Content

**Description**

In the `processCollateral` function, the `collateralDeltaAmount` is initially set to `params.order.initialCollateralDeltaAmount().toInt256()`, which cannot be set for decrease orders. Therefore, there is no way to decrease collateral from a position without closing the entire position.

**Recommendation**

Allow for `initialCollateralDeltaAmount` to be set for decrease orders so users are able to decrease their collateral without closing their position.

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

