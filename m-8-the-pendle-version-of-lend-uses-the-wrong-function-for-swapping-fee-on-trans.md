---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3736
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/12
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/105

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
  - fee_on_transfer

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - IllIllI
---

## Vulnerability Title

M-8: The Pendle version of `lend()` uses the wrong function for swapping fee-on-transfer tokens

### Overview


This bug report is about the Pendle version of the `lend()` function which is part of the Illuminate protocol. The bug is that the Pendle version of `lend()` uses the wrong Sushiswap function to swap fee-on-transfer tokens. The wrong function being used is `swapExactTokensForTokens()` when it should use `swapExactTokensForTokensSupportingFeeOnTransferTokens()`. As a result, users will be unable to use the Pendle version of `lend()` when the underlying is a fee-on-transfer token with the fee turned on. The bug was found by IllIllI and was confirmed by JTraversa and 0x00052. It was then escalated for 1 USDC by 0x00052 with a reminder to Evert0x. Sherlock-admin then confirmed the escalation. The recommended solution is to use `swapExactTokensForTokensSupportingFeeOnTransferTokens()` instead.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/105 

## Found by 
IllIllI

## Summary

The Pendle version of `lend()` uses the wrong function for swapping fee-on-transfer tokens


## Vulnerability Detail
The Pendle version of `lend()` is not able to handle fee-on-transfer tokens properly (USDT is a fee-on-transfer token which is [supported](https://github.com/sherlock-audit/2022-10-illuminate/blob/main/test/fork/Contracts.sol#L61-L62)) and pulls out the contract's fee balance (I've filed this issue separately). Once that is fixed there still is the fact that the Pendle version uses the wrong Sushiswap function (the Pendle router is a Sushiswap router). The function uses `swapExactTokensForTokens()` when it should use [`swapExactTokensForTokensSupportingFeeOnTransferTokens()`](https://github.com/sushiswap/sushiswap/blob/99c16c262f70a1ea8b6583c08c51f176eeb8f521/protocols/sushiswap/contracts/UniswapV2Router02.sol#L340-L346) instead.


## Impact
_Smart contract unable to operate due to lack of token funds_

Users will be unable to use the Pendle version of `lend()` when the underlying is a fee-on-transfer token with the fee turned on (USDT currently has the fee turned off, but they can turn it on at any moment).

## Code Snippet

The pulling in of the amount by `IPendle` will either take part of the Illuminate protocol fees, or will revert if there is not enough underlying after the fee is applied for the Sushiswap transfer (depending on which fee-on-transfer fix is applied for the other issue I filed):
```solidity
// File: src/Lender.sol : Lender.lend()   #1

541                address[] memory path = new address[](2);
542                path[0] = u;
543                path[1] = principal;
544    
545                // Swap on the Pendle Router using the provided market and params
546 @>             returned = IPendle(pendleAddr).swapExactTokensForTokens(
547 @>                 a - fee,
548 @>                 r,
549 @>                 path,
550 @>                 address(this),
551 @>                 d
552 @>             )[1];
553            }
554    
555            // Mint Illuminate zero coupons
556            IERC5095(principalToken(u, m)).authMint(msg.sender, returned);
557    
558            emit Lend(p, u, m, returned, a, msg.sender);
559            return returned;
560:       }
```
https://github.com/sherlock-audit/2022-10-illuminate/blob/main/src/Lender.sol#L536-L560


## Tool used

Manual Review

## Recommendation
Use `swapExactTokensForTokensSupportingFeeOnTransferTokens()`

## Discussion

**JTraversa**

Same as #116 

**0x00052**

Escalate for 1 USDC

Reminder @Evert0x 

**sherlock-admin**

 > Escalate for 1 USDC
> 
> Reminder @Evert0x 

You've created a valid escalation for 1 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | IllIllI |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/105
- **Contest**: https://app.sherlock.xyz/audits/contests/12

### Keywords for Search

`Fee On Transfer`

