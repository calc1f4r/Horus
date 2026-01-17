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
solodit_id: 3643
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/204

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
finders_count: 5
finders:
  - Jeiwan
  - bin2chen
  - 0xRajeev
  - HonorLt
  - rvierdiiev
---

## Vulnerability Title

H-5: `commitToLiens` always reverts

### Overview


A bug report has been issued related to the function `commitToLiens()` in the protocol AstariaRouter. This function always reverts when attempting to call `_returnCollateral()`, preventing borrowers from depositing collateral and requesting loans. This is due to the NFT being transferred to `COLLATERAL_TOKEN` in `_transferAndDepositAsset()` which mints the token with `collateralId` to borrower (`from` address) and not the `operator_` (i.e. `AstariaRouter`). The impact of this bug is that the core NFT lending functionality of the protocol fails to bootstrap. The code snippet related to this bug can be found at the source link. The bug was found by HonorLt, 0xRajeev, rvierdiiev, bin2chen, Jeiwan. The recommended solution is to remove the call to `_returnCollateral()` in `commitToLiens()`. The issue was escalated for 2 USDC and accepted by Evert0x. The contestants' payouts and scores will be updated according to the changes made on this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/204 

## Found by 
HonorLt, 0xRajeev, rvierdiiev, bin2chen, Jeiwan

## Summary

The function `commitToLiens()` always reverts at the call to `_returnCollateral()` which prevents borrowers from depositing collateral and requesting loans in the protocol.

## Vulnerability Detail

The collateral token with `collateralId` is already minted directly to the caller (i.e. borrower) in `commitToLiens()` at the call to `_transferAndDepositAsset()` function. That's because while executing `_transferAndDepositAsset` the NFT is transferred to `COLLATERAL_TOKEN` whose `onERC721Received` mints the token with `collateralId` to borrower (`from` address) and not the `operator_` (i.e. `AstariaRouter`) because `operator_ != from_`.

However, the call to `_returnCollateral()` in `commitToLiens()` incorrectly assumes that this has been minted to the operator and attempts to transfer it to the borrower which will revert because the `collateralId` is not owned by  `AstariaRouter` as it has already been transferred/minted to the borrower.

## Impact

The function `commitToLiens()` always reverts, preventing borrowers from depositing collateral and requesting loans in the protocol, thereby failing to bootstrap its core NFT lending functionality.

## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L244-L274
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L578-L587
3. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/CollateralToken.sol#L282-L284
4. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L589-L591

## Tool used

Manual Review

## Recommendation
Remove the call to `_returnCollateral()` in `commitToLiens()`.

## Discussion

**secureum**

Escalate for 2 USDC.

Given the impact of failing to bootstrap core protocol functionality as described above, we still think this is of high-severity (not Medium as judged) unlike a DoS that affects only a minority of protocol flows. Also, this is not a dup of #195.

cc @berndartmueller @lucyoa

**sherlock-admin**

 > Escalate for 2 USDC.
> 
> Given the impact of failing to bootstrap core protocol functionality as described above, we still think this is of high-severity (not Medium as judged) unlike a DoS that affects only a minority of protocol flows. Also, this is not a dup of #195.
> 
> cc @berndartmueller @lucyoa

You've created a valid escalation for 2 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Evert0x**

Escalation accepted

**sherlock-admin**

> Escalation accepted

This issue's escalations have been accepted!

Contestants' payouts and scores will be updated according to the changes made on this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Jeiwan, bin2chen, 0xRajeev, HonorLt, rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/204
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

