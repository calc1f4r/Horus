---
# Core Classification
protocol: Sturdy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54510
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7dae5fff-ba32-4207-9843-c607f15464a3
source_link: https://cdn.cantina.xyz/reports/cantina_sturdy_sep2023.pdf
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
  - liquid_staking
  - lending
  - bridge
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Manuel
  - HickupHH3
---

## Vulnerability Title

DebtManager.manualAllocation is not considering the respect minimum idle feature in VaultV3.update_debt 

### Overview


The DebtManager Overview bug report discusses an issue with the manualAllocation function in the DebtManager.sol file. The function is used to adjust the debt for each silo in the VaultV3 contract. However, there is a problem when decreasing or withdrawing debt from a silo, as the function does not take into account the minimum total idle amount constraint set in the VaultV3 contract. This can lead to a revert of the function and incorrect allocation of debt. The recommendation is to update the function to consider the minimum idle constraint for each position or to use the actual new debt returned by the update_debt function. The developers have acknowledged the issue and suggest that when allocating data off-chain, the minimum idle amount and each silo's maximum debt should be considered to avoid any revert cases and ensure correct allocation.

### Original Finding Content

## DebtManager Overview

## Context
**File:** DebtManager.sol  
**Line:** 300

## Description
The `manualAllocation` function allows for the allocation of debt for each silo in the `VaultV3` by increasing or decreasing it. 

The `VaultV3.update_debt` function has a feature that respects the minimum total idle amount (see `VaultV3.vy`, Line 935). This constraint defines the minimum amount of assets in the `VaultV3` that should not be invested into silos. 

In the case of decreasing or withdrawing debt from a silo, if the minimum total idle constraint is violated, it would withdraw more funds than actually requested from the `update_debt` call. This fact is not considered in the `manualAllocation` function. It assumes the passed parameter `new_debt` to the `update_debt` will change the debt accordingly, which can lead to a revert of the `manualAllocation` function.

## Recommendation
The array passed into the `manualAllocation` function needs to consider the minimum idle constraint for each position. An alternative solution could be to consider the actual new debt returned by the `update_debt` function. A difference here needs to be considered in the upcoming `update_debt` calls for the successor.

## Sturdy
Acknowledged. When `zkVerifier` or the admin makes the allocation data off-chain, they need to consider the `minimum_idle_amount` and each silo's `maxDebt` amount to avoid revert cases and allocate correctly.

## Cantina
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sturdy |
| Report Date | N/A |
| Finders | Manuel, HickupHH3 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sturdy_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7dae5fff-ba32-4207-9843-c607f15464a3

### Keywords for Search

`vulnerability`

