---
# Core Classification
protocol: Blockbank
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55952
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-08-blockbank.md
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

Address lacks zero-check

### Overview

See description below for full details.

### Original Finding Content

**Description**

LGEWhitelisted.sol, line 61

Missing “require” statement for comparison “pairAddress” function parameter with zero
address. It is needed to prevent misleading transactions or a transaction with incorrect
arguments (e.g. because of frontend validation failure).

**Recommendation**:

Add “require” statement before executing function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Blockbank |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-08-blockbank.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

