---
# Core Classification
protocol: Quail Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40648
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/083add5c-19a7-4c6d-9492-9079006ac222
source_link: https://cdn.cantina.xyz/reports/cantina_solo_quail_mar2024.pdf
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
  - Blockdev
---

## Vulnerability Title

Upgradable contracts used for immutable deployment 

### Overview


The bug report states that a contract called QuailFinance is using upgradable contracts, but there is no Proxy contract found. Upgradable contracts are meant to be used with Proxy contracts to avoid issues with delegatecall and storage slot clashing. However, the repository does not have a Proxy contract, indicating that the contracts will be deployed in a way that cannot be changed. The recommendation is to use a simple Ownable contract instead of OwnableUpgradable, remove all upgradable inherited contracts, remove the initializer function, and make adjustments in the constructor. If the user still wants to use a proxy, they should update the project to include a proxy contract.

### Original Finding Content

## QuailFinance.sol Analysis

## Context
QuailFinance.sol#L14-L14

## Description
Upgradable contracts are used but no Proxy contract found. Upgradable contracts are designed to be used with Proxy contracts due to the intricacies of delegatecall and storage slot clashing concerns. The repository doesn’t contain any proxy contract indicating that the contracts will be deployed in an immutable way.

## Recommendation
Consider using the simple `Ownable` contract instead of `OwnableUpgradable`, remove all Upgradable inherited contracts, remove the initializer function and adjust it in the constructor. If you want to use a proxy, then update the project to use a proxy contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Quail Finance |
| Report Date | N/A |
| Finders | Blockdev |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_solo_quail_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/083add5c-19a7-4c6d-9492-9079006ac222

### Keywords for Search

`vulnerability`

