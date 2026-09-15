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
solodit_id: 40274
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/18bed847-07eb-421d-99c5-9571f2885dba
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_psm_aug2024.pdf
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
  - Christoph Michel
---

## Vulnerability Title

Missing RateProvider check in the deploy script

### Overview

See description below for full details.

### Original Finding Content

## PSM3Deploy.sol Review

## Context
**File**: PSM3Deploy.sol  
**Line**: 18  

## Description
In the PSM3Deploy.sol contract, when the PSM contract is deployed, a RateProvider is passed as a parameter. However, there is a missing check to verify whether the rate provider has been properly initialized.

## Recommendation
Consider adding a check to see if `rateProvider.getConversionRate()` returns a value different than 0.

## Maker
Fixed in commit **6324e261**.

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
| Finders | m4rio, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_psm_aug2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/18bed847-07eb-421d-99c5-9571f2885dba

### Keywords for Search

`vulnerability`

