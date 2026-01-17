---
# Core Classification
protocol: Maple Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54799
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/8ff1bbc8-5f91-4d10-9eea-cc9f88b82e62
source_link: https://cdn.cantina.xyz/reports/cantina_maple_apr2023.pdf
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Christoph Michel
  - Riley Holterhus
  - Jonatas Martins
---

## Vulnerability Title

Open-term loan manager functions missing isLoan validation 

### Overview

See description below for full details.

### Original Finding Content

## Context
open-term-loan-manager/LoanManager.sol#L33

## Description
The following open-term loan manager functions do not validate their `loan_` argument using the `isLoan` modifier:
- `proposeNewTerms`
- `rejectNewTerms`
- `callPrincipal`
- `removeCall`

This allows the pool delegate to forward a call to an arbitrary address.

## Recommendation
For extra safety, add the `isLoan` modifier to the four functions mentioned.

## Status
- **Maple**: Fixed in PR-59.
- **Cantina**: Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Maple Finance |
| Report Date | N/A |
| Finders | Christoph Michel, Riley Holterhus, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_maple_apr2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/8ff1bbc8-5f91-4d10-9eea-cc9f88b82e62

### Keywords for Search

`vulnerability`

