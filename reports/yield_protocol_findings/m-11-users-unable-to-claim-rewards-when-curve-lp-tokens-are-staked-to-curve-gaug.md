---
# Core Classification
protocol: Notional Exponent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62503
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1001
source_link: none
github_link: https://github.com/sherlock-audit/2025-06-notional-exponent-judging/issues/595

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
finders_count: 5
finders:
  - bretzel
  - touristS
  - xiaoming90
  - Riceee
  - Bluedragon
---

## Vulnerability Title

M-11: Users unable to claim rewards when Curve LP tokens are staked to Curve Gauge.

### Overview


This bug report addresses an issue with the `AbstractRewardManager` contract in the Notional protocol. The contract is supposed to handle rewards for both the Booster and Gauge Reward Managers, but it is not currently able to claim rewards for the Gauge branch. This is due to a check in the code that causes the process to stop when the rewardPool is not set, which is the case when tokens are staked to the Gauge. As a result, users are unable to claim their rewards from the Curve Gauge. The impact of this bug is that protocol users cannot claim any rewards if the strategy uses Gauge instead of Booster. The suggested mitigation is to implement logic to claim rewards from the Gauge contract when the rewardPool is not set.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-06-notional-exponent-judging/issues/595 

This issue has been acknowledged by the team but won't be fixed at this time.

## Found by 
Bluedragon, Riceee, bretzel, touristS, xiaoming90

### Summary
According to the contest sponsors the `AbstractRewardManager` acts as the core logic contract for both Booster and Gauge Reward Managers. But claiming rewards for gauge branch is not implemented.

### Vulnerability details 
The issue here lies when the `CONVEX_BOOSTER` is not initialised. When a user enters a position via Notional, their assets are deposited to a curve pool and the vault receives LP tokens which are further staked for rewards in the Curve Gauge. 

When we take a look at the [`_stakeLpTokens`](https://github.com/sherlock-audit/2025-06-notional-exponent/blob/main/notional-v4/src/single-sided-lp/CurveConvex2Token.sol#L291-L298) used to stake the LP tokens, we see they are directly staked to Curve Gauge if Booster is not initialised. But the issue is claiming rewards is only implemented for the Convex Strategy and not for this scenario when LP tokens are staked to Gauge Strategy. 

Lets look at the flow of reward claim -->

1. User calls `claimRewards` on the router
2. `RewardManagerMixin::claimAccountRewards` is called
3. `RewardManagerMixing::_updateAccountRewards` is invoked
4. Delegate call to `updateAccountRewards` on `AbstractRewardManager`
5. This internally calls the `_claimVaultRewards` 

Given that the `AbstractRewardManager` is the underlying core contract logic for reward claim. Here we notice that the `_claimVaultRewards` function has a check  `if (rewardPool.rewardPool == address(0)) return;` 
This causes the control flow to return the claim execution process when the rewardPool is not set, which is the case when tokens are staked to Gauge. Resulting in users not able to claim their reward shares from the Curve Gauge. 

### Impact
The protocol users cannot claim any rewards if the strategy uses Gauge instead of Booster. 

### Code Snippets
https://github.com/sherlock-audit/2025-06-notional-exponent/blob/main/notional-v4/src/rewards/AbstractRewardManager.sol#L190

### Mitigation
When rewardPool == address(0), i.e., the strategy uses Gauge, instead of shortcircuiting, implement logic to claim rewards from the Gauge contract.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional Exponent |
| Report Date | N/A |
| Finders | bretzel, touristS, xiaoming90, Riceee, Bluedragon |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-06-notional-exponent-judging/issues/595
- **Contest**: https://app.sherlock.xyz/audits/contests/1001

### Keywords for Search

`vulnerability`

