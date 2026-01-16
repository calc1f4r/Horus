---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57915
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#3-missing-reward-accumulator-initialization-in-stake-creation
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Missing Reward Accumulator Initialization in Stake Creation

### Overview


The bug report identifies an issue with the `_internalStakeForAddress` function in the `DIAStakingCommons` contract. The reward accumulator is not properly initialized when a new stake is created, which allows stakers to claim all rewards, regardless of when they started staking. This could potentially lead to incorrect reward distribution and loss of funds. The report recommends adding initialization of the reward accumulator value during stake creation and changing the reward calculation in the `_getTotalRewards` function to account for stored values. The client also suggests using the `_updateRewardAccumulator` function to ensure accurate reward calculations from the start of staking. 

### Original Finding Content

##### Description
This issue has been identified within the `_internalStakeForAddress` function of the `DIAStakingCommons` contract.
The reward accumulator (`rewardAccumulator`) is not initialized when a new stake is created. This oversight allows stakers to claim all rewards that have ever been accumulated by the contract, regardless of when they started staking, because of the following line: `stakerDelta = rewardAccumulator - currentStore.rewardAccumulator`. As the `currentStore.rewardAccumulator` wasn't initialized, `stakerDelta` would be equal to the value of the global `rewardAccumulator`. A similar issue exists in the `DIAWhitelistedStaking._getTotalRewards()` function, where `rewards` variable is calculated using only the `rewardAccumulator` without subtracting the `currentStore.rewardAccumulator`.
The issue is classified as **Critical** severity because it could lead to incorrect reward distribution and potential loss of funds through unauthorized reward claims.
<br/>
##### Recommendation
We recommend adding the initialization of the `rewardAccumulator` value during stake creation in the `_internalStakeForAddress` function to ensure proper reward tracking from the moment of staking. Also, `reward` calculation in the `_getTotalRewards` should be changed to properly account for the stored `currentStore.rewardAccumulator`.

> **Client's Commentary:**
> Both stake() and stakeForAddress() invoke _updateRewardAccumulator() and pass the most recent rewardAccumlator to the _internalStakeForAddress() function. This value is then used to initialize the newStore.rewardAccumulator, & newStore.initialRewardAccumulator variables. The former will continue to increment and track reward progression over time, while the latter remains constant to offset any accumulated rewards prior to the stake's startTime, ensuring accurate reward calculations from the moment staking begins.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#3-missing-reward-accumulator-initialization-in-stake-creation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

