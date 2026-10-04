---
# Core Classification
protocol: Blastoff
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37484
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-14-BlastOff.md
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

Misplaced stake limit validation in stake function of `LockedStakingPools` contract

### Overview


A bug has been identified in the `LockedStakingPools` contract that prevents the `TooManyStake` error from being triggered. This error is meant to restrict users from having more than 100 active stakes in a pool, but the check for this condition is incorrectly nested within another condition that checks if the user has no existing stakes. This means that the error can never be triggered, even if a user has more than 100 stakes. The recommendation is to check for the number of stakes before adding a new one to prevent this issue. The bug has been resolved. 

### Original Finding Content

**Severity**: Medium

**Status**:  Resolved

**Description**

The following check inside the stake function from `LockedStakingPools` contract attempts to restrict users from having more than 100 active stakes in any given pool. 

```solidity
   if (userStakeIds[poolId][msg.sender].length == 0) {
     if (userStakeIds[poolId][msg.sender].length > 100) revert TooManyStake();
     noUsersStaked[poolId] += 1;
   }
```
However, the check for `userStakeIds[poolId][msg.sender].length > 100` is incorrectly nested within another condition that checks if the user has no existing stakes (`length == 0`). This contradiction means that the check for exceeding the stake limit is only performed when the user has not yet staked anything (`length == 0`), which makes it impossible to trigger the `TooManyStake` revert under any circumstance.

**Recommendation**:

Before adding a new stake, check if the user already has 100 stakes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Blastoff |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-14-BlastOff.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

