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
solodit_id: 40581
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

LpWrapper deposits and withdraws will be bricked if Velodrome gauge is killed. 

### Overview


The bug report is about a problem in the LpWrapper contract, specifically in line 255. The issue is that when a user tries to withdraw their funds, the contract also tries to deposit them back into the Core contract. However, if the corresponding Velodrome gauge is no longer active, this process cannot be completed and the funds become stuck in the LpWrapper contract. The recommendation is to add an emergency withdraw function to prevent this from happening. The bug has been fixed in a recent commit and the attempt to withdraw from the gauge has been skipped in another part of the code.

### Original Finding Content

## Context: LpWrapper.sol#L255

## Description
Within the LpWrapper contract, all withdraws make a withdraw and deposit back in Core.sol. The problem is that in case the corresponding Velodrome gauge is killed, it will not allow for any new deposits to happen. This would lead to all funds within the LpWrapper forever stuck.

## Recommendation
Consider adding an emergency withdraw function.

## Mellow
Fixed in commit 736eef90.

## Cantina Managed
The attempt to withdraw from the gauge is skipped at VeloAmmModule.sol#L146.

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

