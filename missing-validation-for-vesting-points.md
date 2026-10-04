---
# Core Classification
protocol: Zap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35424
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-11-Zap.md
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

Missing validation for vesting points

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**

In Contract Vesting.sol, the method `initialize(...)` sets the vesting points as follows:
`(vestingPoints, ) = ascendingSort(_vestingPoints);`

Here, vesting points are ordered as per the timestamp value but do not check if the time values are in the past.

`Claim ()` can be done immediately if any past value is set.

**Recommendation**: 

Validate that both points’ timestamp value is >= block.timestamp.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-11-Zap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

