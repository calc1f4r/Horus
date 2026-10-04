---
# Core Classification
protocol: Snailbrook
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35392
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-08-SnailBrook.md
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

`getRewards` For Stake Would Give Incorrect Rewards When User Has Withdrawn Already

### Overview


This bug report discusses an issue with the `stake.amount` not being emptied out when a user withdraws their stake. This can lead to incorrect results when using the `getRewardsForStake` function. The bug has been resolved and the recommendation is to empty out the `stake.amount` on withdrawal.

### Original Finding Content

**Severity** - Medium

**Status** - Resolved

**Description**

When a user withdraws their stake their `stake.status` is set to Withdrawn but the `stake.amount` still persists , though this is harmless since user can’t withdraw twice (due to the `stake.status` check in withdraw) this might lead to incorrect results when `getRewardsForStake` is queried . 
If a user has already withdrawn their stake the `stake.amount` is still the same and the function `getRewardsForStake` will still return the reward amount which is calculated with the `stake.amount`.

**Recommendation:**

Empty out the `stake.amount` on withdrawal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Snailbrook |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-08-SnailBrook.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

