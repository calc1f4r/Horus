---
# Core Classification
protocol: SXT_2025-03-31
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63319
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SXT-security-review_2025-03-31.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-04] `stakingDelayStartTime` Not Reset After `claimUnstake()`

### Overview


The bug report is about a medium severity issue in a staking system. The `stakingDelayStartTime` variable is not being reset after the unstaking process is completed, leading to a delay in staking for users. This happens when the staking delay period is longer than the unstaking period. To fix this, the `stakingDelayStartTime` should be reset to 0 in the `claimUnstake()` function.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `stakingDelayStartTime` is initialized when `CollaborativeStaking::initiateUnstake()` is called, but it is never cleared or reset when the corresponding unstaking process is completed via `claimUnstake()`.

```solidity
    function claimUnstake() external onlyRole(STAKER_ROLE) {
        emit ClaimUnstake();

        IStaking(STAKING_ADDRESS).claimUnstake();
    }
```

As a result, even after the users have:
	1.	Staked funds,
	2.	Initiated unstaking,
	3.	Successfully claimed the unstaked tokens,

They are still subject to a staking delay before being able to stake again. This happens because the `withStakingDelay` modifier enforces the delay based on `stakingDelayStartTime`, which remains set.

This vulnerability exists when the `STAKING_DELAY_LENGTH` is longer than the `UNSTAKING_UNBONDING_PERIOD` defined in `Staking.sol`. In this case, the users have to wait an additional `STAKING_DELAY_LENGTH` even after the unstaking process is fully completed, which is unnecessary and can disrupt staking workflows and, also, delay participation in the staking.

## Recommendations

Consider resetting the `stakingDelayStartTime` in the `claimUnstake()` function to `0`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | SXT_2025-03-31 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SXT-security-review_2025-03-31.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

