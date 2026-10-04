---
# Core Classification
protocol: Tren
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45821
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-Tren.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

Potential Precision Loss Due to Division Before Multiplication

### Overview


A bug was found in the SingleLiquidityProvider.sol contract, where the calculateEmissionPerSecond function performs division before multiplication. This can result in precision loss and incorrect emission values, especially with low apy values. The bug has been resolved, but it is recommended to revisit the calculations and change the operation orders to avoid rounding errors in the future. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

The calculateEmissionPerSecond function in SingleLiquidityProvider.sol performs division before multiplication in the line ((apy / 100) * investmentAmount) / timePeriod, which may lead to precision loss. When working with integer division, dividing apy by 100 first can round the result down if apy is not a multiple of 100. This can cause an incorrect and lower emission value, especially with low apy values.
In cases with small apy values or when precision is critical, this approach could result in miscalculations affecting user rewards or emissions.

**Recommendation**: 

Consider revisiting the calculations in the contract and change the operation orders to multiply before dividing to minimize rounding errors.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tren |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-Tren.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

