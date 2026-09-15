---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40204
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e9c7968-9565-4b05-a8f2-f41ddc64ec27
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_alm_sept2024.pdf
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
  - m4rio
  - Jonatas Martins
---

## Vulnerability Title

Unused variables and missing check within ForeignController

### Overview

See description below for full details.

### Original Finding Content

## Analysis of ForeignController.sol

## Context
ForeignController.sol#L72-L76

## Description
Within the `ForeignController`'s constructor, the `psm` variable is initialized, supposedly being a `PSM3` that contains the following 3 assets: `usds`, `susds`, `usdc`. 

There is no check that verifies this is true in the constructor; we expect this to be handled in the deploy script. Additionally, the `usds` and `susds` variables are not utilized at all in the contract; the functions that deal with these assets actually receive the asset as a parameter.

## Recommendation
Consider whether the check that the `psm` has the right assets should be performed in the constructor. If not, consider removing the unnecessary variables.

## MakerDAO
Fixed in PR 26.

## Cantina Managed
Verified, fixed by removing the variables `usds` and `susds`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_alm_sept2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6e9c7968-9565-4b05-a8f2-f41ddc64ec27

### Keywords for Search

`vulnerability`

