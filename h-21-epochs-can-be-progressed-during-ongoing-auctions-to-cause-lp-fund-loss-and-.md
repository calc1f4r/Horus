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
solodit_id: 3659
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/175

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

H-21: Epochs can be progressed during ongoing auctions to cause LP fund loss and collateral lockup

### Overview


This bug report is about the `currentEpoch` being progressed while having an ongoing auction which can mess up the liquidation logic to potentially cause LP fund loss and collateral lockup. The issue is related to the `LiquidationAccountant.claim()` function which is only callable if `finalAuctionEnd` is set to 0 or the  `block.timestamp` is greater than `finalAuctionEnd` (i.e. auction has ended). The `finalAuctionEnd` is set within the `LiquidationAccountant.handleNewLiquidation` function, which is called from the `AstariaRouter.liquidate` function. However, instead of providing a timestamp of the auction end, a value of `2 days + 1 days` is given. This does not achieve the intended constraint on checking for the end of the auction because it uses a fixed duration instead of a timestamp. 

The impact of this bug is that epochs can be progressed during ongoing auctions to completely mess up the liquidation logic to potentially cause LP fund loss and collateral lockup. The code snippet related to this bug can be found in the following files: 

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LiquidationAccountant.sol#L67
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/PublicVault.sol#L244-L248
3. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L409

The bug was found manually by 0xRajeev. The recommendation to fix this bug is to revisit the logic to use an appropriate timestamp instead of a fixed duration.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/175 

## Found by 
0xRajeev

## Summary

The `currentEpoch` can be progressed while having an ongoing auction which will completely mess up the liquidation logic to potentially cause LP fund loss and collateral lockup.

## Vulnerability Detail

The `LiquidationAccountant.claim()` function is only callable if `finalAuctionEnd` is set to 0 or the  `block.timestamp` is greater than `finalAuctionEnd` (i.e. auction has ended). Furthermore, `PublicVault.processEpoch` should only be callable if there is *no* ongoing auction if a liquidation accountant is deployed in the current epoch.

`finalAuctionEnd` is set within the `LiquidationAccountant.handleNewLiquidation` function, which is called from the `AstariaRouter.liquidate` function. However, instead of providing a timestamp of the auction end, a value of `2 days + 1 days` is given because `COLLATERAL_TOKEN.auctionWindow()` returns `2 days`.

This does not achieve the intended constraint on checking for the end of the auction because it uses a fixed duration instead of a timestamp.

## Impact

Epochs can be progressed during ongoing auctions to completely mess up the liquidation logic to potentially cause LP fund loss and collateral lockup.
 
## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LiquidationAccountant.sol#L67
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/PublicVault.sol#L244-L248
3. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L409

## Tool used

Manual Review

## Recommendation

Revisit the logic to use an appropriate timestamp instead of a fixed duration.

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
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/175
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

