---
# Core Classification
protocol: MorphL2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41880
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/207
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/168

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
finders_count: 7
finders:
  - 0xStalin
  - n4nika
  - p0wd3r
  - sammy
  - mstpr-brainbot
---

## Vulnerability Title

M-8: Stakers lose their commission if they unstake as they cannot claim their pending rewards anymore after unstaking

### Overview


This bug report is about an issue with stakers losing their commission when they unstake. This can happen if the staker is removed by an admin or if they are slashed. Even in these cases, they should still be able to claim their previously accrued rewards. The root cause of this issue is a modifier that only allows stakers to call the function for claiming commissions. There are no internal or external pre-conditions for this issue to occur. The attack path is when a staker stakes and accrues commissions, then either unstakes or gets removed, resulting in the loss of all accrued rewards. The impact of this bug is the loss of unclaimed rewards. The suggested mitigation is to remove the modifier and allow anyone to call the function for claiming commissions. The issue has been fixed by the protocol team in a recent pull request.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/168 

## Found by 
0xStalin, mstpr-brainbot, n4nika, p0wd3r, sammy, underdog, zraxx
### Summary

Once a staker unstakes or gets removed, they permanently lose access to all their accrued commissions.

This is a problem as it can either happen mistakenly or if the staker gets removed by an admin or slashed. However even in that case, they should still be able to claim their previously accrued rewards since they did not act negatively during that period.


### Root Cause

[`L2Staking.sol::claimCommission`](https://github.com/sherlock-audit/2024-08-morphl2/blob/98e0ec4c5bbd0b28f3d3a9e9159d1184bc45b38d/morph/contracts/contracts/l2/staking/L2Staking.sol#L215) has the `onlyStaker` modifier, making it only callable by stakers.


### Internal pre-conditions

None

### External pre-conditions

None

### Attack Path

Issue path in this case

* Staker stakes and accrues commissions over a few epochs
* Now either the staker unstakes or gets removed forcibly by the admin
* The staker has now lost access to all previously accrued rewards


### Impact

Loss of unclaimed rewards


### PoC

_No response_

### Mitigation

Consider removing the `onlyStaker` modifier and allow anyone to call it. This should not be a problem since normal users do not have any claimable commission anyways except if they were a staker before.



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/morph-l2/morph/pull/516

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | MorphL2 |
| Report Date | N/A |
| Finders | 0xStalin, n4nika, p0wd3r, sammy, mstpr-brainbot, underdog, zraxx |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/168
- **Contest**: https://app.sherlock.xyz/audits/contests/207

### Keywords for Search

`vulnerability`

