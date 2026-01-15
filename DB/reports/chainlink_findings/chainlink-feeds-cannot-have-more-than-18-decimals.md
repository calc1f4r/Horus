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
solodit_id: 35179
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

Chainlink Feeds Cannot Have More Than 18 Decimals

### Overview

See description below for full details.

### Original Finding Content

Within `OracleRouter`, [a subtraction of chainlink's decimals](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/OracleRouter.sol#L151) is performed inside `_getChainlinkPrice`. If the decimals from the chainlink aggregator exceed `18`, then this operation will fail non\-descriptively.


Consider implementing an informative error message which is returned when the decimals exceed `18`. Alternatively, consider adding logic to format prices with greater than `18` decimals.


***Update:** Acknowledged, not resolved. The Radiant team stated:*



> *Acknowledged. We find this scenario to be very unlikely.*

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

