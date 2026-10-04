---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5927
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/238

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - don't_update_state

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cccz
---

## Vulnerability Title

[M-19] When users transfer GiantLP, some rewards may be lost

### Overview


A bug has been discovered in the GiantMevAndFeesPool.sol file of the 2022-11-stakehouse GitHub repository. The bug causes users to lose some rewards when transferring GaintLP. This is because the beforeTokenTransfer function does not call StakingFundsVault.claimRewards to claim the latest rewards, resulting in a smaller accumulatedETHPerLPShare. To mitigate this issue, consider calling the claimRewards function before the beforeTokenTransfer calls updateAccumulatedETHPerLP().

### Original Finding Content


GiantMevAndFeesPool.beforeTokenTransfer will try to distribute the user's current rewards to the user when transferring GaintLP, but since beforeTokenTransfer will not call StakingFundsVault.claimRewards to claim the latest rewards, thus making the calculated accumulatedETHPerLPShare smaller and causing the user to lose some rewards.

### Proof of Concept

<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L146-L148>

### Recommended Mitigation Steps

Consider claiming the latest rewards from StakingFundsVault before the GiantMevAndFeesPool.beforeTokenTransfer calls updateAccumulatedETHPerLP()

**[vince0656 (Stakehouse) acknowledged and commented](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/238#issuecomment-1329443510):**
 > So the nuance here is that due to contract limitations, users should be encouraged for this specific case to claim rewards before transferring tokens due to the requirement of claim params that the contract wouldn't readily have when executing a transfer. We can document this limitation in detail and encourage users to always claim before transferring the tokens.

**[LSDan (judge) commented](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/238#issuecomment-1334589905):**
 > I think medium is appropriate for this issue given that we have a loss of funds if the user performs actions out of order.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/238
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Don't update state`

