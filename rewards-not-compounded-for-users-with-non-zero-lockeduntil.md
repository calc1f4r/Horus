---
# Core Classification
protocol: Starter
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35713
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-starter.md
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

Rewards Not Compounded For Users with Non-Zero lockedUntil

### Overview

See description below for full details.

### Original Finding Content

**Severity** - Informational

**Status** - Acknowledged

**Description**

The pool contract only rewards stakers with yield who staked without a lock period (for these stakers `liquidWeight` is being assigned , for users who have locked their stake for a duration there `liquidWeight` is 0) inside `_unstake` (L655-L656) . Though this may be a design choice it seems that stakers who actually staked for a duration and locked their stake don’t receive accrued yield.

**Recommendation**:

The design choice should be acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Starter |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-starter.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

