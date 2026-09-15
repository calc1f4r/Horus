---
# Core Classification
protocol: Real Wagmi #2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27403
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/118
source_link: none
github_link: https://github.com/sherlock-audit/2023-10-real-wagmi-judging/issues/104

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
finders_count: 3
finders:
  - shogoki
  - HHK
  - 0x52
---

## Vulnerability Title

M-6: `computePoolAddress()` will not work on ZkSync Era

### Overview


This bug report is about the `computePoolAddress()` function not working on ZkSync Era when using the wagmi protocol. This function is used when a user is borrowing or repaying a position and is using Uniswap v3 as a fallback. The `computePoolAddress()` function is used to check that the callback is a pool and on ZkSync Era it will not match. This could lead to a user not being able to close their position and having to pay collateral for a longer time.

The impact of this issue is medium as it is unlikely to happen, but it could result in short-term DOS and more fees paid by the borrower. The team recommends calling the Uniswap factory getter `getPool()` to get the address of the pool. They are not planning to make any fixes to this issue right now.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-10-real-wagmi-judging/issues/104 

## Found by 
0x52, HHK, shogoki

When using the wagmi protocol, multiple swap can happen when borrowing or repaying a position. When the swap uses Uniswap v3 it checks that the callback is a pool by computing the address but the computation won't match on ZkSync Era.

## Vulnerability Detail

When borrowing or repaying a position a user can either use a custom router that was approved by the wagmi team to make the swaps required or can use Uniswap v3 as a fallback.

When using the Uniswap v3 as a fallback the [`_v3SwapExactInput()`](https://github.com/sherlock-audit/2023-10-real-wagmi/blob/b33752757fd6a9f404b8577c1eae6c5774b3a0db/wagmi-leverage/contracts/abstract/ApproveSwapAndPay.sol#L204) internal function is being called. This function uses [`computePoolAddress()`](https://github.com/sherlock-audit/2023-10-real-wagmi/blob/b33752757fd6a9f404b8577c1eae6c5774b3a0db/wagmi-leverage/contracts/abstract/ApproveSwapAndPay.sol#L271) to find the pool address to use. [`computePoolAddress()`](https://github.com/sherlock-audit/2023-10-real-wagmi/blob/b33752757fd6a9f404b8577c1eae6c5774b3a0db/wagmi-leverage/contracts/abstract/ApproveSwapAndPay.sol#L271) is also used during the [`uniswapV3SwapCallback()`](https://github.com/sherlock-audit/2023-10-real-wagmi/blob/b33752757fd6a9f404b8577c1eae6c5774b3a0db/wagmi-leverage/contracts/abstract/ApproveSwapAndPay.sol#L242) to make sure the `msg.sender` is a valid pool.

On ZkSync Era the `create2` addresses are not computed the same way see [here](https://era.zksync.io/docs/reference/architecture/differences-with-ethereum.html#address-derivation).

This will result in the swaps on Uniswapv3 to revert. If a user was able to open a position using a custom router but the custom router is removed later on by the team or if the liquidity was one sided so no swap happened. The borrower and liquidators could find themself not able to close the positions until a new router is whitelisted.

The borrower could be forced to pay collateral for a longer time as he won't be able to close his position.

## Impact

Medium. Unlikely to happen but would result in short-term DOS and more fees paid by the borrower.

## Code Snippet

https://github.com/sherlock-audit/2023-10-real-wagmi/blob/b33752757fd6a9f404b8577c1eae6c5774b3a0db/wagmi-leverage/contracts/abstract/ApproveSwapAndPay.sol#L146
https://github.com/sherlock-audit/2023-10-real-wagmi/blob/b33752757fd6a9f404b8577c1eae6c5774b3a0db/wagmi-leverage/contracts/abstract/ApproveSwapAndPay.sol#L204
https://github.com/sherlock-audit/2023-10-real-wagmi/blob/b33752757fd6a9f404b8577c1eae6c5774b3a0db/wagmi-leverage/contracts/abstract/ApproveSwapAndPay.sol#L271

## Tool used

Manual Review

## Recommendation

Consider calling the Uniswap factory getter `getPool()` to get the address of the pool.



## Discussion

**fann95**

This is too obvious a problem with which this project simply will not work. We know about this, so we will make changes before deployment in ZkSync Era.

**Czar102**

As the contest readme states, watsons were to consider zkSync as one of the chains the code in scope was to be deployed on. If watsons couldn't have known that a modification of the code in scope would be deployed on zkSync, I don't see a reason to invalidate this issue, even if it was previously considered by the protocol team and/or is trivial.

**fann95**

I’m pasting the solution for Sherlock, but we don’t plan to make any fixes to this issue right now.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Real Wagmi #2 |
| Report Date | N/A |
| Finders | shogoki, HHK, 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-10-real-wagmi-judging/issues/104
- **Contest**: https://app.sherlock.xyz/audits/contests/118

### Keywords for Search

`vulnerability`

