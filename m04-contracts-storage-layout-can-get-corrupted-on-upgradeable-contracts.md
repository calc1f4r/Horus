---
# Core Classification
protocol: Notional Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11150
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/notional-audit/
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
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M04] Contracts storage layout can get corrupted on upgradeable contracts

### Overview


The Notional protocol uses the OpenZeppelin/SDK upgradeable contracts to manage upgrades in the system, which follows the unstructured proxy pattern. This upgradeability system consists of a proxy contract which users interact with directly and a second contract which contains the logic. It is important to take into account any potential changes in the storage layout of a contract, as there can be storage collisions between different versions of the same implementation. This can lead to critical errors in the contracts. To avoid this, it is important to check whether there were changes in the storage layout before upgrading a contract by saving the storage layout of the implementation contract’s previous version and comparing it with the storage layout of the new one. Additionally, the openzeppelin/upgrades plugins can be used to cover some of these scenarios.

### Original Finding Content

The Notional protocol uses a copy of some of the [OpenZeppelin/SDK upgradeable contracts](https://github.com/OpenZeppelin/openzeppelin-sdk/tree/v2.8.2/packages/lib/src) to manage upgrades in the system, which follows [the unstructured proxy pattern](https://blog.openzeppelin.com/upgradeability-using-unstructured-storage/).


This upgradeability system consists of a proxy contract which users interact with directly and that is in charge of forwarding transactions to and from a second contract. This second contract contains the logic, commonly known as the implementation contract.  

When using this particular upgradeability pattern, it is important to take into account any potential changes in the storage layout of a contract, as there can be storage collisions between different versions of the same implementation. Some possible scenarios are:


* When changing the order of the variables in the contract
* When removing the non-latest variable defined in the contract
* When changing the type of a variable
* When introducing a new variable before any existing one
* In some cases, when adding a new field to a struct in the contract


There is no certainty that the storage layout will remain safe after an upgrade. Violating any of these storage layout restrictions will cause the upgraded version of the contract to have its storage values mixed up, and can lead to critical errors in the contracts.


Consider checking whether there were changes in the storage layout before upgrading a contract by saving the storage layout of the implementation contract’s previous version and comparing it with the storage layout of the new one. Additionally, consider using the [openzeppelin/upgrades](https://github.com/OpenZeppelin/openzeppelin-upgrades) plugins which already cover some of these scenarios.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Notional Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/notional-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

