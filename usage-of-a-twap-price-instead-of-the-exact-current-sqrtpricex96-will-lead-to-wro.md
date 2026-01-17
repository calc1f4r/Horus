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
solodit_id: 40582
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

Usage of a TWAP price instead of the exact current sqrtPriceX96 will lead to wrong calcula- tion of token amounts within the position 

### Overview


The bug report describes an issue with the LpWrapper contract, specifically on line 97. When users deposit funds, the contract uses a function called getAmountsForLiquidity to calculate the exact amounts of two tokens within the position. However, the problem is that the function uses an incorrect value for sqrtPriceX96, which is obtained from an oracle. This results in inaccurate token amounts being calculated and users depositing less than expected and at a different ratio than expected. The recommendation is to use the correct value for sqrtPriceX96 from the contract's slot0. The bug has been fixed in two commits by Mellow and Cantina Managed.

### Original Finding Content

## Issue Report: LpWrapper.sol#L97

## Context
When depositing in the `LpWrapper`, `getAmountsForLiquidity` is called in order to calculate the exact `token0` and `token1` amounts within the position. 

## Description
The problem is that the `sqrtPriceX96` used is not the current one, but rather the TWAP value returned from the oracle. This would lead to inaccurate token amounts being calculated, resulting in users depositing less than expected and at a different ratio than anticipated.

## Recommendation
Use the `slot0`'s `sqrtPriceX96`.

## Status
- **Mellow**: Fixed in commit `52c0aaf0`.
- **Cantina Managed**: Fixed.

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

