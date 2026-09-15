---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29632
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
github_link: none

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
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Jeiwan
  - Alex The Entreprenerd
  - Optimum
  - D-Nice
---

## Vulnerability Title

Liquidity staked at ticks can be manipulated to impact swap fees and rewards

### Overview


A bug has been found in the CLPool.sol code that can cause incorrect recording of staked liquidity amounts when removing all liquidity from a position. This can lead to a skewed total amount of staked liquidity in the pool, affecting the calculation of swap fees and gauge rewards. The issue has been fixed in the latest code update. The fix ensures that calls to updateStake() are skipped when the tick has been cleared, only occurring when the entire liquidity in the position is decreased and it is the only liquidity in the given tick ranges. The issue has been resolved in the latest code update.

### Original Finding Content

## Severity: High Risk

## Context
- CLPool.sol#L544-L545
- CLPool.sol#L367-L375

## Description
When removing all staked liquidity from a position via `CLGauge.decreaseStakedLiquidity()`, the amounts of staked liquidity at the ticks of the position are recorded incorrectly. Due to the clearing of the ticks, the lower tick will have a negative amount of staked liquidity and the upper tick will have a positive amount. In a normal situation, both values should be 0.

`CLGauge.decreaseStakedLiquidity()` calls `NonfungiblePositionManager.decreaseLiquidity()` (CLGauge.sol#L270) to remove liquidity from the position. The latter calls `CLPool.burn()` (NonfungiblePositionManager.sol#L296) to burn the liquidity from the pool. Burning liquidity updates a position (CLPool.sol#L497-L504, CLPool.sol#L260), which clears the ticks if all liquidity was removed from the position (CLPool.sol#L367-L375). This clearing will also clear the values of `stakedLiquidityNet` of the ticks. However, `CLGauge.decreaseStakedLiquidity()` then calls `CLPool.stake()` (CLGauge.sol#L280), which updates the staked liquidity in the ticks that have just been cleared (CLPool.sol#L544-L545).

As a result, the total amount of staked liquidity in a pool can be skewed during swapping, as the pool's staked liquidity is updated with the values stored at ticks (CLPool.sol#L726). This will have a strong impact on the protocol since both swap fees (CLPool.sol#L684-L685) and gauge rewards (CLPool.sol#L870) are computed based on the amount of staked liquidity.

While the impact can be caused by any user who removes their liquidity via `CLGauge.decreaseStakedLiquidity()`, we also believe that the miscalculation can be triggered intentionally to manipulate the value of staked liquidity to gain benefits from swap fees and/or gauge rewards.

## Recommendation
In `CLPool.stake()`, consider skipping a call to `ticks.updateStake()` when the value of `initialized` of the respective tick is false.

## Velodrome
The issue has been fixed in commit `171a82f2`. The fix that has been applied is to skip calls to `updateStake()` when the tick has been cleared (i.e., is uninitialized). This should only occur on a call to `decreaseStakedLiquidity()` when the following are true:
- The entire liquidity in the position is decreased.
- The liquidity is the only liquidity in the given tick ranges.

## Spearbit
Fixed as recommended in commit `171a82f2`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | Jeiwan, Alex The Entreprenerd, Optimum, D-Nice |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf

### Keywords for Search

`vulnerability`

