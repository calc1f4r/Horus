---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40510
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/2c5aba7f-d561-4b2b-bbcc-184095521c35
source_link: https://cdn.cantina.xyz/reports/cantina_competition_aave_may2024.pdf
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
  - StErMi
---

## Vulnerability Title

swaptovariable natspec is incorrect 

### Overview

See description below for full details.

### Original Finding Content

## Context
IPool.sol#L384

## Description
The `swapToVariable` function is described as "Permission-less movement of stable positions to variable." From the official docs:

> Allowing any address to swap any stable rate user to variable, without changing anything else in the position.

The natspec documentation instead states that the function allows the owner of the debt position to swap his own debt from stable to variable.

## Recommendation
Update the natspec to document the real behavior and scope of the function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_aave_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/2c5aba7f-d561-4b2b-bbcc-184095521c35

### Keywords for Search

`vulnerability`

