---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21858
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Saw-Mon and Natalie
  - Jonah1005
  - Blockdev
---

## Vulnerability Title

Several functions in AstariaRouter can be made non-payable

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
- `AstariaRouter.sol#L118-L173`
- `AstariaRouter.sol#L202`

## Description
Following functions in `AstariaRouter` are payable when they should never be sent the native token:
- `mint()`
- `deposit()`
- `withdraw()`
- `redeem()`
- `pullToken()`

## Recommendation
Remove the payable keyword for the highlighted functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Jonah1005, Blockdev |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf

### Keywords for Search

`vulnerability`

