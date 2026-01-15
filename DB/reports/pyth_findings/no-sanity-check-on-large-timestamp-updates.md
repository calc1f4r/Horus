---
# Core Classification
protocol: Layer N
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54012
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2
source_link: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
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
  - zigtur
  - Rikard Hjort
  - defsec
---

## Vulnerability Title

No sanity check on large timestamp updates 

### Overview

See description below for full details.

### Original Finding Content

## Issue Report

## Context
`engine.rs#L409`

## Description
Even if Pyth updates are trusted, it would make sense to have some sanity check against errors and ensure that time progresses somewhat steadily. An erroneous timestamp update could cause significant damage since a bug that, for example, shifts a timestamp far into the future would not be corrected and block all future price feed updates.

## Recommendation
Apply some sanity check, e.g., that the timestamp is not more than 1 hour into the future, and force that restriction to be manually overridden when necessary.

## LayerN
Fixed by emitting a warning to telemetry.

## Cantina Managed
Fixed. As the question of which timestamps would be valid is complex to automate, telemetry checks are an adequate mitigation and allow for manual adjustment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Layer N |
| Report Date | N/A |
| Finders | zigtur, Rikard Hjort, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2

### Keywords for Search

`vulnerability`

