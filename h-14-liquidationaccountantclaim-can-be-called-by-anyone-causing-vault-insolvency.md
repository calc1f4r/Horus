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
solodit_id: 3652
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/188

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
finders_count: 4
finders:
  - 0xRajeev
  - rvierdiiev
  - obront
  - TurnipBoy
---

## Vulnerability Title

H-14: `LiquidationAccountant.claim()` can be called by anyone causing vault insolvency

### Overview


This bug report is about the vulnerability in the `LiquidationAccountant.claim()` function of the PublicVault smart contract. This function can be called by anyone and any number of times, allowing them to manipulate the `yIntercept` of a public vault by triggering the `claim()` flow after liquidations, resulting in vault insolvency. This means that anyone can cause the vault to become insolvent and cause losses to all depositors. The issue was found by obront, TurnipBoy, 0xRajeev, and rvierdiiev and the tool used was Manual Review. The recommendation to fix the issue is to allow only the vault to call `claim()` by requiring authorizations. The issue was escalated for 1 USDC, accepted, and the contestants' payouts and scores will be updated according to the changes made.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/188 

## Found by 
obront, TurnipBoy, 0xRajeev, rvierdiiev

## Summary

`LiquidationAccountant.claim()` can be called by anyone to reduce the implied value of a public vault.

## Vulnerability Detail

`LiquidationAccountant.claim()` is called by the `PublicVault` as part of the `processEpoch()` flow. But it has no access control and can be called by anyone and any number of times. If called after `finalAuctionEnd`, one will be able to trigger `decreaseYIntercept()` on the vault even if they cannot affect fund transfer to withdrawing liquidity providers and the PublicVault.

## Impact

This allows anyone to manipulate the `yIntercept` of a public vault by triggering the `claim()` flow after liquidations resulting in vault insolvency.

## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LiquidationAccountant.sol#L65-L97

## Tool used

Manual Review

## Recommendation

Allow only vault to call `claim()` by requiring authorizations.

## Discussion

**SantiagoGregory**

Our updated LiquidationAccountant implementation (now moved to WithdrawProxy) tracks a hasClaimed bool to make sure claim() is only called once (we also now block claim() from being called until after finalAuctionEnd).

**IAmTurnipBoy**

Escalate for 1 USDC

Abuse can cause vault to implode and cause loss of funds to all depositors. Should be high

**sherlock-admin**

 > Escalate for 1 USDC
> 
> Abuse can cause vault to implode and cause loss of funds to all depositors. Should be high

You've created a valid escalation for 1 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Evert0x**


Escalation accepted.



**sherlock-admin**

> 
> Escalation accepted.
> 
> 

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
| Finders | 0xRajeev, rvierdiiev, obront, TurnipBoy |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/188
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

