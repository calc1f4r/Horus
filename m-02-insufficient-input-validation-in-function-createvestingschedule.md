---
# Core Classification
protocol: Moleculevesting
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20576
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-04-01-MoleculeVesting.md
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
  - Pashov
---

## Vulnerability Title

[M-02] Insufficient input validation in function `createVestingSchedule`

### Overview


This bug report is about the insufficient validation of the arguments of the `createVestingSchedule` function. If the arguments are not validated properly, it can lead to users never vesting their tokens, which is a high impact issue. However, the likelihood of this happening is low, as it requires a malicious or compromised admin or an error on their part. 

The report lists four problematic scenarios. The first scenario is that the `_start` argument can be a timestamp that has already passed or is too far away in the future. The second is that `_cliff` can be too big, preventing users from claiming. The third is that 1 is a valid value for `duration`, but the `!= 0` check is insufficient. The fourth is that if `_slicePeriodSeconds` is too big, the math in `_computeReleasableAmount` will have rounding errors.

The recommendation is to add sensible lower and upper bounds for all arguments of the `createVestingSchedule` method. This will help ensure that the arguments are properly validated, thus avoiding the potential issue of users not being able to vest their tokens.

### Original Finding Content

**Impact:**
High, as it can lead to users never vesting their tokens

**Likelihood:**
Low, as it requires a malicious/compromised admin or an error on his side

**Description**

The input arguments of the `createVestingSchedule` function are not sufficiently validated. Here are some problematic scenarios:

1. `_start` can be a timestamp that has already passed or is too far away in the future
2. `_cliff` can be too big, users won't be able to claim
3. 1 is a valid value for `duration`, the `!= 0` check is insufficient
4. If `_slicePeriodSeconds` is too big then the math in `_computeReleasableAmount` will have rounding errors

**Recommendations**

Add sensible lower and upper bounds for all arguments of the `createVestingSchedule` method.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Moleculevesting |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-04-01-MoleculeVesting.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

