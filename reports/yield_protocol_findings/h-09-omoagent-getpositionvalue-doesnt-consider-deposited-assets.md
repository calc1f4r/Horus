---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53327
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-09] OmoAgent: `getPositionValue()` doesn't consider deposited assets

### Overview


The bug report is about a high severity issue that affects the accuracy of calculating total assets in the `OmoVault` contract. The `totalAssets()` function calls `getPositionValue()` to calculate the total assets, but the `getPositionValue()` function does not include the value of deposited assets, leading to incorrect calculations and potential loss of funds for users. The recommendation is to modify the `getPositionValue()` function to include the value of deposited assets when calculating the total position value.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

Function `totalAssets()` calls `getPositionValue()` for all the dynamic accounts to calculate the total assets. In the `OmoAgent` contract, the `getPositionValue()` function does not take into account the deposited assets when calculating the position value. This leads to an incorrect calculation of `totalAssets()` in `OmoVault`, which can result in potential loss of funds for users due to inaccurate asset tracking.  
**Note**: agents can deposit assets (not just positions) into `OmoAgent` by `depositAssets()` function

## Recommendations

Modify `getPositionValue()` to include the value of deposited assets when computing the total position value.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

