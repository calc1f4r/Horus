---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7298
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - don't_update_state

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

If a collateral's liquidation auction on Seaport ends without a winning bid, the call to liquidatorNFTClaim does not clear the related data on LienToken 's side and also for payee s that are public vaults

### Overview


The bug report describes an issue with FTClaim not clearing the related data on LienToken's side and payees that are public vaults. This issue is considered to be of high risk and is located in the CollateralToken.sol#L107. When a liquidation auction ends without being fulfilled/matched on Seaport and the currentliquidator calls into liquidatorNFTClaim, the storage data (s.collateralStateHash, s.auctionData, s.lienMeta) on the LienToken side does not get reset/cleared. This means that s.collateralStateHash[collateralId] stays equal to bytes32("ACTIVE_AUCTION"), s.auctionData[collateralId] will have the past auction data, and s.lienMeta[collateralId].atLiquidation will be true. This will cause future calls to commitToLiens by holders of the same collateral to revert.

The recommendation is to make sure to clear related storage data on LienToken's side and payees that are public vaults when liquidatorNFTClaim is called.

### Original Finding Content

## High Risk Vulnerability Report

## Severity
**High Risk**

## Context
`CollateralToken.sol#L107`

## Description
If/when a liquidation auction ends without being fulfilled/matched on Seaport, and afterward when the current liquidator calls into `liquidatorNFTClaim`, the storage data (`s.collateralStateHash`, `s.auctionData`, `s.lienMeta`) on the LienToken side do not get reset/cleared. Additionally, the lien token does not get burnt. This results in the following issues:

- `s.collateralStateHash[collateralId]` remains equal to `bytes32("ACTIVE_AUCTION")`.
- `s.auctionData[collateralId]` retains the past auction data.
- `s.lienMeta[collateralId].atLiquidation` will be `true`.

As a consequence, future calls to `commitToLiens` by holders of the same collateral will revert.

## Recommendation
Ensure to clear related storage data on the LienToken's side and on payees that are public vaults when `liquidatorNFTClaim` is called.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Don't update state`

