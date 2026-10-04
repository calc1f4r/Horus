---
# Core Classification
protocol: Balmy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46441
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/d365c977-e13a-41e2-84e3-67083ecbc362
source_link: https://cdn.cantina.xyz/reports/antina_balmy_november2024.pdf
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
finders_count: 2
finders:
  - Blockdev
  - ladboy233
---

## Vulnerability Title

Protocol reported: liquidity mining layer doesn 't increase the length of the balanceChanges array during special Withdrawal 

### Overview


This bug report is about a problem with the liquidity mining layer not properly increasing the length of the balanceChanges array during a special withdrawal. This can cause issues with the earn vault accounting. The bug has been fixed in PR 100.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
During a special withdrawal, the liquidity mining layer doesn't increase the length of the `balanceChanges` array properly. 

Let's see an example:
- The connector supports only token USDC.
- The liquidity mining layer adds OP as a reward token.
- The liquidity mining layer added OP in almost all functions:
  - `allTokens`
  - `withdraw`

However, we aren't modifying the length in `balanceChanges` when `specialWithdraw` is called. In our example, it would have a length of 1, while `allTokens` would have a length of 2, which breaks the earn vault accounting.

## Balmy
Fixed in PR 100.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Balmy |
| Report Date | N/A |
| Finders | Blockdev, ladboy233 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/antina_balmy_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/d365c977-e13a-41e2-84e3-67083ecbc362

### Keywords for Search

`vulnerability`

