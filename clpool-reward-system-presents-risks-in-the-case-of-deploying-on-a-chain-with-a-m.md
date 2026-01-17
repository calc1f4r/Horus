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
solodit_id: 29639
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review-Nov23.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

CLPool reward system presents risks in the case of deploying on a chain with a Mempool

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
CLPool.sol#L708-L709

## Description
The rewards math on CLPool is based on the idea that rewards are dripped each second exclusively to the active liquidity. A drip of rewards increases the `rewardsGrowthGlobal` crediting said growth to all active liquidity. The way this is done, in a swap, is by calling `_updateRewardsGrowthGlobal` on crossing ticks. See CLPool.sol#L708-L709:

```solidity
_updateRewardsGrowthGlobal(); /// @audit Called every time crossing happens
```

It's worth noting that this accrual process is based on a delta time, meaning that it ignores changes that happen within the same block (see CLPool.sol#L853-L857):

```solidity
uint32 timestamp = _blockTimestamp();
uint256 _lastUpdated = lastUpdated;
uint256 timeDelta = timestamp - _lastUpdated;
if (timeDelta != 0) {
    // ...
}
```

In a mempool system, nothing happens between blocks: all of the action happens inside of the block. Since accrual can be triggered at the start of the block, the most optimal LP strategy would be to claim said rewards, then unstake the liquidity and JIT said liquidity to end users as a means to gain swap fees.

### Liquidity Provision Mempool Risks
In the case of a deployment on a chain with a mempool, bundling would allow Active LP to:
- Claim rewards until now.
- Unstake.
- JIT LP to gain swap fees.
- Restake at the end of the block, to farm the new drip of rewards.

Ultimately, this is a challenge in balancing effective volume against time spent in the pool, with the main issue being that, since actions/volume within a block are not counted, said gaming could be performed. This will be negative for Passive LPs but neutral for end users.

An interesting edge case of the above, meant to allow this on non-mempool systems could be “wrapped swaps,” which would ensure a swap is MEVd back and forth as a way for the LP to ensure that their liquidity remains in the active range. This may be positive for end users and indifferent to passive LPs.

## Recommendation
Monitor the behavior of Active vs Passive LPs and users and determine if a Volume-Based reward system would be fairer versus a time-based system which may be gameable, but gaming it may be too expensive.

## Velodrome
The issue has been acknowledged and no further action will take place. Monitoring of LP behavior will take place if a mempool exists.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

