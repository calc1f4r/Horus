---
# Core Classification
protocol: Gain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58475
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-19-Gain.md
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
  - zokyo
---

## Vulnerability Title

Ensure No Fee On Transfer Tokens

### Overview

See description below for full details.

### Original Finding Content

**Description**

The fiat token is supposed to be a token pegged to the US dollar. There are certain tokens which incurs a fee on transfer. This means that everytime x amount of a fee on transfer tokenis transferred to an address, that address receives an amount x - fee. Due to this reason if the fiat token is a fee on transfer tokenthen the line L313 would revert (since an amount less than fiattoken_amount is transferred).

**Recommendation**

Make sure fee on transfer token cases are handled appropriately or blacklist such tokens.

**Re-audit comment**

Acknowledged

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Gain |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-19-Gain.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

