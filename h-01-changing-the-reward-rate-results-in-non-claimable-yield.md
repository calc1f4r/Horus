---
# Core Classification
protocol: Vetenet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34033
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2023-12-01-veTenet.md
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
  - Pashov
---

## Vulnerability Title

[H-01] Changing the reward rate results in non-claimable yield

### Overview


This bug report discusses a problem where rewards are not being distributed correctly to validators. This issue occurs when a specific method is called in a certain order, causing the rewards to not be properly calculated. The bug is considered to have a high impact because it results in validators losing out on their accrued rewards. To fix this, the report recommends calling a different method before updating a specific variable. This should only be done when the variable has already been set.

### Original Finding Content

**Severity**

**Impact:**
High, as accrued rewards won't be distributed to validators

**Likelihood:**
Medium, as it requires method to be called in a specific order

**Description**

The `setDailyRewardRate` in `RewardVault` resets the `lastReward` storage variable to the current day. This means that now when `RewardVault::distributeRewards` is called, only the duration since the latest `setDailyRewardRate` call and the current moment will be used to calculate the accrued rewards. The problem with this approach is if that before calling `setDailyRewardRate` there were accrued but unclaimed rewards, those rewards will not be claimable anymore and the validators will lose on them.

**Recommendations**

Call `distributeRewards` before you update `lastReward` in `setDailyRewardRate`. This should only be done when `lastReward` has already been set.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Vetenet |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2023-12-01-veTenet.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

