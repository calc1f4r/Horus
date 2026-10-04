---
# Core Classification
protocol: Creditswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37108
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
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

Missing zero address checks in `ProtocolController`

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**:  Resolved

**Description**

There is missing zero address check for initialAdmin and `feeCollector_` parameter in `initialize()` function. Once set, it cannot be set again.

**Recommendation**:

It is advised to add a zero address check for the above functions.

**Comments**: The client said that the feeCollector can be set to the zero address explicitly, in which case no fees are collected (that’s an easy way to turn off all fees). This implementation was missed in some cases, fixed in commits 6e4b7cf and 4eec52a

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Creditswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

