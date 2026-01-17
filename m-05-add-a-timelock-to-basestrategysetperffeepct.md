---
# Core Classification
protocol: Sandclock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42404
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-sandclock
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/178

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] Add a timelock to `BaseStrategy:setPerfFeePct`

### Overview


The bug report is about a suggestion to improve the security of a code in a project called Sandclock. The suggestion is to add a timelock to the functions that set important variables. This will increase trust in the project for its users. The report also mentions the tools used and steps to mitigate the issue. However, a member of the project team has acknowledged the suggestion but also pointed out that it may not completely eliminate the risk. Another member has mentioned that they will implement the suggestion by setting an admin as a timelock.

### Original Finding Content

_Submitted by Dravee_

To give more trust to users: functions that set key/critical variables should be put behind a timelock.

#### Proof of Concept

<https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/strategy/BaseStrategy.sol#L249-L253>

#### Tools Used

VS Code

#### Recommended Mitigation Steps

Add a timelock to setter functions of key/critical variables.

**[naps62 (Sandclock) acknowledged](https://github.com/code-423n4/2022-01-sandclock-findings/issues/178#issuecomment-1015430589):**
 > While this is a valid suggestion, it doesn't necessarily indicate a vulnerability in the existing approach. A timelock can indeed increase trust, but it never truly eliminates the same risk (i.e.: once the timelock finishes, the same theoretical attacks from a malicious operator could happen anyway)

**[ryuheimat (Sandclock) commented](https://github.com/code-423n4/2022-01-sandclock-findings/issues/178#issuecomment-1024395152):**
 > We will set admin as a timelock





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/178
- **Contest**: https://code4rena.com/reports/2022-01-sandclock

### Keywords for Search

`vulnerability`

