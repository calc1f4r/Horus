---
# Core Classification
protocol: Threshold
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54720
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e
source_link: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
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
  - Alex The Entreprenerd
  - luksgrin
  - Kurt Barry
---

## Vulnerability Title

Misleading comment for TIMEOUT 

### Overview

See description below for full details.

### Original Finding Content

## Context: PriceFeed.sol#L37

## Description
The `TIMEOUT` constant is used for both Chainlink and Tellor, but the attached comment does not reflect that since it only names Chainlink.

## Recommendation
Consider changing the comment so that it is clear that the variable is used for Tellor too.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Threshold |
| Report Date | N/A |
| Finders | Alex The Entreprenerd, luksgrin, Kurt Barry |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e

### Keywords for Search

`vulnerability`

