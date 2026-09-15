---
# Core Classification
protocol: Heurist
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37702
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-07-01-Heurist.md
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

Missing Sanity Checks in initialize Function

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational

**Status**: Resolved

**Description**

The initialize function in the `ZkImagine` contract sets initial values for various parameters, including the mint fee, referral discount, cooldown window, and start timestamp. However, it lacks sanity checks to ensure that these parameters are valid and within reasonable ranges. Without these checks, the contract may be initialized with incorrect or invalid values, E.g. the mint fee could be initialized to zero.

**Recommendation**: 

Add sanity checks to the initialize function to validate the parameters and ensure they are within acceptable ranges. This will help prevent initialization with unintended or invalid values and ensure the contract operates as expected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Heurist |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-07-01-Heurist.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

