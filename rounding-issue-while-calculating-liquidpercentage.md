---
# Core Classification
protocol: Starter
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35708
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-starter.md
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

Rounding Issue While Calculating `liquidPercentage`

### Overview


The report describes a bug that has been fixed. The bug affected the calculation of `liquidPercentage` in a function called `_processRewards()`. This function creates a new deposit for rewards and calculates the `liquidPercentage` using the formula `user.liquidWeight*100 / user.totalWeight`. However, if the `totalWeight` of the user is greater than 100 times the `liquidWeight`, the `liquidPercentage` would round down to 0. This means that users with a small amount of liquid staked would receive 0 yield for their deposit. The recommendation is to use a higher precision for calculating `liquidPercentage` to avoid this issue in the future.

### Original Finding Content

**Severity** - Medium

**Status** - Resolved

**Description**

The `liquidPercentage` calculated inside `_processRewards()` (L773) is as follows →
```solidity
Deposit memory newDeposit = Deposit({
        tokenAmount: pendingYield,
        lockedFrom: uint64(block.timestamp),
        lockedUntil: uint64(block.timestamp + getRewardLockPeriod(_staker)), // staking yield for Reward Lock Period
        weight: depositWeight,
        liquidPercentage: (user.liquidWeight * 100) / user.totalWeight, //AUDIT-round
        isYield: true
      });
```

Here a new deposit is being created (for rewards) and the `liquidPercentage` is `user.liquidWeight*100 / user.totalWeight` , if the `totalWeight` of the user is > `100*liquidWeight` (quite possible if the user has staked a very little amount as liquid and rest non-liquid) then the liquidPercentage would round to 0. Therefore, a user with `liquidWeight > 0` will receive 0 yield for his deposit due to the rounding.

**Recommendation**:

Use higher precision for calculating `liquidPercentage`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Starter |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-starter.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

