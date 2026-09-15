---
# Core Classification
protocol: Anvil Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41268
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/anvil-protocol-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Risk of Storage Collision in Proxy Contract

### Overview


This bug report is about a problem with the AnvilGovernorDelegator.sol proxy contract. The contract does not follow the ERC-1967 standard for proxy storage slots, which can cause a storage collision with the logic contract. This means that if the logic contract upgrades and introduces a state variable, the proxy contract storage will collide and could lead to a contract takeover or make the contract inoperable. The suggestion is to follow the ERC-1967 standard and use unstructured storage approaches for proxy implementations. This bug has been resolved in a recent pull request at commit 0a5cb12.

### Original Finding Content

The [AnvilGovernorDelegator.sol](https://github.com/AmperaFoundation/sol-contracts/blob/c6e940c12044c8994f778c978e34582449229df8/contracts/governance/AnvilGovernorDelegator.sol) proxy contract does not follow the [ERC\-1967](https://eips.ethereum.org/EIPS/eip-1967) standard for proxy storage slots. The contract stores the implementation address in a non\-random slot, which can lead to a storage collision with the logic contract if some state variables are in use.


The [AnvilGovernorDelegate.sol](https://github.com/AmperaFoundation/sol-contracts/blob/c6e940c12044c8994f778c978e34582449229df8/contracts/governance/AnvilGovernorDelegate.sol) logic contract does not have any state variables using the storage slots. However, if the logic contract upgrades in the future and introduces a state variable, the proxy contract storage will collide, leading to a contract takeover due to the collision of the `_owner` variable or making the contract entirely inoperable due to the collision of the `_implementation` variable.


Consider following the ERC\-1967 standard and [utilize unstructured storage](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies#unstructured-storage-proxies) approaches for proxy implementations.


***Update:** Resolved in [pull request \#298](https://github.com/AmperaFoundation/sol-contracts/pull/298) at commit [0a5cb12](https://github.com/AmperaFoundation/sol-contracts/commit/0a5cb12882fc97eb2bcfe9e55279e70ce86553cf).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Anvil Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/anvil-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

