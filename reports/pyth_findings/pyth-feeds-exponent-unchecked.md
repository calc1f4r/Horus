---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35181
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Pyth Feeds Exponent Unchecked

### Overview

See description below for full details.

### Original Finding Content

Within the `OracleRouter` contract, [a subtraction of Pyth's `expo` value](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/OracleRouter.sol#L166) is performed inside the `_getPythPrice` function. If the `expo` from Pyth's return exceed 18 or are less than \-18, then this will fail non\-descriptively.


Consider implementing an informative error message which is returned when `abs(priceData.expo) > 18`. Alternatively, consider adding logic to format prices with exponents outside of `[-18,18]`.


***Update:** Resolved in [pull request \#92](https://github.com/radiant-capital/riz/pull/92) at commit [3f0fdc0](https://github.com/radiant-capital/riz/pull/92/commits/3f0fdc03799bf1d3d417c6b54a4c82460e0d1f7c).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

