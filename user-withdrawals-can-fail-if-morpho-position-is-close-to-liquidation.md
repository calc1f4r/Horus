---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6939
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
---

## Vulnerability Title

User withdrawals can fail if Morpho position is close to liquidation

### Overview


This bug report is about a problem with a withdrawal algorithm in PositionsManagerForAaveLogic.sol. When trying to withdraw funds from Morpho as a P2P supplier, the last step of the algorithm borrows an amount from the pool ("hard withdraw"). If Morpho’s position on Aave’s debt / collateral value is higher than the market’s maximum LTV ratio but lower than the market’s liquidation threshold, the borrow will fail and the position cannot be liquidated. In this case, withdrawals may fail. 

The recommendation is to consider ways to mitigate the impact of this problem. Morpho will first launch on Compound (where there is only Collateral Factor) and will not focus now on this particular issue. Spearbit has acknowledged the report. 

In summary, this bug report is about a problem with a withdrawal algorithm in PositionsManagerForAaveLogic.sol that can lead to failed withdrawals if Morpho’s position on Aave’s debt / collateral value is higher than the market’s maximum LTV ratio but lower than the market’s liquidation threshold. The recommendation is to consider ways to mitigate the impact of this problem, although Morpho will not focus on this issue at the moment.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
`PositionsManagerForAaveLogic.sol#L246`

## Description
When trying to withdraw funds from Morpho as a P2P supplier, the last step of the withdrawal algorithm borrows an amount from the pool ("hard withdraw"). If Morpho’s position on Aave’s debt/collateral value is higher than the market’s maximum LTV (Loan-To-Value) ratio but lower than the market’s liquidation threshold, the borrow will fail, and the position cannot be liquidated. Therefore, withdrawals could fail.

## Recommendation
This seems hard to solve in the current system as it relies on "hard withdraws" to always ensure enough liquidity for P2P suppliers. Consider ways to mitigate the impact of this problem. 

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
| Finders | N/A |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

