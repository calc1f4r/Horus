---
# Core Classification
protocol: Mellow
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40580
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10
source_link: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
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
finders_count: 4
finders:
  - Kaden
  - Saw-mon and Natalie
  - deadrosesxyz
  - Akshay Srivastav
---

## Vulnerability Title

RebalanceParams.callback can steal accrued fees of liquidity NFTs during rebalance 

### Overview


This bug report discusses an issue with the rebalancing process in the Core.sol code. It explains that when liquidity NFTs are transferred to the RebalanceParams.callback address, there is a possibility for the address to claim the accrued fees of the NFT if the CallbackParams of a user's managed position are empty. This could result in the user's accrued fees being stolen. The report recommends validating the accrued fees to the NFT and notes that the issue has been fixed in a recent commit. The Cantina Managed team has also addressed the issue by not supporting empty CallbackParams. 

### Original Finding Content

## Vulnerability Report

## Context
Core.sol#L221-L223

## Description
During the rebalancing process, the liquidity NFTs are transferred to the `RebalanceParams.callback` address. In cases where the `CallbackParams` of a user's managed position are empty (a scenario when the user just wants rebalancing without gauge deposits), it could allow the `RebalanceParams.callback` address to claim the accrued fees of that NFT at the moment it receives the NFT for rebalancing. This essentially leads to the potential theft of the accrued fees from the user.

## Recommendation
Similar to the liquidity checks (Core.sol#L236), consider validating the accrued fees to the NFT.

## Mellow
Fixed in commit `736eef90`.

## Cantina Managed
The issue has been fixed by not supporting empty `CallbackParams`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Mellow |
| Report Date | N/A |
| Finders | Kaden, Saw-mon and Natalie, deadrosesxyz, Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10

### Keywords for Search

`vulnerability`

