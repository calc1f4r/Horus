---
# Core Classification
protocol: 0x v3 Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13940
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/10/0x-v3-staking/
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
  - dexes
  - yield
  - services
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Alex Wade
  - Steve Marx
---

## Vulnerability Title

Delegated stake weight reduction can be bypassed by using an external contract  Won't Fix

### Overview


A bug report was filed regarding a feature of the 0x protocol that allows ZRX holders to delegate their staked ZRX to a market maker in exchange for a configurable percentage of the stake reward. The protocol currently gives a lower weight (90%) to ZRX staked by delegation. However, it is possible to bypass this weight reduction via external smart contracts, which gives a higher proportion of the stake reward to the ZRX staked through this contract. The development team believes there is some value to having a lower delegated stake weight as the default behavior, but recommends that the stake weight reduction for delegated stake be removed.

### Original Finding Content

#### Resolution



From the development team:



> 
> Although it is possible to bypass the weight reduction via external smart contracts, we believe there is some value to having a lower delegated stake weight as the default behavior. This can still approximate the intended behavior and should give a very slight edge to pool operators that own their stake.
> 
> 
> 




#### Description


Staking pools allow ZRX holders to delegate their staked ZRX to a market maker in exchange for a configurable percentage of the stake reward (accrued over time through exchange fees). When staking as expected through the 0x contracts, the protocol favors ZRX staked directly by the operator of the pool, assigning a lower weight (90%) to ZRX staked by delegation. In return, delegated members receive a configurable portion of the operator’s stake reward.


Using a smart contract, it is possible to represent ZRX owned by any number of parties as ZRX staked by a single party. This contract can serve as the operator of a pool with a single member—itself. The advantages are clear for ZRX holders:


* ZRX staked through this contract will be given full (100%) stake weight.
* Because stake weight is a factor in reward allocation, the ZRX staked through this contract receives a higher proportion of the stake reward.


#### Recommendation


Remove stake weight reduction for delegated stake.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | 0x v3 Staking |
| Report Date | N/A |
| Finders | Alex Wade, Steve Marx |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/10/0x-v3-staking/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

