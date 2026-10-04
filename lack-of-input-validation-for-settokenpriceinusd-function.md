---
# Core Classification
protocol: Blastoff
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37494
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-14-BlastOff.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Lack of Input Validation for `setTokenPriceInUSD` Function

### Overview

See description below for full details.

### Original Finding Content

**Severity** : Informational

**Status** : Resolved

**Description** :

The `setTokenPriceInUSD` function in the `IDOPoolAbstract` contract lacks input validation, allowing for the setting of an IDO price to any value without restrictions. This poses a risk as it enables the contract owner to arbitrarily change the IDO price to potentially unfair or nonsensical values.

**Recommendation** : 

Implement input validation within the `setTokenPriceInUSD` function to ensure that the IDO price is within acceptable bounds. Use require statements to enforce these conditions and provide meaningful error messages for invalid inputs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Blastoff |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-14-BlastOff.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

