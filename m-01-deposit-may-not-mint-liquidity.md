---
# Core Classification
protocol: Radiant-July
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41032
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-July.md
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

[M-01] `deposit` may not mint liquidity

### Overview


This report discusses a bug in the `deposit` function of a program that determines whether bounds are defined. The issue is that the function does not mint liquidity if either `baseLower` or `baseUpper` is equal to `0`. However, in certain cases, such as when the price is `1` and the tick is `0`, this results in the function not minting liquidity even when bounds are defined. The recommendation is to only check for `0` in one of the variables, rather than both.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `deposit` function will mint liquidity only if bounds are defined. However, the method to determine whether bounds are defined is wrong.

When `baseLower` and `baseUpper` are both `0`, the bounds are undefined. However, the `deposit` function does not mint liquidity as long as one of `baseLower` and `baseUpper` is `0`. For uniswap pool v3, if the price is `1`, its tick is `0`. Therefore, this results in the `deposit` function not minting liquidity when bounds are already defined.

## Recommendations

If one of `baseLower` and `baseUpper` is not `0`, mint liquidity.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Radiant-July |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-July.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

