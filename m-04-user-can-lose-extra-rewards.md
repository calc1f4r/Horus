---
# Core Classification
protocol: veToken Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6125
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-vetoken-finance-contest
source_link: https://code4rena.com/reports/2022-05-vetoken
github_link: https://github.com/code-423n4/2022-05-vetoken-findings/issues/15

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

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - csanuragjain
---

## Vulnerability Title

[M-04] User can lose extra rewards

### Overview


This bug report is about a vulnerability in the VE3DRewardPool.sol contract. This vulnerability allows the rewardManager to delete extra rewards that have been staked for users. This means that existing stakers will not be able to claim these extra rewards, and the funds will be locked with no one having access to them.

The proof of concept outlines how this vulnerability could be exploited. It involves the rewardManager adding two extra reward tokens, A and B, and then a user making a deposit of 1000. This stakes the extra rewards A and B for the user. The rewardManager then calls clearExtraRewards, which removes the extraRewards object. As a result, the user has no way of retrieving the staked extra rewards A and B of amount 1000.

The recommended mitigation steps to fix this vulnerability involve the rewardManager withdrawing and claiming all existing stakes on extra rewards before clearing them. This will ensure that users are not left without access to their extra rewards.

### Original Finding Content

_Submitted by csanuragjain_

rewardManager can at anytime delete the extra Rewards. This impacts the extra rewards earned by existing staker. The existing staker will have no way to claim these extra rewards. Since these extra rewards have been staked for all users making a deposit BaseRewardPool.sol#L215 so basically the extra reward gets locked with no one having access to this fund. Need to be fixed for BaseRewardPool.sol as well

### Proof of Concept

1.  rewardManager adds 2 extra reward token A,B using addExtraReward
2.  User X makes a deposit of amount 1000 using stake function
3.  This stakes extra rewards A,B for this user
4.  rewardManager now calls clearExtraRewards which removes extraRewards object
5.  User X has now no way to retrieve the staked extra rewards A,B of amount 1000

### Recommended Mitigation Steps

If rewardManager wants to clear extra rewards then all existing stakes on extra rewards must be withdrawn and claimed so that user extra rewards are not lost.

**[solvetony (veToken Finance) disagreed with severity and commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/15#issuecomment-1156597107):**
 > Not an issue of the user staked fund, but we need to add call at pool factory for `clearExtraRewards()`. 

**[Alex the Entreprenerd (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/15#issuecomment-1190943684):**
 > The warden has shown how, due to admin privilege, extra rewards could stay stuck in the contract.
> 
> Because this is contingent on a malicious admin, I believe Medium Severity to be more appropriate.
> 
> Notice that the rewards would be lost forever as there doesn't seem to be any `sweep` function which instead would allow the admin to take the reward tokens.
> 
> My recommendation is to remove the function to `clearExtraRewards` as it doesn't seem to help but it can indeed cause issues.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | veToken Finance |
| Report Date | N/A |
| Finders | csanuragjain |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-vetoken
- **GitHub**: https://github.com/code-423n4/2022-05-vetoken-findings/issues/15
- **Contest**: https://code4rena.com/contests/2022-05-vetoken-finance-contest

### Keywords for Search

`vulnerability`

