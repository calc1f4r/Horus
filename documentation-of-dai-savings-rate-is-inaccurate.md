---
# Core Classification
protocol: MCD Core Smart Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17062
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf
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
finders_count: 4
finders:
  - JP Smith
  - Sam Moelius
  - David Pokora
  - Rajeev Gopalakrishna
---

## Vulnerability Title

Documentation of Dai Savings Rate is inaccurate

### Overview

See description below for full details.

### Original Finding Content

## Type: Denial of Service

**Target:** flop.sol, vat.sol, vow.sol

## Difficulty: Low

### Description
The Dai Savings Rate (DSR) does not constrict Dai supply. However, both the whitepaper and the MakerDAO Medium post (which currently appear first in an online search for “Dai Savings Rate”) state that it does. This could lead Dai users to misunderstand the DSR’s function.

### Recommendation
Update both the Medium post and the whitepaper to clarify the function of the DSR. Regularly review all public documentation for accuracy as Dai functionality is updated.

© 2019 Trail of Bits  
Multi-Collateral Dai Security Review | 30

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | MCD Core Smart Contracts |
| Report Date | N/A |
| Finders | JP Smith, Sam Moelius, David Pokora, Rajeev Gopalakrishna |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/mc-dai.pdf

### Keywords for Search

`vulnerability`

