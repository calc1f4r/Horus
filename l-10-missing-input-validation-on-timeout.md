---
# Core Classification
protocol: Reality Cards
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 317
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-06-reality-cards-contest
source_link: https://code4rena.com/reports/2021-06-realitycards
github_link: https://github.com/code-423n4/2021-06-realitycards-findings/issues/74

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
  - dexes
  - cdp
  - cross_chain
  - synthetics
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xRajeev
---

## Vulnerability Title

[L-10] Missing input validation on timeout

### Overview

See description below for full details.

### Original Finding Content

## Handle

0xRajeev


## Vulnerability details

## Impact

Factory constructor sets timeout to 86400 seconds but setter setTimeout() has no threshold checks for a min timeout value. If this is accidentally set to 0 or lower-than-safe value then there is no dispute window and users lose confidence in market.


## Proof of Concept

https://github.com/code-423n4/2021-06-realitycards/blob/86a816abb058cc0ed9b6f5c4a8ad146f22b8034c/contracts/RCFactory.sol#L137

https://github.com/code-423n4/2021-06-realitycards/blob/86a816abb058cc0ed9b6f5c4a8ad146f22b8034c/contracts/RCFactory.sol#L299-L303

## Tools Used

Manual Analysis

## Recommended Mitigation Steps

Add input validation for threshold checks on both low and high ends.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Reality Cards |
| Report Date | N/A |
| Finders | 0xRajeev |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-realitycards
- **GitHub**: https://github.com/code-423n4/2021-06-realitycards-findings/issues/74
- **Contest**: https://code4rena.com/contests/2021-06-reality-cards-contest

### Keywords for Search

`vulnerability`

