---
# Core Classification
protocol: Napier Finance - LST/LRT Integrations
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33331
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/369
source_link: none
github_link: https://github.com/sherlock-audit/2024-05-napier-update-judging/issues/36

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
finders_count: 6
finders:
  - ydlee
  - Ironsidesec
  - KupiaSec
  - Drynooo
  - no
---

## Vulnerability Title

M-6: Incorrect checking in `receiveFlashLoan` can cause `swapETHForYt` to fail unexpectedly.

### Overview


Issue M-6 is a bug in the MetapoolRouter contract that can cause the `swapETHForYt` function to fail unexpectedly. This is due to an incorrect check in the `receiveFlashLoan` function, which is supposed to ensure that the user has enough ETH to cover the `repayAmount` for the flash loan. However, the check is using the wrong variable and can result in the function failing even when the user has enough ETH. This bug was discovered by a team of security researchers and can be fixed by updating the check to use the correct variable. The impact of this bug is that it breaks the core functionality of the contract. The fix has been implemented in the protocol team's code and has been reviewed and approved by the Lead Senior Watson. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-05-napier-update-judging/issues/36 

## Found by 
Drynooo, Ironsidesec, KupiaSec, Varun\_05, no, ydlee
## Summary
The following checking in `receiveFlashLoad` is incorrect, causing `swapETHForYt` to fail.
```solidity
File: metapool-router/src/MetapoolRouter.sol

333:        if (repayAmount > remaining) revert Errors.MetapoolRouterInsufficientETHRepay(); // Can't repay the flash loan
```

## Vulnerability Detail
In line 333, the check here is to ensure that the `ETH` sent by the user is enough to cover the `repayAmount`. Thus the check should revert if `repayAmount > TransientStorage.tloadU256(TSLOT_CB_DATA_VALUE)` , instead of `repayAmount > remaining`.

Let's assume that:
1. The user swaps `5 ETH` for some Yt by `swapETHForYt`. (i.e. `msg.value = 5 ETH`)
2. The estimated amount of WETH required to issue the PT and YT is `4 WETH` (i.e. `wethDeposit = 4 WETH`). 
3. The PT are finally swapped to `2 WETH` (i.e. `wethReceived = 2 WETH`). 
4. The `feeAmount` of flash loan is `0.1 WETH`.

Then:
1. `repayAmount = wethDeposit + feeAmounts[0] = 4 WETH + 0.1 WETH = 4.1 WETH`
2. `spent = repayAmount - wethReceived = 4.1 WETH - 2 WETH = 2.1 WETH`
3. `remaining = 5 WETH - spent = 5 WETH - 2.1 WETH = 2.9 WETH`

Line 333 in `receiveFlashLoan` reverts as `repayAmount > remaining`, and the `swapETHForYt` fails. But the user pays more than required to swap. The fail is not expected.
```solidity
File: metapool-router/src/MetapoolRouter.sol

323:        // Calculate the amount of ETH spent in the swap
324:        uint256 repayAmount = wethDeposit + feeAmounts[0];
325:        uint256 spent = repayAmount - wethReceived; // wethDeposit + feeAmounts[0] - wethReceived
326:
327:        // Revert if the ETH spent exceeds the specified maximum
328:        if (spent > TransientStorage.tloadU256(TSLOT_CB_DATA_MAX_ETH_SPENT)) {
329:            revert Errors.MetapoolRouterExceededLimitETHIn();
330:        }
331:
332:        uint256 remaining = TransientStorage.tloadU256(TSLOT_CB_DATA_VALUE) - spent;
333:@>      if (repayAmount > remaining) revert Errors.MetapoolRouterInsufficientETHRepay(); // Can't repay the flash loan
```
https://github.com/sherlock-audit/2024-05-napier-update/blob/main/metapool-router/src/MetapoolRouter.sol#L323-L333

## Impact
Incorrect checking can cause `swapETHForYt` to fail unexpectedly, breaking the core functionality of the contract.

## Code Snippet
https://github.com/sherlock-audit/2024-05-napier-update/blob/main/metapool-router/src/MetapoolRouter.sol#L323-L333

## Tool used

Manual Review

## Recommendation
```solidity
-        if (repayAmount > remaining) revert Errors.MetapoolRouterInsufficientETHRepay();
+        if (repayAmount > TransientStorage.tloadU256(TSLOT_CB_DATA_VALUE)) revert Errors.MetapoolRouterInsufficientETHRepay();
```



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/napierfi/metapool-router/pull/28


**sherlock-admin2**

The Lead Senior Watson signed off on the fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Napier Finance - LST/LRT Integrations |
| Report Date | N/A |
| Finders | ydlee, Ironsidesec, KupiaSec, Drynooo, no, Varun\_05 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-05-napier-update-judging/issues/36
- **Contest**: https://app.sherlock.xyz/audits/contests/369

### Keywords for Search

`vulnerability`

