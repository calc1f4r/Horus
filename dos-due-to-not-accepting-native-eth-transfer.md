---
# Core Classification
protocol: Level  Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46586
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/612f3254-f6a6-420d-8d51-fb058e4af022
source_link: https://cdn.cantina.xyz/reports/cantina_level_money_october_2024.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Mario Poneder
  - Delvir0
  - Om Parikh
---

## Vulnerability Title

DoS due to not accepting native ETH transfer 

### Overview


The bug report is about an issue with LevelBaseReserveManager.sol, specifically on line 26. When depositing into a restating protocol, the contract will revert if the strategy or vault supports native restating or accrues rewards in ETH. This is because the contract does not have a receive or fallback function. To fix this, the recommendation is to add a receive or fallback function with appropriate access control to accept ETH. If the protocol does not want to interact with any currently deployed or future vaults or strategies that can transfer ETH, this should be documented explicitly.

### Original Finding Content

## LevelBaseReserveManager.sol Analysis

## Context
**File:** LevelBaseReserveManager.sol  
**Line:** 26

## Description
When depositing into the underlying restating protocol, which is either a vault or a strategy that delegates to the operator, there are important considerations. If the strategy/vault supports native restating or accrues rewards in ETH, then the contract will revert when withdrawing from such a strategy/vault because it does not implement the receive or fallback function. 

The protocol correctly implements `transferEther` to remove the ETH out of the contract once it is redeemed by the reserve manager.

## Recommendation
- Add a receive/fallback function with appropriate access control to accept ETH wherever required. 
- If the protocol does not wish to interact with any currently deployed or future vaults/strategies that can potentially transfer ETH, this should be documented explicitly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Level  Money |
| Report Date | N/A |
| Finders | Mario Poneder, Delvir0, Om Parikh |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_level_money_october_2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/612f3254-f6a6-420d-8d51-fb058e4af022

### Keywords for Search

`vulnerability`

