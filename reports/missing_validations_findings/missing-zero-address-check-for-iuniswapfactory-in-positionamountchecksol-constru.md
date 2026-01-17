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
solodit_id: 57413
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

Missing zero address check for IUniswapFactory in PositionAmountCheck.sol constructor

### Overview

See description below for full details.

### Original Finding Content

**Description**

In contract PositionAmountCheck.sol in constructor at line 16 IUniswapFactory is initialized at an address that's not checked to not be zero.

**Recommendation**

Add a check for address not zero.

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

