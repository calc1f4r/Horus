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
solodit_id: 54024
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

Oracle uses a deprecated Pyth Hermes API endpoint 

### Overview

See description below for full details.

### Original Finding Content

## Oracle Price Update Summary

## Context
- **File:** oracle.rs#L8

## Description
The oracle retrieves price updates through the Pyth network Hermes API by requesting the `/api/latest_vaas` endpoint. However, this endpoint is deprecated according to the Hermes API documentation available at [hermes.pyth.network/docs/#/rest/latest_vaas](https://hermes.pyth.network/docs/#/rest/latest_vaas).

## Recommendation
The Hermes API documentation indicates that `/v2/updates/price/latest` should be used instead.

## LayerN
- **Status:** Acknowledged. The documentation does not possess any security or end-of-life notes.

## Cantina Managed
- **Status:** Acknowledged.

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

