---
# Core Classification
protocol: Karak-June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38497
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
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

[M-02] Operator's manager can pause vault actions

### Overview


The report discusses a medium severity bug in NativeVault, where the manager is given too much power and can disrupt the protocol's functionality. For example, the manager can pause the slashing of funds or prevent users from withdrawing. The report recommends removing the manager role, as the operator may not be fully trustworthy.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

When NativeVault is created, its manager is granted a role that allows him to pause different actions. With such power, the manager can break some functionality of the protocol.
An example of such actions is slashing. The manager can pause it and then Core contract will not be able to slash funds from the operator.
Another example: the manager can forbid users to withdraw.

## Recommendations

Think about removing the manager role, as the operator is not a fully trusted entity.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Karak-June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

