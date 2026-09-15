---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1628
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/140

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
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - hyh
---

## Vulnerability Title

[H-05] Users will lose a majority or even all of the rewards when the amount of total shares is too large, due to precision loss

### Overview


This bug report is about an issue in the LiquidityFarming and LiquidityProviders contracts of the Biconomy project. The issue occurs when the totalSharesStaked is large enough, causing the users to lose their rewards due to precision loss.

In the LiquidityFarming contract, the accTokenPerShare is calculated based on the total staked shares. However, in the LiquidityProviders contract, the mintedSharesAmount can become very large, resulting in precision loss.

The proof of concept (PoC) provided in the report explains how Alice could lose her rewards due to this issue. The PoC shows that when the totalSharesStaked is larger than 1e36, the accumulator will be rounded down to 0.

The report provides two recommendations to fix this issue. The first is to consider lowering the BASE_DIVISOR so that the initial share price can be higher. The second is to consider making the ACC_TOKEN_PRECISION larger to prevent precision loss.

### Original Finding Content

_Submitted by WatchPug, also found by hyh_

[LiquidityFarming.sol#L265-L291](https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityFarming.sol#L265-L291)<br>

```solidity
function getUpdatedAccTokenPerShare(address _baseToken) public view returns (uint256) {
    uint256 accumulator = 0;
    uint256 lastUpdatedTime = poolInfo[_baseToken].lastRewardTime;
    uint256 counter = block.timestamp;
    uint256 i = rewardRateLog[_baseToken].length - 1;
    while (true) {
        if (lastUpdatedTime >= counter) {
            break;
        }
        unchecked {
            accumulator +=
                rewardRateLog[_baseToken][i].rewardsPerSecond *
                (counter - max(lastUpdatedTime, rewardRateLog[_baseToken][i].timestamp));
        }
        counter = rewardRateLog[_baseToken][i].timestamp;
        if (i == 0) {
            break;
        }
        --i;
    }

    // We know that during all the periods that were included in the current iterations,
    // the value of totalSharesStaked[_baseToken] would not have changed, as we only consider the
    // updates to the pool that happened after the lastUpdatedTime.
    accumulator = (accumulator * ACC_TOKEN_PRECISION) / totalSharesStaked[_baseToken];
    return accumulator + poolInfo[_baseToken].accTokenPerShare;
}
```

[LiquidityProviders.sol#L286-L292](https://github.com/code-423n4/2022-03-biconomy/blob/04751283f85c9fc94fb644ff2b489ec339cd9ffc/contracts/hyphen/LiquidityProviders.sol#L286-L292)<br>

```solidity
uint256 mintedSharesAmount;
// Adding liquidity in the pool for the first time
if (totalReserve[token] == 0) {
    mintedSharesAmount = BASE_DIVISOR * _amount;
} else {
    mintedSharesAmount = (_amount * totalSharesMinted[token]) / totalReserve[token];
}
```

In `HyphenLiquidityFarming`, the `accTokenPerShare` is calculated based on the total staked shares.

However, as the `mintedSharesAmount` can easily become very large on `LiquidityProviders.sol`, all the users can lose their rewards due to precision loss.

### Proof of Concept

Given:

*   rewardsPerSecond is `10e18`;
*   lastRewardTime is 24 hrs ago;

Then:

1.  Alice `addTokenLiquidity()` with `1e8 * 1e18` XYZ on B-Chain, totalSharesMinted == `1e44`;
2.  Alice `deposit()` to HyphenLiquidityFarming, totalSharesStaked == `1e44`;
3.  24 hrs later, Alice tries to claim the rewards.

`accumulator = rewardsPerSecond * 24 hours` == 864000e18 == 8.64e23

Expected Results: As the sole staker, Alice should get all the `864000e18` rewards.

Actual Results: Alice received 0 rewards.

That's because when `totalSharesStaked > 1e36`, `accumulator = (accumulator * ACC_TOKEN_PRECISION) / totalSharesStaked[_baseToken];` will be round down to `0`.

When the `totalSharesStaked` is large enough, all users will lose their rewards due to precision loss.

### Recommended Mitigation Steps

1.  Consider lowering the `BASE_DIVISOR` so that the initial share price can be higher;
2.  Consider making `ACC_TOKEN_PRECISION` larger to prevent precision loss;

See also the Recommendation on [Issue #139](https://github.com/code-423n4/2022-03-biconomy-findings/issues/139).

**[ankurdubey521 (Biconomy) confirmed](https://github.com/code-423n4/2022-03-biconomy-findings/issues/140)**

**[pauliax (judge) commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/140#issuecomment-1120958989):**
 > Great find, probably deserves a severity of high.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | WatchPug, hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/140
- **Contest**: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest

### Keywords for Search

`vulnerability`

