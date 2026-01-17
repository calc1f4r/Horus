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
solodit_id: 31004
audit_firm: Oxorio
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom Stablecoin.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[ACKNOWLEDGED] Received amount of stablecoin is not validated in `FathomProxyWalletOwnerUpgradeable`

### Overview

See description below for full details.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[FathomProxyWalletOwnerUpgradeable.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L91 "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol" "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol") | contract `FathomProxyWalletOwnerUpgradeable` > function `openPosition` | 91

##### Description
In the function [`openPosition`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol#L91 "/contracts/main/fathom-SDK/FathomProxyWalletOwnerUpgradeable.sol") of the contract `FathomProxyWalletOwnerUpgradeable`, the transferred stablecoin amount equals the balance of the contract. This amount is not verified to match the parameter `_stablecoinAmount`. The function will not fail even if the factually transferred amount will be less than the requested `_stablecoinAmount` or even if no tokens will be transferred at all.
##### Recommendation
We recommend verifying that the transferred amount matches the requested amount.
##### Update
###### Client's response
We would like to exclude `FathomProxyWalletOwner` and  `FathomProxyWalletOwnerUpgradeable` from the audit scope.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

