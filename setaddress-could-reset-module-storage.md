---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35171
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
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

setAddress Could Reset Module Storage

### Overview


The RizLendingPoolAddressesProvider contract has a function called `_updateImpl` that creates a new proxy when a specific `id` has a zero value in the `_addresses` mapping. However, if the owner calls the `setAddress` function with a zero value for the `id` and then upgrades the module, the contract will create a new proxy and reset all stored data, potentially causing issues for users. This can be fixed by either removing the `setAddress` function or restricting its parameter to any implementation besides the zero address. This issue has been resolved in a recent update to the code.

### Original Finding Content

The [`_updateImpl` function](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPoolAddressesProvider.sol#L261) of the `RizLendingPoolAddressesProvider` contract deploys a new proxy when the `_addresses` mapping has a zero value for the particular `id`. Otherwise, it makes a call to the deployed proxy to initiate the upgrade to the new implementation.


However, if the owner calls the [`setAddress` function](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPoolAddressesProvider.sol#L98) with a zero value for the particular `id` and then upgrades the implementation of the module, the contract will read the zero address, create a new proxy, and start the storage from scratch in that module. This would reset all stored data for that module, potentially causing functionality to become stuck or users to lose funds.


As the `_updateImpl` function already takes into account whether a proxy has been deployed or not, consider either removing the manual `setAddress` functionality from the code, or restricting its parameter to any implementation besides the zero address.


***Update:** Resolved in [pull request \#82](https://github.com/radiant-capital/riz/pull/82) at commit [8e7584e](https://github.com/radiant-capital/riz/pull/82/commits/8e7584e8b850f3411462cf45112a93c1198fd6f7). The `setAddress` function no longer accepts the zero address as input.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

