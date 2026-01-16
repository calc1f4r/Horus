---
# Core Classification
protocol: Symmio, Staking and Vesting
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55109
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/838
source_link: none
github_link: https://github.com/sherlock-audit/2025-03-symm-io-stacking-judging/issues/650

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
finders_count: 2
finders:
  - 0x73696d616f
  - ge6a
---

## Vulnerability Title

M-5: Double spending attack in the Vesting contract

### Overview


This bug report discusses an issue with the Vesting contract, specifically with the function resetVestingPlans(). This function is used by an administrator account to reset vesting plans for a list of users. The issue is that this function can potentially lead to double spending, where a user can claim their locked tokens twice. This is because the function does not check if the user has already claimed their tokens before resetting their vesting plan. This could result in loss of funds for both the protocol and users. No response or mitigation has been provided yet. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-03-symm-io-stacking-judging/issues/650 

## Found by 
0x73696d616f, ge6a

### Summary

The function resetVestingPlans() is called by an administrator account and resets vesting plans for a list of users, with the corresponding amount provided as input. The function calls _resetVestingPlans(), where it checks whether the given amount is greater than or equal to the claimed amount for the user. After that, it calls resetAmount() from LibVestingPlan. In this function, the state is updated, the new amount is recorded, and claimedAmount is set to 0.



### Root Cause

The issue here is that this can lead to double spending. Even though the user executing the request is trusted, they cannot know whether another transaction has been executed before theirs, in which the user whose vesting plan is being reset has withdrawn their locked amount by paying a penalty fee. If this happens, the user will be able to claim the same amount again after the reset, which would harm other users who might not be able to claim their rewards.

https://github.com/sherlock-audit/2025-03-symm-io-stacking/blob/main/token/contracts/vesting/Vesting.sol#L222-L237


### Internal Pre-conditions

None

### External Pre-conditions

None

### Attack Path

1. Trusted user sends a transaction for executes resetVestingPlans()
2. Regular user subject of this reset sends a transaction that is executed before the first one and claim their locked tokens as they pay a penalty
3. After the reset the user  is able to claim the tokens up to amount again

### Impact

Loss of funds for the protocol and for the users

### PoC

_No response_

### Mitigation

_No response_

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Symmio, Staking and Vesting |
| Report Date | N/A |
| Finders | 0x73696d616f, ge6a |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-03-symm-io-stacking-judging/issues/650
- **Contest**: https://app.sherlock.xyz/audits/contests/838

### Keywords for Search

`vulnerability`

