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
solodit_id: 6928
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
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
  - hack3r-0m
  - Jay Jonah
  - Christoph Michel
  - Emanuele Ricci
---

## Vulnerability Title

Liquidating Morpho’s Aave position leads to state desynchronization

### Overview


This bug report concerns an issue with the PositionsManagerForAaveGettersSetters.sol code in Morpho. When a single position on Aave that encompasses all of Morpho’s individual user positions is liquidated, the user position state tracked in Morpho desynchronizes from the actual Aave position. This leads to issues when users try to withdraw their collateral or repay their debt from Morpho, and it's also possible to double-liquidate for a profit.

To illustrate this, consider a single borrower B1 on Morpho who supplies 1 ETH and borrows 2500 DAI. This creates a position on Aave for Morpho. If the ETH price crashes and the position becomes liquidatable, a liquidator can liquidate the position on Aave, earning the liquidation bonus. They can repay some debt and seize some collateral for profit. However, this repaid debt and removed collateral is not synced with Morpho; the user’s supply and debt balance remain 1 ETH and 2500 DAI. This means the same user on Morpho can be liquidated again because Morpho uses the exact same liquidation parameters as Aave.

The recommendation to prevent this issue is to send aTokens on behalf of Morpho and set it as collateral, and to run their own liquidation bots. No direct fixes have been implemented. This issue is of high risk and should be addressed as soon as possible.

### Original Finding Content

## Severity: High Risk

## Context
PositionsManagerForAaveGettersSetters.sol#L208-L219

## Description
Morpho has a single position on Aave that encompasses all of Morpho’s individual user positions that are on the pool. When this Aave Morpho position is liquidated, the user position state tracked in Morpho desynchronizes from the actual Aave position. This leads to issues when users try to withdraw their collateral or repay their debt from Morpho. It’s also possible to double-liquidate for a profit.

### Example
There’s a single borrower B1 on Morpho who is connected to the Aave pool.
- B1 supplies 1 ETH and borrows 2500 DAI. This creates a position on Aave for Morpho.
- The ETH price crashes and the position becomes liquidatable.
- A liquidator liquidates the position on Aave, earning the liquidation bonus. They repaid some debt and seized some collateral for profit.
- This repaid debt / removed collateral is not synced with Morpho. The user’s supply and debt balance remain 1 ETH and 2500 DAI. The same user on Morpho can be liquidated again because Morpho uses the exact same liquidation parameters as Aave.
- The Morpho liquidation call again repays debt on the Aave position and withdraws collateral with a second liquidation bonus.
- The state remains desynced.

## Recommendation
Liquidating the Morpho position should not break core functionality for Morpho users. Morpho: This issue can be prevented by sending, at the beginning at least, aTokens on behalf of Morpho and set it as collateral to prevent this issue. Also, we will run our own liquidation bots. We will not implement any "direct" fix inside the code.

## Spearbit
Acknowledged, no direct fixes have been implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

