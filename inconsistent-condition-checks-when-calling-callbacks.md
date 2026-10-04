---
# Core Classification
protocol: Dahlia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53174
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443
source_link: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - kankodu
  - Yorke Rhodes
---

## Vulnerability Title

Inconsistent condition checks when calling callbacks 

### Overview

See description below for full details.

### Original Finding Content

## Context Information

## Context
`Dahlia.sol#L336`

## Description
In this context, `onDahliaSupplyCollateral` is only called when `callbackData.length` is non-zero, whereas for the other callbacks, the following check is performed:

```solidity
if (callbackData.length > 0 && address(msg.sender).code.length > 0) { ... }
```

## Recommendation
Make sure the conditions checked are consistent across the callback functionality or add an explanation as to why the extra check `address(msg.sender).code.length > 0` in this context is missing.

## Status
- **Dahlia:** Fixed in commit `bb8ce8fa`.
- **Cantina Managed:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Dahlia |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, kankodu, Yorke Rhodes |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443

### Keywords for Search

`vulnerability`

