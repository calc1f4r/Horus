---
# Core Classification
protocol: dYdX Perpetual Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11475
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/dydx-perpetual-audit/
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
  - yield
  - services
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Unsafe transparent proxy pattern

### Overview


This bug report is about the OpenZeppelin's AdminUpgradeabilityProxy contract, which is used to implement the unstructured storage proxy pattern. This pattern is important in order to prevent collisions between function signatures of the proxy and the implementation contracts. However, the PerpetualProxy contract has removed this check, which introduces a risk of function signature collisions. 

The dYdX team is aware of this and intends to mitigate the risk via extensive testing before deploying any new implementation contracts. It is recommended that the original transparent proxy pattern be followed by removing the PerpetualProxy contract and using the AdminUpgradeabilityProxy contract directly, and also defining a new role, different from the admin of the proxy, to interact with the functions that have the onlyAdmin modifier. 

The development team has responded, stating that they have comprehensive tests to ensure that there is no function signature collision.

### Original Finding Content

[OpenZeppelin’s `AdminUpgradeabiltyProxy` contract](https://github.com/OpenZeppelin/openzeppelin-sdk/blob/v2.6.0/packages/lib/contracts/upgradeability/AdminUpgradeabilityProxy.sol) is used to implement the [unstructured storage proxy pattern](https://blog.openzeppelin.com/upgradeability-using-unstructured-storage/) by having the [`PerpetualProxy` contract](https://github.com/dydxprotocol/perpetual/blob/c5e2b0e58aaf532d2c8b1f658d1df2f6a3385318/contracts/protocol/PerpetualProxy.sol) inherit from the former and managing `delegatecall`s to the [`PerpetualV1` contract](https://github.com/dydxprotocol/perpetual/blob/c5e2b0e58aaf532d2c8b1f658d1df2f6a3385318/contracts/protocol/v1/PerpetualV1.sol).


One of the features of the proxy model implemented in the library is the [transparent proxy pattern](https://blog.openzeppelin.com/the-transparent-proxy-pattern/), which prevents collisions between function signatures of the proxy and the implementation contracts by [not allowing the admin of the proxy to call the implementation contract](https://github.com/OpenZeppelin/openzeppelin-sdk/blob/de895221ffeb8a99a5314d0b203db2580a2074f7/packages/lib/contracts/upgradeability/BaseAdminUpgradeabilityProxy.sol#L117). This is an important security feature. However, the [`_willFallback` function](https://github.com/dydxprotocol/perpetual/blob/c5e2b0e58aaf532d2c8b1f658d1df2f6a3385318/contracts/protocol/PerpetualProxy.sol#L52) in `PerpetualProxy.sol` has removed this check.


The motivation behind removing the check is to allow for the same address to be the admin of both the `PerpetualProxy` contract *and* the `PerpetualV1` contract. However, this convenience introduces the risk of function signature collisions that could make functions on the implementation contract unreachable by the admin.


The dYdX team is aware of this and intends to mitigate the risk via extensive testing before deploying any new implementation contracts. But the risk could be removed entirely by separating the concerns — having one admin for upgrading the proxy, and different one for calling access-controlled functions on the implementation contract.


Consider following the original transparent proxy pattern by removing the `PerpetualProxy` contract and using the `AdminUpgradeabilityProxy` contract directly. Additionally, consider defining a new role, one different from the admin of the proxy, to interact with the functions that have the [`onlyAdmin`](https://github.com/dydxprotocol/perpetual/blob/c5e2b0e58aaf532d2c8b1f658d1df2f6a3385318/contracts/protocol/lib/Adminable.sol#L43) modifier.


**Update**: Unchanged. The development team responds, “We have comprehensive tests to ensure that there is no function signature collision.”

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | dYdX Perpetual Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/dydx-perpetual-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

