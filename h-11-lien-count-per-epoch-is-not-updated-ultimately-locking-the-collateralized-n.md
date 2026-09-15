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
solodit_id: 3649
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/194

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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
finders_count: 1
finders:
  - 0xRajeev
---

## Vulnerability Title

H-11: Lien count per epoch is not updated ultimately locking the collateralized NFT

### Overview


This bug report was found by 0xRajeev and it concerns the lien count per epoch not being updated in the PublicVault contract. This issue causes payments to the lien and liquidation of the lien to revert, ultimately locking the collateralized NFT. 

When a lien is bought out, the lien start is set to the current block.timestamp and the duration to the newly provided duration. If the borrower now wants to make a payment to this lien, the `LienToken._payment` function will evaluate the lien's current epoch and will use a different epoch as when the lien was initially created. The attempt to then call `IPublicVault(lienOwner).decreaseEpochLienCount` will fail, as the lien count for the new epoch has not been increased yet.

The impact of this bug is that after a lien buyout, payments to the lien and liquidating the lien will revert, which will ultimately lock the collateralized NFT. This will prevent the borrower from making payments towards the previously bought lien that aligns to the current epoch, which will force a liquidation on exceeding lien duration. This could lock the borrower's collateral in the protocol.

The recommended solution is to increment `liensOpenForEpoch` when a lien is bought with a duration spilling into an epoch higher than the current one.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/194 

## Found by 
0xRajeev

## Summary

The lien count per epoch is not updated, causing payments to the lien and liquidation of the lien to revert.

## Vulnerability Detail

The PublicVault contract keeps track of open liens per epoch to prevent starting a new epoch with open liens. The lien count for a given epoch is decreased whenever a lien is fully paid back (either through a regular payment or a liquidation payment). However, if a lien is bought out, the lien start will be set to the current `block.timestamp` and the duration to the newly provided duration.

If the borrower now wants to make a payment to this lien, the `LienToken._payment` function will evaluate the lien's current epoch and will use a different epoch as when the lien was initially created. The attempt to then call `IPublicVault(lienOwner).decreaseEpochLienCount` will fail, as the lien count for the new epoch has not been increased yet. The same will happen for liquidations.

## Impact

After a lien buyout, payments to the lien and liquidating the lien will revert, which will ultimately lock the collateralized NFT.

This will certainly prevent the borrower from making payments towards that future-epoch lien in the current epoch because `decreaseEpochLienCount()` will revert. However, even after the epoch progresses to the next one via `processEpoch()`, the `liensOpenForEpoch` for the new epoch still does not account for the previously bought out lien aligned to this new epoch because `liensOpenForEpoch` is only updated in two places:
    1.  `_increaseOpenLiens()` which is not called by anyone 
    2. `_afterCommitToLien()` <- `commitToLien()` <-- <-- `commitToLiens()` which happens only for new lien commitments

This will prevent the borrower from making payments towards the previously bought lien that aligns to the current epoch, which will force a liquidation on exceeding lien duration. Depending on when the liquidation can be triggered, if this condition is satisfied `PublicVault(owner).timeToEpochEnd() <= COLLATERAL_TOKEN.auctionWindow()` then `decreaseEpochLienCount()` will revert to prevent auctioning and lock the borrower's collateral in the protocol.

## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/PublicVault.sol#L259-L262
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L634-L636
3. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L153
4. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L399

## Tool used

Manual Review

## Recommendation

`liensOpenForEpoch` should be incremented when a lien is bought with a duration spilling into an epoch higher than the current one.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | 0xRajeev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/194
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

