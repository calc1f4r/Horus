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
solodit_id: 3651
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/190

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
  - Jeiwan
  - obront
  - zzykxx
---

## Vulnerability Title

H-13: A payment made towards multiple liens causes the borrower to lose funds to the payee

### Overview


This bug report is about an issue found in the Sherlock Audit project - Astaria Judging. It was found by obront, Jeiwan, zzykxx, and 0xRajeev. The issue is that when a borrower makes a payment towards multiple liens, the entire payment is sent to the payee of the first lien, causing the borrower to lose funds. This happens because when the underlying _makePayment() function loops over the open liens, the entire payment amount is provided in the call to _payment() in the first iteration, and the amount is returned as capitalSpent, making the paymentAmount for the next iteration equal to 0. 

The impact of this issue is that only the first lien is paid off and the entire payment is sent to its payee, while the remaining liens remain unpaid and the borrower loses funds to the payee. The code snippet for this issue can be found at the following links: https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L387-L389, https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L410-L424, and https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L630-L645.

The recommendation for this issue is to add paymentAmount -= lien.amount in the else block of _payment(). The discussion for this issue includes IAmTurnipBoy escalating for 1 USDC and sherlock-admin accepting the escalation. Contestants' payouts and scores will be updated according to the changes made on this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/190 

## Found by 
obront, Jeiwan, zzykxx, 0xRajeev

## Summary

A payment made towards multiple liens is entirely consumed for the first one causing the borrower to lose funds to the payee.

## Vulnerability Detail

A borrower can make a bulk payment against multiple liens for a collateral hoping to pay more than one at a time using `makePayment (uint256 collateralId, uint256 paymentAmount)` where the underlying `_makePayment()` loops over the open liens attempting to pay off more than one depending on the `totalCapitalAvailable` provided.

However, the entire `totalCapitalAvailable` is provided via `paymentAmount` in the call to `_payment()` in the first iteration which transfers that completely to the payee in its logic even if it exceeds that `lien.amount`. That total amount is returned as `capitalSpent` which makes the `paymentAmount` for next iteration equal to `0`.

## Impact

Only the first lien is paid off and the entire payment is sent to its payee. The remaining liens remain unpaid. The payment maker (i.e. borrower ) loses funds to the payee.

## Code Snippet
1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L387-L389
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L410-L424
3. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L630-L645

## Tool used

Manual Review

## Recommendation

Add `paymentAmount -= lien.amount` in the `else` block of `_payment()`.

## Discussion

**IAmTurnipBoy**

Escalate for 1 USDC

Clear loss of funds. Should be high

**sherlock-admin**

 > Escalate for 1 USDC
> 
> Clear loss of funds. Should be high

You've created a valid escalation for 1 USDC!

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
| Finders | 0xRajeev, Jeiwan, obront, zzykxx |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/190
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

