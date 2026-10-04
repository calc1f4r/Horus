---
# Core Classification
protocol: Newwit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20999
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2022-10-19-Newwit.md
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
  - AuditOne
---

## Vulnerability Title

Validation missing on `_initialSupply`

### Overview

See description below for full details.

### Original Finding Content

**Description:**

1. Observe that in the `initialize`function `_initialSupply` is not checked to be smaller than or equal to `_maxSupply`.
2. Observe that admin can mistakenly set `_initialSupply`greater than `_maxSupply`which is incorrect behavior.

**Recommendations:** 

Add a check `_initialSupply <= _maxSupply`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Newwit |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2022-10-19-Newwit.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

