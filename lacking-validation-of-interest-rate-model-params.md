---
# Core Classification
protocol: MetaStreet Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54775
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/d89f3fe2-d0ba-42fd-9625-02ca6cbca5e4
source_link: https://cdn.cantina.xyz/reports/cantina_metastreet_sep2023.pdf
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
  - HickupHH3
  - Anurag Jain
---

## Vulnerability Title

Lacking validation of interest rate model params 

### Overview

See description below for full details.

### Original Finding Content

## Context
**File:** WeightedInterestRateModel.sol  
**Lines:** 64-66  

## Description
There is lacking validation on the `tickExponential` and `tickThreshold` parameters.

- **tickThreshold** should be checked to be `<= 1e18` (or lesser even). Otherwise, no tick can meet the threshold, resulting in zero normalisation and distribution failure.
- **tickExponential** should be bounded within a certain range.
  - If `tickExponential` is below `1e18`, then it will assign a heavier weight to lower ticks. This could arguably be seen as a feature.
  - If `tickExponential` is above `1e36`, then all resultant weights will be zero, leading to zero normalisation as well.
  - A sufficiently high `tickExponential` can cause the weight to be zero after a certain number of assigned ticks.

## Recommendation
Have sanity checks for these parameters.

## MetaStreet
Resolved in commit `fbd7342`.

## Cantina
Fixed. These parameters are no longer settable by the pool creator, but have been made immutable, to be determined by the protocol admin upon deployment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MetaStreet Labs |
| Report Date | N/A |
| Finders | HickupHH3, Anurag Jain |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_metastreet_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/d89f3fe2-d0ba-42fd-9625-02ca6cbca5e4

### Keywords for Search

`vulnerability`

