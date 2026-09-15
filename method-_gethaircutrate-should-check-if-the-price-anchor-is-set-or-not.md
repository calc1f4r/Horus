---
# Core Classification
protocol: Wombat Exchange
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37544
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat Exchange.md
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

Method `_getHaircutRate` should check if the price anchor is set or not

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Description**

In Contract VolatilePool.sol, the method `_getHaircutrate(...)` calculates the volatility of `fromAsset` and `toAsset` if they are not price anchor.

Since `priceAnchor` is not set in the `initialize()` method, there is a possibility of it not being assigned and this will lead to volatility calculation even for `priceAnchor` asset if it is either `fromAsset` or `toAsset` which will lead to wrong haircut rate.

**Recommendation**: 

Ensure that the price anchor is set before `getHaircutrate` can be calculated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Wombat Exchange |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat Exchange.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

