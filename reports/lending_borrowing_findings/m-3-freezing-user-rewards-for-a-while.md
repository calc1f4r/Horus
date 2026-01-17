---
# Core Classification
protocol: Olympusdao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6679
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/50
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/187

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - cccz
  - ABA
  - Ruhum
  - mahdikarimi
  - xAlismx
---

## Vulnerability Title

M-3: freezing user rewards for a while

### Overview


This bug report is related to freezing user rewards. It was found by five people: cccz, mahdikarimi, ABA, xAlismx, GimelSec, and Ruhum. When a user claims some cached rewards, it is possible that their rewards will be frozen for a while. The issue is caused by a line of code in the internalRewardsForToken function, which can revert if the amount of debt is higher than the accumulated rewards for the user LP shares. This means that the user must wait until they have earned the same amount of rewards as the last time they claimed rewards in order to be able to claim them. The impact of this bug is that user rewards will be locked for a while. The code snippet and recommendation for fixing this issue are provided in the report. The tool used for this report was manual review. The recommendation for fixing this issue is to add the cached rewards to the total rewards in the code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/187 

## Found by 
cccz, mahdikarimi, ABA, xAlismx, GimelSec, Ruhum

## Summary
When a user claims some cached rewards it's possible that rewards be freezed for a while . 
## Vulnerability Detail
the following line in internalRewardsForToken function can revert because already claimed rewards has been added to debt so if amount of debt be higher than accumulated rewards for user LP shares it will revert before counting cached rewards value so user should wait until earned rewards as much as last time he/she claimed rewards to be able claim it . 
`uint256 totalAccumulatedRewards = (lpPositions[user_] * accumulatedRewardsPerShare) - userRewardDebts[user_][rewardToken.token];`
## Impact
user rewards will be locked for a while 
## Code Snippet
https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L354-L372
## Tool used

Manual Review

## Recommendation
add cached rewards to total rewards like the following line 
`uint256 totalAccumulatedRewards = (lpPositions[user_] * accumulatedRewardsPerShare + cachedUserRewards[user_][rewardToken.token] ) - userRewardDebts[user_][rewardToken.token];`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Olympusdao |
| Report Date | N/A |
| Finders | cccz, ABA, Ruhum, mahdikarimi, xAlismx, GimelSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/187
- **Contest**: https://app.sherlock.xyz/audits/contests/50

### Keywords for Search

`vulnerability`

