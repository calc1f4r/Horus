---
# Core Classification
protocol: pSTAKE Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13312
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/08/pstake-finance/
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

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  -  Eli Leers

  -  Sergii Kravchenko
  - Shayan Eskandari
---

## Vulnerability Title

Reward rate changes are not taken into account in LP staking

### Overview


The pSTAKE Finance team has implemented a new Emission logic for pToken and other reward tokens in StakeLP, which ensures rewards are only distributed after updating the Reward Pool. This addresses the potential issue of rewards varying depending on when users call the `calculateRewardsAndLiquidity` function. Currently, the amount of rewards depends on when the function is called, and the reward amount can even decrease over time. This is due to two main factors: changes in the reward rate, and not every liquidity provider staking their LP tokens. The team recommends an algorithm that does not incentivize users to gather rewards earlier or later.

### Original Finding Content

#### Resolution



Comment from pSTAKE Finance team:



> 
> Have implemented two new Emission logic for pToken & Other Reward Tokens in StakeLP which mandatorily distributes rewards only after updating the Reward Pool, thereby fixing this potential issue.
> 
> 
> 




#### Description


When users update their reward (e.g., by calling the `calculateRewards` function), the reward amount is calculated according to all reward rate changes after the last update. So it does not matter when and how frequently you update the reward; in the end, you’re going to have the same amount.


On the other hand, we can’t say the same about the lp staking provided in the `StakeLPCoreV8` contract. The amount of these rewards depends on when you call the `calculateRewardsAndLiquidity` function, and the reward amount can even decrease over time.


Two main factors lead to this:


* Changes in the reward rate. If the reward rate is decreased at some point, it’s getting partially propagated to all the rewards there were not distributed yet. So the reward of the users that didn’t call the `calculateRewardsAndLiquidity` function may decrease. On the other hand, if the reward rate is supposed to increase, it’s better to wait and not call `calculateRewardsAndLiquidity` for as long as possible.
* Not every liquidity provider will stake their LP tokens. When users provide liquidity but do not stake the LP tokens, the reward for these Stokens is still going to the Holder contract. These rewards getting proportionally distributed to the users that are staking their LP tokens. Basically, these rewards are added to the current reward rate but change more frequently. The same logic applies to that rewards; if you expect the unstaked LP tokens to increase, it’s in your interest not to withdraw your rewards. But if they are decreasing, it’s better to gather the rewards as early as possible.


#### Recommendation


The most preferred staking solution is to have an algorithm that is not giving people an incentive to gather the rewards earlier or later.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | pSTAKE Finance |
| Report Date | N/A |
| Finders |  Eli Leers
,  Sergii Kravchenko, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/08/pstake-finance/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

