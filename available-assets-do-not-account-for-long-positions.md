---
# Core Classification
protocol: Panoptic Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33821
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/panoptic-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Available Assets Do Not Account For Long Positions

### Overview


The bug report discusses an issue with the Panoptic Pool and AMM pool in a trading platform. When a short position is created, tokens are moved from the Panoptic Pool to the AMM pool, reducing the balance of the pool and preventing withdrawals. When a long position is created, tokens are moved back to the Panoptic Pool, increasing the balance and allowing for withdrawals. However, with leverage, there may not be enough liquidity in the Panoptic Pool for the long position to be exercised, causing it to be disabled until more liquidity is provided. The report suggests accounting for the available assets used by both option buyers and sellers. The Panoptic team has acknowledged the issue but has not yet fixed it, stating that it is intended for flexibility and user experience. However, users have options to free up funds in case of a liquidity crunch, such as depositing more collateral, creating more long positions, closing short positions, or waiting for other sellers to close positions.

### Original Finding Content

When a short position is minted, tokens are moved from the Panoptic Pool to the AMM pool thus reducing the balance of the pool. This amount is reflected in the reduction of the available assets, thus preventing withdrawals.


When a corresponding long position is minted, tokens are moved from the AMM pool to the Panoptic Pool, increasing the balance of the pool. The same amount is then added back to the available assets, allowing any LPs to withdraw their assets when the long position is still active.


With leverage, it is possible that after LP withdrawals, there may not be sufficient liquidity in the Panoptic Pool to transfer to the AMM pool when exercising the long position, thus disabling long positions from closing until further liquidity provision.


Consider accounting for the available assets used by both option buyers and sellers.


***Update:** Acknowledged, not fixed. The Panoptic team stated:*



> This is intended. Allowing removed long liquidity to be reused for short positions and withdrawals greatly enhances flexibility and user experience in most situations. It is possible for the pool to lack the funds necessary to exercise a long position in certain unusual circumstances, but users who wish to exercise their options have multiple options to free up funds in the event of a liquidity crunch. They can deposit more collateral, mint more long positons, close their short positions, or wait for other sellers to close positions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Panoptic Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/panoptic-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

