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
solodit_id: 40206
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

The psm.to18ConversionFactor() call can be cached

### Overview

See description below for full details.

### Original Finding Content

## Code Review Summary

## Context
- **File:** MainnetController.sol
- **Lines:** #L246, #L276

## Description
The `psm.to18ConversionFactor()` call can be cached as this variable is immutable in the psm.

## Recommendation
Consider caching this variable into an immutable variable.

## MakerDAO
Fixed in commit `5ea7f6d2`.

## Cantina Managed
Verified.

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

