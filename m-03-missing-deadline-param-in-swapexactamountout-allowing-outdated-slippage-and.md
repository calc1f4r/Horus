---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25963
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-pooltogether
source_link: https://code4rena.com/reports/2023-08-pooltogether
github_link: https://github.com/code-423n4/2023-08-pooltogether-findings/issues/126

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
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - piyushshukla
  - bin2chen
  - SanketKogekar
  - MohammedRizwan
  - cartlex\_
---

## Vulnerability Title

[M-03]  Missing `deadline` param in `swapExactAmountOut()` allowing outdated slippage and allow pending transaction to be executed unexpectedly

### Overview


This bug report is about the loss of funds/tokens for the protocol in the case of block execution being delegated to the block validator without a hard deadline. The functions `swapExactAmountOut()` from `LiquidationRouter.sol` and `LiquidationPair.sol` use the methods `source.liquidate(_account, tokenIn, swapAmountIn, tokenOut, _amountOut);` and `_liquidationPair.swapExactAmountOut(_receiver, _amountOut, _amountInMax);` respectively to swap tokens. These methods make sure to pass slippage (minimum amount out), but miss to provide the deadline which is crucial to avoid unexpected trades/losses for users and protocol. Without a deadline, the transaction might be left hanging in the mempool and be executed way later than the user wanted, leading to users/protocol getting a worse price.

The recommended mitigation steps are that users should be allowed to provide a fixed deadline as parameter, and also never set deadline to `block.timestamp`. The severity of this issue has been marked as Medium, as when the value lost is guaranteed to be very large and preventing the mistake has a very low cost, it is reasonable to assign a medium risk rating.

### Original Finding Content


<https://github.com/GenerationSoftware/pt-v5-cgda-liquidator/blob/7f95bcacd4a566c2becb98d55c1886cadbaa8897/src/LiquidationRouter.sol#L63-L80><br>
<https://github.com/GenerationSoftware/pt-v5-cgda-liquidator/blob/7f95bcacd4a566c2becb98d55c1886cadbaa8897/src/LiquidationPair.sol#L211-L226>

Loss of funds/tokens for the protocol, since block execution is delegated to the block validator without a hard deadline.

### Proof of Concept

The function `swapExactAmountOut()` from `LiquidationRouter.sol` and `LiquidationPair.sol` use these methods to swap tokens:

`source.liquidate(_account, tokenIn, swapAmountIn, tokenOut, _amountOut);`

and

`_liquidationPair.swapExactAmountOut(_receiver, _amountOut, _amountInMax);`

<https://github.com/GenerationSoftware/pt-v5-cgda-liquidator/blob/7f95bcacd4a566c2becb98d55c1886cadbaa8897/src/LiquidationPair.sol#L211-L226>

<https://github.com/GenerationSoftware/pt-v5-cgda-liquidator/blob/7f95bcacd4a566c2becb98d55c1886cadbaa8897/src/LiquidationRouter.sol#L63-L80>

Both methods make sure to pass slippage (minimum amount out), but miss to provide the deadline which is crucial to avoid unexpected trades/losses for users and protocol.

Without a deadline, the transaction might be left hanging in the mempool and be executed way later than the user wanted.

That could lead to users/protocol getting a worse price, because a validator can just hold onto the transaction. And when it does get around to putting the transaction in a block

One part of this change is that PoS block proposers know ahead of time if they're going to propose the next block. The validators and the entire network know who's up to bat for the current block and the next one.

This means the block proposers are known for at least 6 minutes and 24 seconds and at most 12 minutes and 48 seconds.

Further reading: <https://blog.bytes032.xyz/p/why-you-should-stop-using-block-timestamp-as-deadline-in-swaps>

### Recommended Mitigation Steps

Let users provide a fixed deadline as param, and also never set deadline to `block.timestamp`.

**[asselstine (PoolTogether) confirmed](https://github.com/code-423n4/2023-08-pooltogether-findings/issues/126#issuecomment-1673816010)**

**[hickuphh3 (judge) commented](https://github.com/code-423n4/2023-08-pooltogether-findings/issues/126#issuecomment-1678355315):**
 > The main argument here is the user will lose out on positive slippage if the exchange rate becomes favourable when the tx is included in a block.
> 
> As to why it's Medium severity: when the value lost is guaranteed to be very large and preventing the mistake has a very low cost, it is reasonable to assign a medium risk rating. The closer the cost/benefit ratio gets to zero, the more likely the issue should be rated QA.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | piyushshukla, bin2chen, SanketKogekar, MohammedRizwan, cartlex\_ |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-pooltogether
- **GitHub**: https://github.com/code-423n4/2023-08-pooltogether-findings/issues/126
- **Contest**: https://code4rena.com/reports/2023-08-pooltogether

### Keywords for Search

`vulnerability`

