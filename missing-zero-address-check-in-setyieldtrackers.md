---
# Core Classification
protocol: Unity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44523
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-02-21-Unity.md
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

Missing zero address check in setYieldTrackers()

### Overview


This bug report describes an issue with the yieldTrackers array in a program. The array may contain a zero address, which can cause problems when calling certain functions. To fix this, it is recommended to add checks for zero addresses and review the program's logic. The severity of this bug is considered medium and it has been acknowledged by the developers.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**


The yieldTrackers array can have zero address being set in its array of addresses via the setYieldTrackers function. This could lead to revert on function calls to recoverClaim() and claim() functions.

**Recommendation**: 

It is advised to add the missing zero address checks for yieldTrackers. It is also advised to review business and operational logic.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Unity |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-02-21-Unity.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

