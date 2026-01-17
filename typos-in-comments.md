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
solodit_id: 41999
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/8f86c4a6-a42c-4541-a4b4-154fb8a3d919
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_psm_oct2024.pdf
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

Typos in comments

### Overview

See description below for full details.

### Original Finding Content

## Context
See below

## Description
- **IPSM3.sol#L95** - asset in the PSM (e.g., sUSDS). should be asset in the PSM.
- **README.md#L14** - swap between USDC, USDS, and sSUDS, should be swap between USDC, USDS, and sUSDS.
- **README.md#L18** - ...held by the PSM - While this is true now assets might be held by the PSM and the Pocket, even if the whole point of the pocket is that it's the PSM's pocket, no one should take assets out of it. Consider rephrasing it to include the Pocket functionality.

## Recommendation
Consider fixing the comments.

## Maker
Fixed in v1.0.0-rc.1.

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

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_psm_oct2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/8f86c4a6-a42c-4541-a4b4-154fb8a3d919

### Keywords for Search

`vulnerability`

