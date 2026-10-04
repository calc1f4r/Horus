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
solodit_id: 61781
audit_firm: Kann
contest_link: none
source_link: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Wild Protocol.md
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

protocol_categories:
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Kann
---

## Vulnerability Title

[H-01] LP Fees Unclaimable via launchV4Pool()

### Overview


The bug report describes an issue with the launchV4Pool() function, which is used to create custom pools and graduate tokens. The problem is that this function does not call another function called setTokenParams(), which is necessary for configuring the LP locker and allowing fee claiming. This means that fees earned from the pool cannot be claimed, making the fee distribution logic useless for tokens created with launchV4Pool(). The team has responded that the issue has been fixed.

### Original Finding Content


## Severity

High

## Description

The function launchV4Pool() allows custom pool creation and token graduation (with manually set ticks and spacing). However, it does not call lpLocker.setTokenParams(), which is required to configure the LP locker for fee claiming.

Without calling setTokenParams(), fees earned from the pool become unclaimable, rendering the fee distribution logic non-functional for tokens launched via launchV4Pool().

In contrast, the graduateToken() function does invoke lpLocker.setTokenParams(), meaning fee claiming only works when using that path. This makes the launchV4Pool() function incomplete and effectively useless for real-world deployments where fees matter.


## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

