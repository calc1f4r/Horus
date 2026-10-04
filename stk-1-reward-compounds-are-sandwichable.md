---
# Core Classification
protocol: Key Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26755
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-05-01-Key Finance.md
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
  - Guardian Audits
---

## Vulnerability Title

STK-1 | Reward Compounds Are Sandwichable

### Overview


This bug report describes a loophole that allows malicious actors to exploit the `updateAllRewardsForTransferReceiverAndTransferFee` function in the GMXKey system. The malicious actors can buy GMXKey, stake it right before the function is called, and receive a portion of the rewards meant for other stakers. They can then immediately claim the rewards, unstake, and sell GMXKey, thus stealing rewards from other stakers.

The bug report recommends a solution to this loophole, such as implementing a staking/unstaking fee or a “warmup period” where stakers cannot accrue rewards. The Key Team has adopted a new approach to rewards, including reward periods, as a resolution to this issue.

### Original Finding Content

**Description**

There exists no fee or lockup period associated with staking to receive a portion of the rewards compounded during the `updateAllRewardsForTransferReceiverAndTransferFee` function.
A malicious actor may simply buy GMXKey and stake right before the `updateAllRewardsForTransferReceiverAndTransferFee` function to immediately accrue a portion of the collected rewards that were meant to be attributed to other stakers. The malicious actor can then immediately claim these rewards, unstake and sell GMXKey after the reward compound, therefore stealing rewards from other stakers.

**Recommendation**

Consider implementing a staking/unstaking fee or a “warmup period” where stakers cannot accrue rewards.

**Resolution**

Key Team: A new approach to rewards including reward periods was adopted.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | Key Finance |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-05-01-Key Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

