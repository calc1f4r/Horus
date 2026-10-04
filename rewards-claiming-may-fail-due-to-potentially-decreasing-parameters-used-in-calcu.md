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
solodit_id: 57919
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#2-rewards-claiming-may-fail-due-to-potentially-decreasing-parameters-used-in-calculation
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

Rewards claiming may fail due to potentially decreasing parameters used in calculation

### Overview


The `DIAWhitelistedStaking` contract has a problem with its reward calculation and claiming process. This can prevent users from claiming their rewards and principal amount. The issue occurs when the contract owner decreases the `rewardRatePerDay` or the user partially unstakes their `principal` amount. This can result in the `getRewardForStakingStore` function returning a lower value than the `currentStore.reward`, causing an assertion to fail. To fix this, it is recommended to remove the `currentStore.reward` and `currentStore.paidOutReward` variables and the `assert` statement. Instead, the `rewardToSend` variable should be calculated using the `getRewardForStakingStore` function. Only the `getRewardForStakingStore` function should be used to calculate rewards, as the staking start time is updated every time rewards are paid out. This issue has been resolved in conjunction with another critical issue.

### Original Finding Content

##### Description
In the `DIAWhitelistedStaking` contract, there is a potential issue in the reward calculation and claiming logic that could lead to reward claims being blocked. The issue arises from the following sequence:
1. In the `updateReward` function, there's an assertion:
```solidity
assert(reward >= currentStore.reward);
```
2. This assertion can fail due to two factors:
- `rewardRatePerDay` can be decreased by the contract owner
- `currentStore.principal` can be decreased during partial principal unstaking
3. When either of these values decreases, the reward calculation in `getRewardForStakingStore`:
```solidity
return (rewardRatePerDay * passedDays * currentStore.principal) / 10000;
```
may return a value lower than `currentStore.reward, causing the assertion to fail.
4. This issue is particularly problematic because:
- After the first reward claim, currentStore.reward is set to 0
- This blocks both reward and principal claiming for the user
<br/>
##### Recommendation
We recommend removing the internal accounting for the `currentStore.reward` and `currentStore.paidOutReward` variables and the mentioned assertion `assert(reward >= currentStore.reward);`. `rewardToSend` variable, which is used inside `unstake` and `unstakePrincipal` functions, should be calculated based on the value returned from the `getRewardForStakingStore` function. `currentStore.paidOutReward` can be kept just as a accumulator. It will be enough to have only the `getRewardForStakingStore` to calculate the rewards as the staking start time is updated every time the rewards are paid out.

> **Client's Commentary:**
> This has been fixed in conjunction with Critical-1

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#2-rewards-claiming-may-fail-due-to-potentially-decreasing-parameters-used-in-calculation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

