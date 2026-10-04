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
solodit_id: 3678
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/232

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - TurnipBoy
---

## Vulnerability Title

M-3: _makePayment is logically inconsistent with how lien stack is managed causing payments to multiple liens to fail

### Overview


This bug report is about an issue found in the code for the LienToken.sol file. The `_makePayment(uint256, uint256)` looping logic is inconsistent with how `_deleteLienPosition` manages the lien stack. This inconsistency creates an issue when a payment is made that pays off multiple liens as the compressing effect of `_deleteLienPosition` causes an array out of bounds error towards the end of the loop.

The bug was found by TurnipBoy who used manual review as the tool for detection. The code snippet in question is located at https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L410-L424. The impact of this bug is that large payments are impossible and users must manually pay off each lien separately. The recommendation is that the payment logic inside of `AuctionHouse.sol` should be used as a model for how to fix the issue with `_makePayment`.

IAmTurnipBoy and sherlock-admin then escalated the issue for 1 USDC and Evert0x accepted the escalation. The escalation can be edited or deleted anytime before the 48-hour window closes. After that, the escalation becomes final.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/232 

## Found by 
TurnipBoy

## Summary

`_makePayment(uint256, uint256)` looping logic is inconsistent with how `_deleteLienPosition` manages the lien stack. `_makePayment` loops from 0 to `openLiens.length` but `_deleteLienPosition` (called when a lien is fully paid off) actively compresses the lien stack. When a payment pays off multiple liens the compressing effect causes an array OOB error towards the end of the loop.

## Vulnerability Detail

    function _makePayment(uint256 collateralId, uint256 totalCapitalAvailable)
      internal
    {
      uint256[] memory openLiens = liens[collateralId];
      uint256 paymentAmount = totalCapitalAvailable;
      for (uint256 i = 0; i < openLiens.length; ++i) {
        uint256 capitalSpent = _payment(
          collateralId,
          uint8(i),
          paymentAmount,
          address(msg.sender)
        );
        paymentAmount -= capitalSpent;
      }
    }

`LienToken.sol#_makePayment(uint256, uint256)` loops from 0 to `openLiens.Length`. This loop attempts to make a payment to each lien calling `_payment` with the current index of the loop.

    function _deleteLienPosition(uint256 collateralId, uint256 position) public {
      uint256[] storage stack = liens[collateralId];
      require(position < stack.length, "index out of bounds");

      emit RemoveLien(
        stack[position],
        lienData[stack[position]].collateralId,
        lienData[stack[position]].position
      );
      for (uint256 i = position; i < stack.length - 1; i++) {
        stack[i] = stack[i + 1];
      }
      stack.pop();
    }

`LienToken.sol#_deleteLienPosition` is called on liens when they are fully paid off. The most interesting portion of the function is how the lien is removed from the stack. We can see that all liens above the lien in question are slid down the stack and the top is popped. This has the effect of reducing the total length of the array. This is where the logical inconsistency is. If the first lien is paid off, it will be removed and the formerly second lien will now occupy it's index. So then when `_payment` is called in the next loop with the next index it won't reference the second lien since the second lien is now in the first lien index.

Assuming there are 2 liens on some collateral. `liens[0].amount = 100` and `liens[1].amount = 50`. A user wants to pay off their entire lien balance so they call  `_makePayment(uint256, uint256)` with an amount of 150. On the first loop it calls `_payment` with an index of 0. This pays off `liens[0]`. `_deleteLienPosition` is called with index of 0 removing `liens[0]`. Because of the sliding logic in `_deleteLienPosition` `lien[1]` has now slid into the `lien[0]` position. On the second loop it calls `_payment` with an index of 1. When it tries to grab the data for the lien at that index it will revert due to OOB error because the array no long contains an index of 1.

## Impact

Large payment are impossible and user must manually pay off each liens separately 

## Code Snippet

https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L410-L424

## Tool used

Manual Review

## Recommendation

Payment logic inside of `AuctionHouse.sol` works. `_makePayment` should be changed to mimic that logic.



## Discussion

**IAmTurnipBoy**

Escalate for 1 USDC

Not a dupe of #190, issue is with the lien array is managed as the payments are made. Fixing #190 wouldn't fix this.

**sherlock-admin**

 > Escalate for 1 USDC
> 
> Not a dupe of #190, issue is with the lien array is managed as the payments are made. Fixing #190 wouldn't fix this.

You've created a valid escalation for 1 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Evert0x**

Escalation accepeted

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | TurnipBoy |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/232
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

