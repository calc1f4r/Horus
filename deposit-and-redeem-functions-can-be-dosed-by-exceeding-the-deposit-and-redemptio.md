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
solodit_id: 42049
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/99c7abab-0ff5-4e0e-a796-b1294271ca25
source_link: https://cdn.cantina.xyz/reports/cantina_level_money_sep2024.pdf
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
  - Delvir0
  - tchkvsky
  - MiloTruck
  - xiaoming90
---

## Vulnerability Title

Deposit and redeem functions can be DOSed by exceeding the deposit and redemption cap 

### Overview


The report discusses a bug in the LevelMinting smart contract, specifically in lines 105 and 113. The bug allows for a maximum number of stablecoins to be minted per block, but it is possible for the cooldown for redemptions to be turned off. This means that users can immediately withdraw their assets without waiting for the cooldown period. In a low-cost environment, this can be exploited by malicious users to repeatedly deposit and withdraw 10000 coins in a single transaction, leading to innocent users being unable to deposit or withdraw. The recommendation is to impose a fee on deposits and withdrawals to prevent this attack. The bug has been acknowledged by Level Money and Cantina and is considered low risk.

### Original Finding Content

## Vulnerability Report

## Context
- LevelMinting.sol#L105
- LevelMinting.sol#L113

## Description
There is a maximum number of stablecoins that can be minted per block. In the current design, it is possible that the cooldown for redemptions is turned off. In this case, users can immediately execute the `redeem()` function to withdraw assets. 

Assuming that the deposit cap and redemption cap are both set to **10,000**. In an L2 environment where the gas fee is cheap, malicious users can perform a Denial of Service (DoS) on the deposit and redemption processes by atomically depositing and redeeming **10,000** within a single transaction every block, thus resulting in the cap being reached. As such, innocent users attempting to deposit or redeem will encounter a revert.

## Recommendation
Consider imposing a fee on deposits and/or withdrawals to deter such an attack.

## Level Money
Acknowledged.

## Cantina
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Level  Money |
| Report Date | N/A |
| Finders | Delvir0, tchkvsky, MiloTruck, xiaoming90 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_level_money_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/99c7abab-0ff5-4e0e-a796-b1294271ca25

### Keywords for Search

`vulnerability`

