---
# Core Classification
protocol: Unimex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57410
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-27-Unimex.md
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

Missing zero address checks for `_from` and `_to` in `_transfer` function of UniMexStaking.sol

### Overview

See description below for full details.

### Original Finding Content

**Description**

In contract UniMexStaking.sol in function_transfer at lines 185-201, there are no checks for the_from and_to address parameters.

**Recommendation**

Add require checks to ensure those addresses are not the zero address.

**Re-audit comment**

Unresolved

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Unimex |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-27-Unimex.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

