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
solodit_id: 54025
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

Auth admits Pyth update timestamps that are rejected by the engine 

### Overview

See description below for full details.

### Original Finding Content

## Context
- **File Locations**: `engine.rs` (Line 409), `auth.rs` (Lines 123-124)

## Description
In `auth.rs`, Pyth updates are rejected if the new timestamp is less than the current timestamp. However, in `engine.rs`, updates are rejected when the new timestamp is not greater than the current timestamp. This inconsistency allows updates to be unnecessarily passed to the engine when the timestamp is the same as the stored one.

## LayerN
- **Fixes**: Implemented in PR 1032 and PR 944.

## Cantina Managed
- **Status**: Fixed. The Pyth updates are no longer handled by the auth threads. Additionally, the timestamp check in `check_pyth_update` has been modified from `>` to `=>`.

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

