---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: uniswap

# Attack Vector Details
attack_type: uniswap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3345
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/2
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-notional-judging/issues/33

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - uniswap
  - swap

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0x52
  - Chom
---

## Vulnerability Title

M-20: UniV2Adapter#getExecutionData doesn't properly handle native ETH swaps

### Overview


This bug report is about UniV2Adapter#getExecutionData which does not properly handle native ETH swaps. It was found by Chom, 0x52 and the code snippet can be found in UniV2Adapter.sol#L12-L52. The issue is that neither method selected supports direct ETH trades, and sender/target are not set correctly for TradingUtils_executeTrade to automatically convert. As a result, all Uniswap V2 calls made with native ETH will fail. This is an important feature that currently does not function, as Notional operates in native ETH rather than WETH. 

There are two possible solutions for this issue. The first is to change the way that target and sender are set to match the implementation in UniV3Adapter. The second is to modify the return data to return the correct selector for each case (swapExactETHForTokens, swapTokensForExactETH, etc.). The first option would be the easiest, and would give the same results considering it's basically the same as what the router is doing internally anyways.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-notional-judging/issues/33 

## Found by 
Chom, 0x52

## Summary

UniV2Adapter#getExecutionData doesn't properly account for native ETH trades which makes them impossible. Neither method selected supports direct ETH trades, and sender/target are not set correctly for TradingUtils_executeTrade to automatically convert

## Vulnerability Detail

    spender = address(Deployments.UNIV2_ROUTER);
    target = address(Deployments.UNIV2_ROUTER);
    // msgValue is always zero for uniswap

    if (
        tradeType == TradeType.EXACT_IN_SINGLE ||
        tradeType == TradeType.EXACT_IN_BATCH
    ) {
        executionCallData = abi.encodeWithSelector(
            IUniV2Router2.swapExactTokensForTokens.selector,
            trade.amount,
            trade.limit,
            data.path,
            from,
            trade.deadline
        );
    } else if (
        tradeType == TradeType.EXACT_OUT_SINGLE ||
        tradeType == TradeType.EXACT_OUT_BATCH
    ) {
        executionCallData = abi.encodeWithSelector(
            IUniV2Router2.swapTokensForExactTokens.selector,
            trade.amount,
            trade.limit,
            data.path,
            from,
            trade.deadline
        );
    }

UniV2Adapter#getExecutionData either returns the swapTokensForExactTokens or swapExactTokensForTokens, neither of with support native ETH. It also doesn't set spender and target like UniV3Adapter, so _executeTrade won't automatically convert it to a WETH call. The result is that all Uniswap V2 calls made with native ETH will fail. Given that Notional operates in native ETH rather than WETH, this is an important feature that currently does not function.

## Impact

Uniswap V2 calls won't support native ETH

## Code Snippet

[UniV2Adapter.sol#L12-L52](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/adapters/UniV2Adapter.sol#L12-L52)

## Tool used

Manual Review

## Recommendation

There are two possible solutions:

1) Change the way that target and sender are set to match the implementation in UniV3Adapter
2) Modify the return data to return the correct selector for each case (swapExactETHForTokens, swapTokensForExactETH, etc.)

Given that the infrastructure for Uniswap V3 already exists in TradingUtils_executeTrade the first option would be the easiest, and would give the same results considering it's basically the same as what the router is doing internally anyways.

## Discussion

**jeffywu**

@weitianjie2000

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Notional |
| Report Date | N/A |
| Finders | 0x52, Chom |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-notional-judging/issues/33
- **Contest**: https://app.sherlock.xyz/audits/contests/2

### Keywords for Search

`Uniswap, Swap`

