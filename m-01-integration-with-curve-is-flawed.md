---
# Core Classification
protocol: Pino
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27251
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Pino.md
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
  - Pashov
---

## Vulnerability Title

[M-01] Integration with `Curve` is flawed

### Overview


This bug report concerns an issue with the `Curve` methods `deposit` and `withdraw`, which are hardcoding the number of underlying tokens in a Curve pool to be exactly two. This is incorrect, as some pools have three or more underlying tokens and with the current implementations users can't make proxy calls to them, which limits the functionality of the protocol.

The impact of this bug is low, as users won't lose funds but the protocol's contract might need new implementation and redeployment. The likelihood of it occurring is high, as users can't use a big part of Curve pools.

The recommendation is to change the methods in `Curve` so that they can work for different counts of underlying tokens in a pool, with proper validations.

### Original Finding Content

**Severity**

**Impact:**
Low, as users won't lose funds but the protocol's contract might need new implementation and redeployment

**Likelihood:**
High, as users can't use a big part of Curve pools

**Description**

Currently, the `Curve` methods `deposit` and `withdraw` are hardcoding the number of underlying tokens in a Curve pool to be exactly two. This is incorrect, as some pools have three or more underlying tokens and with the current implementations users can't make proxy calls to them, which limits the functionality of the protocol.

**Recommendations**

Change the methods in `Curve` so that they can work for different counts of underlying tokens in a pool, make sure to do this with a proper validations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Pino |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Pino.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

