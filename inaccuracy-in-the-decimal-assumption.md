---
# Core Classification
protocol: Planar Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35320
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar Finance.md
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

Inaccuracy in the decimal assumption

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**:  Unresolved

**Description**:

The Presale contract has a hardcoded constant, `MIN_TOTAL_RAISED_FOR_MAX_PLANE`, which assumes the usage of a stablecoin (USDC) with 6 decimals. This design choice introduces a vulnerability when the contract is deployed on blockchain networks where the stablecoin or sale token has a different decimal configuration. The discrepancy in decimal handling can lead to significant miscalculations in the token sale mechanics, potentially allowing tokens to be sold for far less than their intended price.

**Recommendation**: 

Consider dynamically adjusting the `MIN_TOTAL_RAISED_FOR_MAX_PLANE` value based on the decimal configuration of the sale token at the time of contract deployment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Planar Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

