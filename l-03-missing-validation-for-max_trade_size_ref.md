---
# Core Classification
protocol: Ostium_2025-01-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61516
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ostium-security-review_2025-01-21.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-03] Missing validation for `MAX_TRADE_SIZE_REF`

### Overview

See description below for full details.

### Original Finding Content


The protocol defines `MAX_TRADE_SIZE_REF` as a constant but lacks validation checks when setting trade size references. This could lead to scenarios where trade size references exceed the intended maximum limit, potentially affecting price impact calculations.

```solidity
// Constant defined but not enforced
uint256 constant MAX_TRADE_SIZE_REF = 10000000e6; // 10M
```

Add validation check when setting trade size reference and validate the value returned from the chainlink report.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ostium_2025-01-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ostium-security-review_2025-01-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

