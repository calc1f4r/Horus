---
# Core Classification
protocol: Fathom Stablecoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30999
audit_firm: Oxorio
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom Stablecoin.md
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
  - Oxorio
---

## Vulnerability Title

[ACKNOWLEDGED] Missing `setOwner` function in `FathomProxyWalletOwner`, `FathomProxyWalletOwnerUpgradeable`

### Overview


The report discusses a bug in the `FathomProxyWalletOwner` and `FathomProxyWalletOwnerUpgradeable` contracts, specifically in the `buildProxyWallet` function. The bug lies in the `build` call to the `ProxyWalletRegistry` contract, where the `_owner` address is incorrectly passed as `address(this)`. This means that if the owner of the `FathomProxyWalletOwner` contract decides to change ownership and migrate to another address, it won't be possible. The report recommends reviewing the logic and adding an implementation for changing ownership in the affected contracts. The client has responded by excluding these contracts from the audit scope.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwner.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol#L72 "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwner.sol") | contract `FathomProxyWalletOwner` > function `buildProxyWallet` | 72
[FathomProxyWalletOwnerUpgradeable.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L71 "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol") | contract `FathomProxyWalletOwnerUpgradeable` > function `buildProxyWallet` | 71

##### Description
In the function `buildProxyWallet` of the contracts `FathomProxyWalletOwner` and `FathomProxyWalletOwnerUpgradeable`, in the `build` call to the `ProxyWalletRegistry` contract, the `_owner` address is passed as `address(this)`. This means that the `FathomProxyWalletOwner` is a direct owner of the `proxyWallet` contract in the `ProxyWalletRegistry` contract. However, if the EOA address, which is the owner of the `FathomProxyWalletOwner` contract, decides to change ownership and migrate to another address, it won't be possible. The EOA address is not an owner of the deployed proxy in the `ProxyWalletRegistry` contract, and the call to the `setOwner` function will revert. At the same time, the `FathomProxyWalletOwner` and `FathomProxyWalletOwnerUpgradeable` contracts are missing the `setOwner` function implementation.
##### Recommendation
We recommend reviewing the existing logic, adding an implementation for changing the ownership of the proxy in the `FathomProxyWalletOwnerUpgradeable` and `FathomProxyWalletOwner` contracts.
##### Update
###### Client's response
We would like to exclude `FathomProxyWalletOwner` and  `FathomProxyWalletOwnerUpgradeable` from the audit scope.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Oxorio |
| Protocol | Fathom Stablecoin |
| Report Date | N/A |
| Finders | Oxorio |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom Stablecoin.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

