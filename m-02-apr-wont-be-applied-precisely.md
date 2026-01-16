---
# Core Classification
protocol: Rivus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58234
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Rivus-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] APR won't be applied precisely

### Overview


The function `rebase()` is not accurately calculating the share price increase and APR. This is because it is not using the `lastRebaseTime` when calculating the rate increase, and is instead assuming that 24 hours have passed since the last time. This results in an incorrect APR for some periods of time. To fix this, the recommendation is to use `duration = block.timestamp - lastRebaseTime` to accurately calculate the rate increase from the last rebase call.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The function `rebase()` handles the share price increase to apply the desired APR. The issue is that the code doesn't use `lastRebaseTime` when calculating rate increase and it assumes 24 hours have passed from the last time which couldn't not be the case. This would wrong APR for some of the time. For example if `rebase()` is called 1 hour sooner or later then for those 1 hour the share price rate would be wrong.

## Recommendations

Use `duration = block.timestamp - lastRebaseTime` to calculate the real rate increase that accrued from the last rebase call.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Rivus |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Rivus-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

