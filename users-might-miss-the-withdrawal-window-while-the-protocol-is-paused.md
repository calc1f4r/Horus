---
# Core Classification
protocol: Isle Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45737
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
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

Users Might Miss The Withdrawal Window While The Protocol Is Paused

### Overview


This bug report describes an issue where users are unable to withdraw their tokens or repay their loans if the protocol is paused. This can result in missed withdrawal windows and defaulted loans. The recommendation is to either account for the paused timeframe or inform users in advance if the protocol will be paused.

### Original Finding Content

**Severity** - Low


**Status** - Acknowledged

**Description**: 

User withdrawals only happen in respective windows , which is current window +2  , but the user might miss the withdrawal window while the protocol was paused . The pausing mechanism does not extend the window time frame therefore if a user had his withdrawal window between x and y and the protocol was paused within this time frame , he would miss his window and now he has to remove some of his tokens when the protocol resumes in order to push his window to a new current window where he can withdraw.

Also, a loan might get subject to a default while the protocol was paused . In the paused state the user won’t be able to repay the loan and as soon as the system gets unpaused the loan is subject to a default and gets defaulted.

**Recommendation**:

Account for the paused timeframe within the withdrawal window or the users should be acknowledged of such behavior in advance.

**Client comment**: If for some reason the protocol must be temporarily paused, for example, if the pool admin is undergoing legal procedures to recover defaulted funds, we will inform users in advance that the protocol will be temporarily paused.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Isle Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

