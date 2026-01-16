---
# Core Classification
protocol: Global Interlink
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44581
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global Interlink.md
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
  - Zokyo
---

## Vulnerability Title

Insufficient sanity checks for treasury creation

### Overview


The bug report is about a medium severity issue that has been resolved. In a specific function called `create_treasury`, there are no checks in place to ensure that certain variables have valid values. This could potentially lead to unexpected behavior and issues. The recommendation is to add checks to make sure that these variables have the correct values.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In contract token_vesting.move, in function `create_treasury` there are no sanity checks for the `total_lock_in_days`, `vesting_period_in_days` and `initial_lock_in_days` variables. It would be ideal to add checks to prevent these values from being zero or being invalid combinations. Also, the `vesting_period_in_days` and `initial_lock_in_days` parameters are not checked to make sure they are not greater than the variable `total_lock_in_days` which could lead to unexpected behavior if the vesting period 	is longer than the total lock period. Even if these values are set in a function that’s protected by admin rights, there is a chance that a mistake is made and not noticed before it leads to a possible issue.

**Recommendation**: 

Add sanity checks to make sure that these parameters are set to the correct values.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Global Interlink |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global Interlink.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

