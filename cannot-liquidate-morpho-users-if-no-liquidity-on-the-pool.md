---
# Core Classification
protocol: Morpho
chain: everychain
category: dos
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6909
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
  - liquidation
  - dos

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
  - EBaizel
  - JayJonah8
  - Christoph Michel
  - Datapunk
  - Emanuele Ricci
---

## Vulnerability Title

Cannot liquidate Morpho users if no liquidity on the pool

### Overview


This bug report is about a medium risk issue with the ExitPositionsManager.sol in aave-v2. The issue is that if there is no liquidity in the collateral asset pool, the liquidation will fail and Morpho could incur bad debt as they cannot liquidate the user. The liquidation mechanisms of Aave and Compound allow the liquidator to seize the debtorsTokens/cTokens, but this would require significant capital as collateral in most cases.

The recommendation is to add a feature where liquidators can seize aTokens/cTokens instead of withdrawing underlying tokens from the pool. This would only work with onPool balances but not with inP2P balances as these don't mint aTokens/cTokens. Morpho decided not to implement this recommendation on the current codebase, and this was acknowledged by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
`aave-v2/ExitPositionsManager.sol#L277`

## Description
Morpho implements liquidations by repaying the borrowed asset and then withdrawing the collateral asset from the underlying protocol (Aave / Compound). If there is no liquidity in the collateral asset pool, the liquidation will fail. Morpho could incur bad debt as they cannot liquidate the user. 

The liquidation mechanisms of Aave and Compound work differently: they allow the liquidator to seize the `debtorsTokens/cTokens`, which can later be withdrawn for the underlying token once there is enough liquidity in the pool. 

Technically, an attacker could even force no liquidity on the pool by frontrunning liquidations by borrowing the entire pool amount, preventing them from being liquidated on Morpho. However, this would require significant capital as collateral in most cases.

## Recommendation
Think about adding a similar feature where liquidators can seize `aTokens/cTokens` instead of withdrawing underlying tokens from the pool. The `aTokens/cTokens` of all pool users are already in the Morpho contract and thus in Morpho's control. Note that this would only work with onPool balances but not with inP2P balances, as these don't mint `aTokens/cTokens`.

## Morpho
As it requires large changes in the liquidation process, we decided not to implement this recommendation on the current codebase.

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
| Finders | EBaizel, JayJonah8, Christoph Michel, Datapunk, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf

### Keywords for Search

`Liquidation, DOS`

