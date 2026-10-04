---
# Core Classification
protocol: Spool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56560
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-30-Spool.md
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
  - Zokyo
---

## Vulnerability Title

Anyone can call a function.

### Overview


The bug report is about a function called "notifyStrategyRemoved()" that is used to remove strategies from a vault. The problem is that there are no restrictions on who can use this function, which means anyone can remove all the strategies from the vault. The recommendation is to add a restriction on who can use the function to prevent this issue.

### Original Finding Content

**Description**

Line 568. Function notifyStrategyRemoved() is used to remove strategies from the vault,
however there are no restrictions on who is allowed to call this function. This way ,anyone can
remove all the strategies from the vault.

**Recommendation**:

Add a restriction on who is able to call function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Spool |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-30-Spool.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

