---
# Core Classification
protocol: Sentiment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3359
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1
source_link: none
github_link: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/033-M

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
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - csanuragjain
  - Czar102
  - panprog
  - PwnPatrol
  - rbserver
---

## Vulnerability Title

M-3: AccountManager: Liquidations not possible when transfer fails

### Overview


This bug report is about the issue M-3 of AccountManager in the sentiment judging project. It was found by panprog, csanuragjain, Czar102, carrot, PwnPatrol, Lambda, kirk-baird, berndartmueller, rbserver, Chom and __141345__. The issue is that when the transfer of one asset fails, liquidations become impossible. This could be caused by blocked addresses, zero balance, paused tokens or upgradeable tokens that changed the implementation. This could be triggered by the user in certain conditions to avoid liquidations. The code snippets related to this issue can be found at AccountManager.sol and Account.sol. The sentiment team fixed the issue as recommended and the lead senior Watson confirmed the fix.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/033-M 
## Found by 
panprog, csanuragjain, Czar102, carrot, PwnPatrol, Lambda, kirk-baird, berndartmueller, rbserver, Chom, \_\_141345\_\_

## Summary
When the transfer of one asset fails, liquidations become impossible.

## Vulnerability Detail
`_liquidate` calls `sweepTo`, which iterates over all assets. When one of those transfers fails, the whole liquidation process therefore fails. There are multiple reasons why a transfer could fail:
1.) Blocked addresses (e.g., USDC)
2.) The balance of the asset is 0, but it is still listed under asset. This can be for instance triggered by performing a 0 value Uniswap swap, in which case it is still added to `tokensIn`. Another way to trigger is to call `deposit` with `amt = 0` (this is another issue that should be fixed IMO, in practice the assets of an account should not contain any tokens with zero balance)
Some tokens revert for zero value transfers (see https://github.com/d-xo/weird-erc20)
3.) Paused tokens
4.) Upgradeable tokens that changed the implementation.

## Impact
See above, an account cannot be liquidated. In certain conditions, this might even be triggerable by the user. For instance, a user could try to get on the USDC blacklist to avoid liquidations.

## Code Snippet
https://github.com/sherlock-audit/2022-08-sentiment/blob/main/protocol/src/core/AccountManager.sol#L384
https://github.com/sherlock-audit/2022-08-sentiment/blob/main/protocol/src/core/Account.sol#L166

## Tool used

Manual Review

## Recommendation
Catch reversions for the transfer and skip this asset (but it could be kept in the assets list to allow retries later on).

## Sentiment Team
Fixed as recommended. PR [here](https://github.com/sentimentxyz/protocol/pull/231).

## Lead Senior Watson
Confirmed fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment |
| Report Date | N/A |
| Finders | csanuragjain, Czar102, panprog, PwnPatrol, rbserver, Chom, berndartmueller, Lambda, kirk-baird, \_\_141345\_\_, carrot |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/033-M
- **Contest**: https://app.sherlock.xyz/audits/contests/1

### Keywords for Search

`vulnerability`

