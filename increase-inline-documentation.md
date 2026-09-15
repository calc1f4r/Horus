---
# Core Classification
protocol: Centrifuge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54424
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/693b6f24-6e47-4194-97b0-356d10dc1df6
source_link: https://cdn.cantina.xyz/reports/cantina_centrifuge_oct2023.pdf
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
finders_count: 2
finders:
  - Liam Eastwood
  - Sujith Somraaj
---

## Vulnerability Title

Increase inline documentation 

### Overview

See description below for full details.

### Original Finding Content

## Code Review Summary

## Context
`src/*`

## Description
The repository has limited comments (inline documentation) within the code, and critical functions lack adequate explanations. This makes understanding the protocol's operations difficult when reviewing the code.

## Recommendation
Ensure every function within the protocol has accompanying comments. This will provide clear documentation throughout the codebase.

## Centrifuge
This is more about coding style than an actual issue. Other protocols such as MakerDAO also adopt a similar style where comments are limited to:
1. External functions (in our case, mainly the liquidity pool contract)
2. Code that is not understandable on its own

I believe we comment where needed, and adding additional comments would clutter the code more.

## Cantina
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Centrifuge |
| Report Date | N/A |
| Finders | Liam Eastwood, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_centrifuge_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/693b6f24-6e47-4194-97b0-356d10dc1df6

### Keywords for Search

`vulnerability`

