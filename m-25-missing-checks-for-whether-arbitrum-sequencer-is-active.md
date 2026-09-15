---
# Core Classification
protocol: GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18672
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/6
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-gmx-judging/issues/151

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
finders_count: 5
finders:
  - hack3r-0m
  - IllIllI
  - 0xdeadbeef
  - ShadowForce
  - GalloDaSballo
---

## Vulnerability Title

M-25: Missing checks for whether Arbitrum Sequencer is active

### Overview


This bug report is regarding an issue found in the code of the GMX Synthetics contract. The issue is that there are no checks in place to determine whether the Arbitrum Sequencer is active. Chainlink recommends that users using price oracles check this before submitting orders. If the sequencer is offline, the index oracles may have stale prices and this could lead to people submitting orders and getting execution prices that do not exist in reality. The bug was found using manual review and the recommended solution is to use a Chainlink oracle to determine whether the sequencer is offline or not, and not allow orders to be executed while the sequencer is offline. A discussion was also held regarding the risk being reduced with a keeper network instead of a separate check.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-gmx-judging/issues/151 

## Found by 
0xdeadbeef, GalloDaSballo, IllIllI, ShadowForce, hack3r-0m

## Summary

Chainlink recommends that users using price oracles, check whether the Arbitrum Sequencer is [active](https://docs.chain.link/data-feeds/l2-sequencer-feeds#arbitrum)


## Vulnerability Detail

If the sequencer goes down, the index oracles may have stale prices, since L2-submitted transactions (i.e. by the aggregating oracles) will not be processed.

## Impact

Stale prices, e.g. if USDC were to de-peg while the sequencer is offline, would let people submit orders and if those people are also keepers, get execution prices that do not exist in reality.

## Code Snippet

Chainlink oracles are used for some prices, but there are no sequencer oracles in use:

```solidity
// File: gmx-synthetics/contracts/oracle/Oracle.sol : Oracle._setPricesFromPriceFeeds()   #1

569                IPriceFeed priceFeed = getPriceFeed(dataStore, token);
570    
571                (
572                    /* uint80 roundID */,
573                    int256 _price,
574                    /* uint256 startedAt */,
575                    /* uint256 timestamp */,
576                    /* uint80 answeredInRound */
577                ) = priceFeed.latestRoundData();
578    
579:               uint256 price = SafeCast.toUint256(_price);
```
https://github.com/sherlock-audit/2023-02-gmx/blob/main/gmx-synthetics/contracts/oracle/Oracle.sol#L569-L579


## Tool used

Manual Review


## Recommendation

Use a [chainlink oracle](https://blog.chain.link/how-to-use-chainlink-price-feeds-on-arbitrum/#almost_done!_meet_the_l2_sequencer_health_flag) to determine whether the sequencer is offline or not, and don't allow orders to be executed while the sequencer is offline.



## Discussion

**xvi10**

This is a valid issue, the risk will be reduced with a keeper network instead of a separate check

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | GMX |
| Report Date | N/A |
| Finders | hack3r-0m, IllIllI, 0xdeadbeef, ShadowForce, GalloDaSballo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-gmx-judging/issues/151
- **Contest**: https://app.sherlock.xyz/audits/contests/6

### Keywords for Search

`vulnerability`

