---
# Core Classification
protocol: Wallek
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35371
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
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

Unused variable.

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**

TestStake::reStake()::totalWithdrawn.
The local variable totalWithdrawn accumulates stake amounts but is not used anywhere else in the function. It may indicate incomplete contract logic in the production code and lead to unintended incidents.
Consequently, the same applies to 'previousAmount", which is redundant and only used for totalWithdrawn.

**Recommendation:**

Complete the contract logic OR remove the variable.
Post audit. Unused variable was removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Wallek |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

