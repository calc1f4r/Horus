---
# Core Classification
protocol: Defi Starter
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28739
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Defi%20Starter/DefiStarter%20Smart%20Contracts/README.md#1-potential-claiming-stuck-for-several-periods-after-withdraw
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

Potential claiming stuck for several periods after withdraw

### Overview


This bug report is about a division by zero issue in the StakingPool.sol contract. The issue occurs when the periodTotalSupply is zero, which can happen when the user stakes tokens in one period, claims the reward in the next period, and then stakes more tokens in the following period. This issue is not considered critical because it cannot be exploited to steal funds, but it should be fixed as soon as possible as it can break the desired contract logic. The issue has been fixed with two commits at https://github.com/defistarter/contracts/commit/670678d7d2fd01b4c059ab76535c849f556377b4 and https://github.com/defistarter/contracts/commit/07edefa4c5931e5fbef97c61d48062c606fc21c4.

### Original Finding Content

https://github.com/defistarter/contracts/blob/9ffe009ee6047ced669711dde14fe38483abdf7e/StakingPool.sol#L341

Here we have division by `periodTotalSupply`, in case if `periodTotalSupply` becomes zero that it will be impossible to claim any reward.

Attack flow:

*Assuming that we have 1 user and 5 periods.*

- at period 0: user stake 10 tokens  (`_historyTotalSupply[0]` = `10`, `user.period` = `0`)
- at period 1: user claimReward and withdraw all 10 tokens (`_historyTotalSupply[1]` = `0`,  `user.period` = `1`)
- at period 2: do nothing (`_historyTotalSupply[2]` = `0`, `user.period` = `1`)
- at period 3: user stake 20 tokens (`_historyTotalSupply[3]` = `20`,  `user.period` = `1`)
- at period 4: user try to `claimReward` and get error “SafeMath: division by zero”

- contract state at period 4 is:

    - `_historyTotalSupply` = `[10, 0, 0, 20, 0]`
    - `user.period` = `1`

    so if user try to claimReward we will get:
    - `savedTotalSupply` = `0` (https://github.com/defistarter/contracts/blob/9ffe009ee6047ced669711dde14fe38483abdf7e/StakingPool.sol#L326)
    - `periodTotalSupply` = `0` (https://github.com/defistarter/contracts/blob/9ffe009ee6047ced669711dde14fe38483abdf7e/StakingPool.sol#L333)

    and finally here we have division by zero here: https://github.com/defistarter/contracts/blob/9ffe009ee6047ced669711dde14fe38483abdf7e/StakingPool.sol#L341

We recommend to check the `periodTotalSupply` value before division and omit that in case of zero.

This particular issue is not marked as critical because that cannot be exploited to steal funds, but issues should be fixed ASAP due to that can break desired contract logic.

Status: *Fixed at https://github.com/defistarter/contracts/commit/670678d7d2fd01b4c059ab76535c849f556377b4, https://github.com/defistarter/contracts/commit/07edefa4c5931e5fbef97c61d48062c606fc21c4*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Defi Starter |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Defi%20Starter/DefiStarter%20Smart%20Contracts/README.md#1-potential-claiming-stuck-for-several-periods-after-withdraw
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

