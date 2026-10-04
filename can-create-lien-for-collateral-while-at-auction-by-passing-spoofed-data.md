---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7296
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
  - validation

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

Can create lien for collateral while at auction by passing spoofed data

### Overview


This bug report is about the createLien function in the LienToken.sol code. The function checks that the collateral isn't currently at auction before giving a lien. However, collateralId is passed in multiple places in the params: both in params directly and in params.encumber.lien. The params.encumber.lien.collateralId is used everywhere else, but the check is performed on params.collateralId. This means that it is possible to set the params.encumber.lien.collateralId to a collateral that is at auction, while using the params.collateralId which is not at auction, thus allowing the validation to pass. 

The recommended fix is to update the code to use the lien.collateralId everywhere instead of encumber.collateralId. This would remove the collateralId parameter entirely from the encumber call, and the issue is resolved with the PR 214.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
**File:** LienToken.sol  
**Lines:** 368-372

## Description
In the `createLien` function, we check that the collateral isn't currently at auction before giving a lien with the following check:

```solidity
if (
    s.collateralStateHash[params.collateralId] == bytes32("ACTIVE_AUCTION")
) {
    revert InvalidState(InvalidStates.COLLATERAL_AUCTION);
}
```

However, `collateralId` is passed in multiple places in the `params`: both in `params` directly and in `params.encumber.lien`. 

The `params.encumber.lien.collateralId` is used everywhere else, and is the final value that is used. But the check is performed on `params.collateralId`.

As a result, we can set the following:
- `params.encumber.lien.collateralId`: collateral that is at auction.
- `params.collateralId`: collateral not at auction.

This will allow us to pass this validation while using the collateral at auction for the lien.

## Recommendation
The check should be updated to use `params.encumber.lien.collateralId` instead:

```solidity
if (
    s.collateralStateHash[params.encumber.lien.collateralId] == bytes32("ACTIVE_AUCTION")
) {
    revert InvalidState(InvalidStates.COLLATERAL_AUCTION);
}
```

Additionally, we can remove `collateralId` entirely from the encumber call, as it's inside lien. The fix is to update to use `lien.collateralId` everywhere instead of `encumber.collateralId`.

## Team Consensus
**Astaria:** We can remove `collateralId` entirely from the encumber call as it's inside lien. The fix is to update to use the `lien.collateralId` everywhere instead of `encumber.collateralId`.  
**Spearbit:** Agreed, that seems like the best fix and gets rid of an unneeded parameter. Confirmed that the following PR 214 resolves the issue.

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

`Validation`

