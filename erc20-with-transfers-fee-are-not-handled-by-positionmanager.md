---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6908
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
  - fee_on_transfer

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

ERC20 with transfer's fee are not handled by *PositionManager

### Overview


This bug report is about the current implementation of PositionsManager.sol, EntryPositionsManager.sol, and ExitPositionsManager.sol not taking into consideration ERC20 tokens that could have fees attached to their transfer events. Morpho is taking for granted that the amount specified by the user will be the amount transferred to the contract's balance, while in reality the contract will receive less. The recommendation is to update the PositionManager logic to track the real amount of token that has been sent by the user after the transfer. However, given the small likelihood for USDC and USDT to turn on fees, Morpho has decided not to implement the recommendations. The checklist has been updated and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
- PositionsManager.sol
- EntryPositionsManager.sol
- ExitPositionsManager.sol

## Description
Some ERC20 tokens could have fees attached to the transfer event, while others could enable them in the future (see USDT, USDC). The current implementation of both PositionManager (for Aave and Compound) is not taking into consideration these types of ERC20 tokens. While Aave seems not to take into consideration this behavior (see LendingPool.sol), Compound, on the other hand, is explicitly handling it inside the `doTransferIn` function. 

Morpho is taking for granted that the amount specified by the user will be the amount transferred to the contract's balance, while in reality, the contract will receive less. In `InsupplyLogic`, for example, Morpho will account for the user's p2p/pool balance for the full amount but will repay/supply to the pool less than the amount accounted for.

## Recommendation
Consider updating the `PositionManager` logic to track the real amount of token that has been sent by the user after the transfer (difference in before and after balance), but also the amount of tokens that have been supplied/borrowed/withdrawn/... given that Morpho itself is doing a second transfer/transferFrom to/from the Aave/Compound protocol.

## Morpho
We updated the asset listing checklist. However, given the small likelihood for USDC and USDT to turn on fees, we decided not to implement the recommendations.

## Spearbit
Verified the checklist, and acknowledged that the recommendations will not be implemented.

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

`Fee On Transfer`

