---
# Core Classification
protocol: Wild Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61782
audit_firm: Kann
contest_link: none
source_link: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Wild Protocol.md
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

protocol_categories:
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Kann
---

## Vulnerability Title

[M-01] Bonding Curve Check  stepsize * numSteps May Not Match curveSupply

### Overview


The report states that there is a bug in a token launch process where the bonding curve parameters are not properly validated. This can lead to potential issues such as offering more tokens than allocated or part of the curve supply becoming unreachable. The team has responded that the bug has been fixed.

### Original Finding Content


## Severity

Medium

## Description

When launching a token with bonding curve parameters, there is no validation ensuring that stepsize * numSteps == curveSupply. If this is not aligned:

If stepsize * numSteps > curveSupply, the bonding curve will appear to offer more tokens than were actually allocated, leading to potential inconsistencies (e.g., using LP pool tokens to fulfill purchases).

If stepsize * numSteps < curveSupply, part of the curve supply will become unreachable via the bonding curve, and remain unused.

While this behavior may be intentional to allow flexible bonding curve shapes, without an explicit check or warning, it can lead to unintended launch behavior due to misconfiguration.


## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | Wild Protocol |
| Report Date | N/A |
| Finders | Kann |

### Source Links

- **Source**: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Wild Protocol.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

