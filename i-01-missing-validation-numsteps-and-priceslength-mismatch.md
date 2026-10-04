---
# Core Classification
protocol: Wild Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61787
audit_firm: Kann
contest_link: none
source_link: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Wild Protocol.md
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
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Kann
---

## Vulnerability Title

[I-01] Missing Validation — numSteps and prices.length Mismatch

### Overview

See description below for full details.

### Original Finding Content


## Severity

Informational

## Description

In the PriceCurve bondingCurveParams, no check ensures that numSteps equals prices.length. A mismatch could result in unexpected pricing behavior or runtime errors.

## Team Response

Fixed.


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | Wild Protocol |
| Report Date | N/A |
| Finders | Kann |

### Source Links

- **Source**: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Wild Protocol.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

