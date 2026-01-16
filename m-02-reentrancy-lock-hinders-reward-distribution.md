---
# Core Classification
protocol: Hyperstable_2025-06-03
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63439
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-06-03.md
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

[M-02] Reentrancy lock hinders reward distribution

### Overview


The bug report describes a problem with the reward distribution system in two contracts, `GaugeV2` and `Voter`. When a user tries to claim their reward by calling `GaugeV2.getReward()`, a lock is put in place to prevent reentrancy, which is when a contract calls itself before the first call has finished. However, the problem arises when `Voter` calls back to `GaugeV2` during the reward distribution process, causing the call to fail because the lock is still active. This means that users are unable to receive their rewards. The report recommends following the example of another contract, `Gauge`, in order to fix the issue. 

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

A reentrancy lock conflict exists in the reward distribution flow between `GaugeV2` and `Voter` contracts. 

1. User calls `GaugeV2.getReward()`. The first `nonReentrant` lock is acquired when `getReward` is called:

```solidity
function getReward(address account, address[] memory tokens) external nonReentrant {
    require(msg.sender == account || msg.sender == voter);
    IVoter(voter).distribute(address(this));
    // ... rest of the function
}
```

2. This calls `Voter.distribute()` which then calls back to GaugeV2:

```solidity
IGauge(_gauge).notifyRewardAmount(base, _claimable);
emit DistributeReward(msg.sender, _gauge, _claimable);
```

3. The call to notifyRewardAmount will revert because the reentrancy lock is still active:

```solidity
function notifyRewardAmount(address token, uint256 amount) external nonReentrant {
    require(token != stake, "invalid reward");
    // ... rest of the function
}
```

This effectively breaks the reward distribution mechanism.

## Recommendations

Follow `Gauge`:

```solidity
        _unlocked = 1;
        IVoter(voter).distribute(address(this));
        _unlocked = 2;
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-06-03 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-06-03.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

