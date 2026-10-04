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
solodit_id: 42003
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ba3e40ff-baf9-4def-8ae0-21f4a9473184
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_alm_controller_oct2024.pdf
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

Missing PSM checks within the initialization of the Foreign Controller

### Overview

See description below for full details.

### Original Finding Content

## Controller Initialization Issue

## Context
`ControllerInit.sol#L252`

## Description
The `ForeignController` expects a `PSM3` instance that has `USDC`, `USDS`, and `SUSDS` as the underlying assets. The initialization script is currently missing a check to ensure that the `PSM` received as a parameter is configured correctly. Specifically, it should confirm that it has three assets: `USDC`, `USDS`, and `SUSDS`.

## Recommendation
Consider adding the following checks:
- `psm.usdc()` is equal to `addresses.usdc`
- `psm.usds()` is equal to `addresses.usds` (note: this entry needs to be added in the `addresses`)
- `psm.suds()` is equal to `addresses.susds` (note: this entry needs to be added in the `addresses`)

## Maker
Fixed in `PR-44`

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

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_alm_controller_oct2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ba3e40ff-baf9-4def-8ae0-21f4a9473184

### Keywords for Search

`vulnerability`

