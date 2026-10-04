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
solodit_id: 44525
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

Missing zero address check in setGov()

### Overview


This bug report discusses a medium severity issue where there is a missing zero address check in the setGov() function. This means that the gov address could accidentally be set to zero, resulting in the loss of access to gov forever. The report recommends adding a zero address check to prevent this issue.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

There is missing zero address check for _gov in setGov() function. This could lead to gov being accidentally set to zero address and its access to gov thus being lost forever. This is because only gov can change the address of gov, but once the gov is set as a zero address, the gov address can never be changed. This would result in all the onlyGov becoming uncallable.

**Recommendation**:

It is advised to add missing zero address check for the gov address.

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

