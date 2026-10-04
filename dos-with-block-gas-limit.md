---
# Core Classification
protocol: Marginal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40542
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0496f8ff-ed7f-467f-8263-adfcc321121a
source_link: https://cdn.cantina.xyz/reports/cantina_solo_marginal_dao_apr2024.pdf
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
  - Kaden
---

## Vulnerability Title

DoS with block gas limit 

### Overview


The report discusses a bug in the MultiRewards contract, specifically in the function called "updateReward". This function is responsible for keeping track of rewards and is used in critical functions such as staking, withdrawing, and getting rewards. The problem is that the function uses an array called "rewardTokens" which can grow in size without any limit. This can cause an increase in gas costs, which can eventually exceed the block gas limit and permanently block the critical functions. This means that all staking and reward tokens will be stuck in the contract forever. The recommendation is to add a maximum length for the rewardTokens array to prevent this issue from occurring. This is considered a low risk bug.

### Original Finding Content

## Context

`MultiRewards.sol#L201-L210`

## Description

`MultiRewards.updateReward` is responsible for reward accounting logic and is executed at the start of critical functions: `stake`, `withdraw`, `getReward`, and `notifyRewardAmount`. The modifier loops over every reward token, checkpointing reward emissions.

The problem with this logic is that `rewardTokens` is an array that can grow in size to an undefined capacity without the ability to reduce the size of the array. As a result, the gas costs required to execute this logic can also grow to an undefined capacity. If the gas costs ever exceed the block gas limit, the critical functions executing this logic will be permanently blocked. Since this modifier is used on every function responsible for removing staking and reward tokens from the contract, this would result in all staking and reward tokens being permanently locked in the contract.

## Recommendation

Add and enforce a maximum length for the `rewardTokens` array, e.g. in `MultiRewards.addReward`:

```solidity
// Revert if we've already reached the max length
if (rewardTokens.length == MAX_REWARD_LENGTH) revert EXCEEDS_MAX_REWARD_LENGTH();
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Marginal |
| Report Date | N/A |
| Finders | Kaden |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_solo_marginal_dao_apr2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0496f8ff-ed7f-467f-8263-adfcc321121a

### Keywords for Search

`vulnerability`

