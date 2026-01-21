---
# Core Classification
protocol: Covalent
chain: everychain
category: uncategorized
vulnerability_type: upgradable

# Attack Vector Details
attack_type: upgradable
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 912
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-covalent-contest
source_link: https://code4rena.com/reports/2021-10-covalent
github_link: https://github.com/code-423n4/2021-10-covalent-findings/issues/45

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - upgradable
  - ownable

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[H-01] Usage of an incorrect version of Ownbale library can potentially malfunction all onlyOwner functions

### Overview


This bug report is about the WatchPug vulnerability in the DelegatedStaking.sol contract. The contract was designed to be an upgradeable proxy contract, however, the current implementation is using a non-upgradeable version of the Ownbale library. As a result, the owner of the contract is not set and all the onlyOwner functions will be inaccessible. The recommendation is to use the upgradeable version of the Ownbale library and change the initialize() function to include the __Ownable_init() call.

### Original Finding Content

## Handle

WatchPug


## Vulnerability details

https://github.com/code-423n4/2021-10-covalent/blob/ded3aeb2476da553e8bb1fe43358b73334434737/contracts/DelegatedStaking.sol#L62-L63

```solidity
// this is used to have the contract upgradeable
function initialize(uint128 minStakedRequired) public initializer {
```

Based on the context and comments in the code, the `DelegatedStaking.sol` contract is designed to be deployed as an upgradeable proxy contract.

However, the current implementaion is using an non-upgradeable version of the `Ownbale` library: `@openzeppelin/contracts/access/Ownable.sol` instead of the upgradeable version: `@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol`.

A regular, non-upgradeable `Ownbale` library will make the deployer the default owner in the constructor. Due to a requirement of the proxy-based upgradeability system, no constructors can be used in upgradeable contracts. Therefore, there will be no owner when the contract is deployed as a proxy contract.

As a result, all the `onlyOwner` functions will be inaccessible.

### Recommendation

Use `@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol` and `@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol` instead.

And change the `initialize()` function to:

```solidity
function initialize(uint128 minStakedRequired) public initializer {
    __Ownable_init();
    ...
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Covalent |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-covalent
- **GitHub**: https://github.com/code-423n4/2021-10-covalent-findings/issues/45
- **Contest**: https://code4rena.com/contests/2021-10-covalent-contest

### Keywords for Search

`Upgradable, Ownable`

