---
# Core Classification
protocol: Wallek
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35383
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Possible misuse of a variable.

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational

**Status**: Resolved

**Description**

TestStake::reStake()#1954. In the function 'reStake()', a variable 'totalWithdrawn is calculated by counting values from all the user's stakes. However, the additional of 'stakeAmount from stake is performed based on whether the amount', which is user re-stakes, is greater than 0. In contrast, it might be possible that it should be performed based on the value of previousAmount and whether its value is greater than 0. The issue is marked as info since auditors can't currently define the severity level of it since the variable 'totalWithdrawn is never used later in the code (See Low-2 issue).

**Recommendation:**

Verify if the value of variable amount` OR `previous Amount should be validated in "if" statement.
Post audit. Variable totalWithdrawn was removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Wallek |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

