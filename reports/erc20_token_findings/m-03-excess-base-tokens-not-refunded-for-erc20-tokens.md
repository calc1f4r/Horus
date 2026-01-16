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
solodit_id: 61784
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

[M-03] Excess Base Tokens Not Refunded for ERC20 tokens

### Overview


The bug report describes an issue where users are not receiving a refund for any excess tokens they send when purchasing tokens using an ERC20 base token. This results in a loss of funds for users. The severity of this bug is medium. The team has responded that the issue has been fixed.

### Original Finding Content


## Severity

Medium

## Description

When a user purchases tokens using an ERC20 base token, the function _getBuyQuoteAndFees() correctly calculates the actual amount used (amountInUsed) and the associated fees. However, if the user sends more than amountInUsed, the excess tokens are not refunded.

In contrast, when using ETH as the base token, any overpayment is explicitly refunded. This inconsistent behavior creates a silent loss of funds for users interacting via ERC20 tokens.

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

