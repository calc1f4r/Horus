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
solodit_id: 11333
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/audius-contracts-audit/
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

[M10] Some state variables are not set during initialize

### Overview


This bug report is about the Audius contracts, which can be upgraded using the unstructured storage proxy pattern. This pattern requires the use of an initializer instead of the constructor to set the initial values of the state variables. In some of the contracts, the initializer is not initializing all of the state variables, such as the `stakingAddress` state variable in the `ClaimsManager` and `Governance` contracts. This means that it is possible to call functions without any staking address set, as they only check that the contract has been initialized.

The solution is to set all the required variables in the initializer. If there is a reason for leaving them uninitialized, the developer should document it and add checks on the functions that use those variables to ensure that they are not called before initialization. This bug has been fixed in pull request #589.

### Original Finding Content

The Audius contracts can be upgraded using the [unstructured storage proxy pattern](https://docs.openzeppelin.com/upgrades/2.8/proxies). This pattern requires the use of an initializer instead of the constructor to set the initial values of the state variables. In some of the contracts, the initializer is not initializing all of the state variables.


For example, in the [`initializer` function of the `ClaimsManager` contract](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ClaimsManager.sol#L78) the [`stakingAddress` state variable](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ClaimsManager.sol#L17) is not set. It can be set later by calling [`setStakingAddress`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ClaimsManager.sol#L163). However, this means that it is possible to call the [`processClaim` function](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ClaimsManager.sol#L227) and some others without any staking address set, because they only [check that the contract has been initialized](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ClaimsManager.sol#L232).


The same happens in the [`initializer` function of the `Governance` contract](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L122), which does not set the [`stakingAddress`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L20) either.


Consider setting all the required variables in the initializer. If there is a reason for leaving them uninitialized consider documenting it, and adding checks on the functions that use those variables to ensure that they are not called before initialization.


***Update**: Fixed in [pull request #589](https://github.com/AudiusProject/audius-protocol/pull/589).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

