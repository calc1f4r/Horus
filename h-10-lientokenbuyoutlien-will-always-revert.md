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
solodit_id: 3648
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/196

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
finders_count: 9
finders:
  - supernova
  - 8olidity
  - yixxas
  - cccz
  - 0xRajeev
---

## Vulnerability Title

H-10: `LienToken.buyoutLien` will always revert

### Overview


This bug report is about an issue found in the Astaria protocol, which is a protocol for lending and borrowing on Ethereum. The issue is that the function `buyoutLien()` will always revert, preventing the borrower from refinancing. This is caused by `buyoutFeeDenominator` being `0` without a setter. The impact of this issue is that the borrower will be locked into their current loan even if better terms are available, leading to loss of funds. The code snippet of the issue is provided in the report. The recommendation given is to initialize the buyout fee numerator and denominator in `AstariaRouter` and add their setters to `file()`. The discussion in the report is about the severity of the issue and the payout for the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/196 

## Found by 
yixxas, ctf\_sec, neila, 0xRajeev, supernova, rvierdiiev, zzykxx, 8olidity, cccz

## Summary

`buyoutLien()` will always revert, preventing the borrower from refinancing.

## Vulnerability Detail

`buyoutFeeDenominator` is `0` without a setter which will cause `getBuyoutFee()` to revert in the `buyoutLien()` flow. 

## Impact

Refinancing is a crucial feature of the protocol to allow a borrower to refinance their loan if a certain minimum improvement of interest rate or duration is offered. The reverting `buyoutLien()` flow will prevent the borrower from refinancing and effectively lead to loss of their funds due to lock-in into currently held loans when better terms are available.

## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L71
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L456
3. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L377
4. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L132

## Tool used

Manual Review

## Recommendation

Initialize the buyout fee numerator and denominator in `AstariaRouter` and add their setters to `file()`.

## Discussion

**secureum**

Escalate for 2 USDC.

Given the potential impact to different flows/contexts, we still think this is a high-severity impact (not Medium as judged). A majority of the dups (while some are dups of a different but related issue) also reported this as a High.

cc @berndartmueller @lucyoa

**sherlock-admin**

 > Escalate for 2 USDC.
> 
> Given the potential impact to different flows/contexts, we still think this is a high-severity impact (not Medium as judged). A majority of the dups (while some are dups of a different but related issue) also reported this as a High.
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
| Finders | supernova, 8olidity, yixxas, cccz, 0xRajeev, neila, rvierdiiev, zzykxx, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/196
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

