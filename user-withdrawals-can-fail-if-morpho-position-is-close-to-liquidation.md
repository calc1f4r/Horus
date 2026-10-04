---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6903
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - dos
  - business_logic

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Christoph Michel
  - Emanuele Ricci
  - hack3r-0m
  - Jay Jonah
---

## Vulnerability Title

User withdrawals can fail if Morpho position is close to liquidation

### Overview


This bug report describes a problem with the ExitPositionsManager.sol code. When a P2P supplier attempts to withdraw funds from Morpho, the last step of the withdrawal algorithm tries to borrow an amount from the pool. If the Morpho position on Aave's debt/collateral value is higher than the market's max LTV ratio but lower than the market's liquidation threshold, the borrow will fail and the position can also not be liquidated, so the withdrawal could fail.

The recommendation is to consider ways to mitigate the impact of this problem. Morpho will first launch on Compound, where there is only Collateral Factor, so they will not focus now on this particular issue. Spearbit has acknowledged the bug report.

### Original Finding Content

## Severity: Medium Risk

## Context
ExitPositionsManager.sol#L468

## Description
When trying to withdraw funds from Morpho as a P2P supplier, the last step of the withdrawal algorithm borrows an amount from the pool ("hard withdraw"). If the Morpho position on Aave's debt/collateral value is higher than the market's max LTV ratio but lower than the market's liquidation threshold, the borrow will fail, and the position can also not be liquidated. The withdrawals could fail.

## Recommendation
This seems hard to solve in the current system as it relies on the "hard withdraws" to always ensure enough liquidity for P2P suppliers. Consider ways to mitigate the impact of this problem. 

## Morpho
Since Morpho will first launch on Compound (where there is only Collateral Factor), we will not focus now on this particular issue.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Christoph Michel, Emanuele Ricci, hack3r-0m, Jay Jonah |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf

### Keywords for Search

`DOS, Business Logic`

