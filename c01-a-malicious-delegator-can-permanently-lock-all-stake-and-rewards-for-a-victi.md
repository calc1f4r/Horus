---
# Core Classification
protocol: Audius Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11309
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/audius-contracts-audit/
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
  - dexes
  - cdp
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[C01] A malicious delegator can permanently lock all stake and rewards for a victim service provider and all of its honest delegators

### Overview


A bug has been identified in the Audius Protocol codebase, in which a malicious delegator can exploit the `DelegateManager.requestUndelegateStake` and `cancelUndelegateStake` functions to increase the value of the `spDelegateInfo[_target].totalLockedUpStake` variable. This can eventually cause the `totalBalanceOutsideStaking` to become less than the `spDelegateInfo[_target].totalLockedUpStake`, resulting in the `claimRewards` function to always revert. 

The malicious delegator can also prevent honest delegators from being able to undelegate their stake, and the victim service provider from being able to claim their rewards or successfully call the `ServiceProviderFactory.requestDecreaseStake` function.

The bug has been fixed by modifying the `cancelUndelegateStake` function so that it reduces the `spDelegateInfo[_target].totalLockedUpStake` variable by the pending `UndelegateStakeRequest` amount, in a pull request (#561).

### Original Finding Content

The [`DelegateManager.requestUndelegateStake` function](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L183) increases the value of the [`spDelegateInfo[_target].totalLockedUpStake`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L213) variable. However, if this request is cancelled via the [`cancelUndelegateStake` function](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L222), the `spDelegateInfo[_target].totalLockedUpStake` variable is not decreased.


This means that a malicious delegator can delegate to a target service provider, and then call `requestUndelegateStake` and `cancelUndelegateStake` repeatedly, causing `spDelegateInfo[_target].totalLockedUpStake` to grow arbitrarily large.


If the attacker makes `spDelegateInfo[_target].totalLockedUpStake` larger than [`totalBalanceOutsideStaking`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L341), then the `claimRewards` function will always revert [on line 364 of `DelegateManager.sol`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L364) when called by the victim service provider. In this way, the malicious delegator can permanently prevent the service provider from ever claiming any of their rewards.


This has additional negative security consequences.


First, since the victim service provider will not be able to claim their pending rewards, the [`_claimPending` function](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L763) will always return `true` after the end of the week in which the attack took place. This means that honest delegators who have delegated to the victim service provider will never be able to undelegate their stake because their calls to the `undelegateStake` function will revert [on line 252](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L252).


Second, this also means that the victim service provider cannot successfully call the [`ServiceProviderFactory.requestDecreaseStake` function](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ServiceProviderFactory.sol#L364) because it will revert [on line 369 of `ServiceProviderFactory.sol`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ServiceProviderFactory.sol#L369). So the victim service provider also has their stake permanently locked.


Consider modifying the `cancelUndelegateStake` function so that it reduces the `spDelegateInfo[_target].totalLockedUpStake` variable by the pending `UndelegateStakeRequest` amount.


***Update**: Fixed in [pull request #561](https://github.com/AudiusProject/audius-protocol/pull/561).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Audius Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/audius-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

