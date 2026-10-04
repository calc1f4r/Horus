---
# Core Classification
protocol: Magic Yearn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57532
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-17-Magic Yearn.md
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
  - zokyo
---

## Vulnerability Title

Incorrect storage of user rewards during staking in MyStaking.

### Overview


The bug report is about a function in a smart contract called MyStaking.sol that calculates rewards during staking. There is a problem where the rewards are being calculated incorrectly, allowing malicious users to increase their rewards unfairly. The recommendation is to fix the code so that rewards are stored correctly and there are no extra rewards given during staking. The issue has been resolved after a re-audit.

### Original Finding Content

**Description**

MyStaking.sol: function_stake(). During staking, the rewards are calculated with function claimableAmount(). This function calculates current accrued rewards and adds "userInfo[user].unclaimedAmount" to the claimable amount. After claimable rewards are calculated, they are added to "userInfo[msg.sender].unclaimedAmount" (Line 245), though unclaimed amount is already calculated. This way, malicious users can illegally increase their rewards.

**Recommendation**

Store rewards correctly so that there can't be any extra rewards during staking.

**Re-audit comment**

Resolved

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Magic Yearn |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-17-Magic Yearn.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

