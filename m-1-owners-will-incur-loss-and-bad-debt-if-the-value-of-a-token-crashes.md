---
# Core Classification
protocol: GFX Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21130
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/97
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-gfx-judging/issues/51

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - xiaoming90
---

## Vulnerability Title

M-1: Owners will incur loss and bad debt if the value of a token crashes

### Overview


This bug report addresses an issue where the owner of an automated order fulfillment contract might incur loss or bad debt if the value of the swapped tokens crash. In this case, users will choose not to claim the orders, resulting in the owner being unable to recoup back the gas fee they have already paid for automating the fulfillment of the orders. The code snippet provided highlights the relevant code, which is from the LimitOrderRegistry.sol file.

The impact of this issue is that owners might be unable to recoup back the gas fee the owner has already paid for automating the fulfillment of the orders, incurring loss and bad debt. The recommendation for this issue is to consider collecting the fee in advance based on a rough estimation of the expected gas fee. If many users choose to abandon the orders, the owner will not incur any significant losses.

The discussion following this bug report states that this is a known issue, but it is unlikely to be fixed. The owner recognizes that gas can possibly be "wasted" under bad network conditions.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-gfx-judging/issues/51 

## Found by 
xiaoming90
## Summary

If the value of the swapped tokens crash, many users will choose not to claim the orders, which result in the owner being unable to recoup back the gas fee the owner has already paid for automating the fulfillment of the orders, incurring loss and bad debt.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-06-gfx/blob/main/uniswap-v3-limit-orders/src/LimitOrderRegistry.sol#L696

```solidity
File: LimitOrderRegistry.sol
696:     function claimOrder(uint128 batchId, address user) external payable returns (ERC20, uint256) {
..SNIP..
726:         // Transfer fee in.
727:         address sender = _msgSender();
728:         if (msg.value >= userClaim.feePerUser) {
729:             // refund if necessary.
730:             uint256 refund = msg.value - userClaim.feePerUser;
731:             if (refund > 0) sender.safeTransferETH(refund);
732:         } else {
733:             WRAPPED_NATIVE.safeTransferFrom(sender, address(this), userClaim.feePerUser);
734:             // If value is non zero send it back to caller.
735:             if (msg.value > 0) sender.safeTransferETH(msg.value);
736:         }
```

Users only need to pay for the gas cost for fulfilling the order when they claim the order to retrieve the swapped tokens. When the order is fulfilled, the swapped tokens will be sent to and stored in the `LimitOrderRegistry` contract. 

However, in the event that the value of the swapped tokens crash (e.g., Terra's LUNA crash), it makes more economic sense for the users to abandon (similar to defaulting in traditional finance) the orders without claiming the worthless tokens to avoid paying the more expensive fee to the owner.

As a result, many users will choose not to claim the orders, which result in the owner being unable to recoup back the gas fee the owner has already paid for automating the fulfillment of the orders, incurring loss and bad debt.

## Impact

Owners might be unable to recoup back the gas fee the owner has already paid for automating the fulfillment of the orders, incurring loss and bad debt.

## Code Snippet

https://github.com/sherlock-audit/2023-06-gfx/blob/main/uniswap-v3-limit-orders/src/LimitOrderRegistry.sol#L696

## Tool used

Manual Review

## Recommendation

Consider collecting the fee in advance based on a rough estimation of the expected gas fee. When the users claim the order, any excess fee will be refunded, or any deficit will be collected from the users. 

In this case, if many users choose to abandon the orders, the owner will not incur any significant losses.



## Discussion

**elee1766**

this is a known issue, but i don't think we will fix it. 

owners recognize that gas can possibly be "wasted" under bad network conditions

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | GFX Labs |
| Report Date | N/A |
| Finders | xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-gfx-judging/issues/51
- **Contest**: https://app.sherlock.xyz/audits/contests/97

### Keywords for Search

`vulnerability`

