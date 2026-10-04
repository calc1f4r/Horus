---
# Core Classification
protocol: Sentiment Update #3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6271
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/37
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-sentiment-judging/issues/26

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Bahurum
---

## Vulnerability Title

M-1: Tokens not owned by an account can be added as an asset to the account

### Overview


This bug report is about an issue found in the `RewardRouterController`, `RewardRouterV2Controller` and `DNGMXVaultController` functions. In the `canCall` function, a token address can be added to the list of assets of an account even if the account does not own the token. This does not pose any issues for the calculation of collateral, but it means that the list of assets of an account can contain tokens that the account does not actually hold. The bug was found through manual review and no particular recommendation was made.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-sentiment-judging/issues/26 

## Found by 
Bahurum

## Summary
In the controllers `RewardRouterController`, `RewardRouterV2Controller` and `DNGMXVaultController` the function `canCall` can return in `tokenIn` a token address that has actually not been received by the account. If the account did not have the token before, than the token is added to the asset list of the account even if the account does not hold the token at all.

## Vulnerability Detail

- in `RewardRouterController`: in `canCallCompound()`, `WETH` is added to `tokensIn` but no tokens are sent to the account as a result of the call to the Reward Router's function `compound()`
- in `RewardRouterV2Controller`: in `canCallRedeem()` the token redeemed is added to `tokensIn`, but the router's function `unstakeAndRedeemGlp()` allows to send the tokens to a 3rd party receiver instead of the caller. In such a case, nop tokens are sent to the account.
- in `DNGMXVaultController`: in `canWithdraw()` the token redeemed is added to `tokensIn`, but the DN GMX vault's functions `redeemToken()` and `withdrawToken()` allow to send the tokens to a 3rd party receiver instead of the caller. In such a case, nop tokens are sent to the account.

## Impact
There can be tokens in the list of assets of an account that the account doesn't actually hold. Note that this does not pose any issues for the calculation of collateral.

## Code Snippet
https://github.com/sherlock-audit/2023-01-sentiment/blob/main/controller-55/src/gmx/RewardRouterController.sol#L67

https://github.com/sherlock-audit/2023-01-sentiment/blob/main/controller-55/src/gmx/RewardRouterV2Controller.sol#L88

https://github.com/sherlock-audit/2023-01-sentiment/blob/main/controller-55/src/gmx/RewardRouterV2Controller.sol#L88

## Tool used

Manual Review

## Recommendation
No particular reccommendation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment Update #3 |
| Report Date | N/A |
| Finders | Bahurum |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-sentiment-judging/issues/26
- **Contest**: https://app.sherlock.xyz/audits/contests/37

### Keywords for Search

`vulnerability`

