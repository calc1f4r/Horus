---
# Core Classification
protocol: Magic Yearn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57536
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-17-Magic Yearn.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Liquidity pool can be set multiple times in MyShare.

### Overview


The bug report is about a function called "setLP" in a code called MyShare.sol. The code has a comment saying that a liquidity pool can only be set once, but the variable used to check this always stays false, which means the pool can be set multiple times. The recommendation is to change the variable to true after setting the pool. The issue has been resolved by checking for a different variable called "txnLiqPool" to make sure the pool is not set to a zero address.

### Original Finding Content

**Description**

MyShare.sol: function setLP(). In the comment section, it is declared that a liquidity pool can be set only once, and the "txnLiqPoolIsSet" variable is checked to be false to verify this. However, the stake of this variable doesn't change, meaning that it will always be equal to false and could be set more than once.

**Recommendation**

Assign true to "txnLiqPoolIsSet" after a liquidity pool is set.

**Re-audit comment**

Resolved.

Post-audit:

In order to validate that a pool can only be set once, the "txnLiqPool" storage variable is checked not to be zero address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Magic Yearn |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-17-Magic Yearn.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

