---
# Core Classification
protocol: Salty.IO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29616
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Damilola Edwards
  - Richie Humphrey
---

## Vulnerability Title

Collateral contract deployment results in permanent loss of rewards

### Overview


This bug report describes a problem with the authentication process in a protocol called Salty.IO. This issue affects users who provide liquidity to the collateral pool, as they are not able to earn rewards and any profits from arbitrage are lost. The problem is caused by the fact that the Liquidity contract, which is responsible for distributing rewards, does not properly reference the Collateral contract. This means that rewards intended for the collateral pool are misdirected and cannot be claimed by users. The report recommends combining the Liquidity and Collateral contracts in the short term and creating a clear specification for all contracts in the long term.

### Original Finding Content

## Diﬃculty: Low

## Type: Authentication

## Description
Anyone who provides liquidity to the collateral pool (also known as the WETH/WBTC pool) will not earn rewards, and any arbitrage proﬁts allocated to the pool will be permanently lost.

The Collateral contract is deployed separately from the Liquidity contract; however, only liquidity in the Liquidity contract can claim rewards. This arises because the Liquidity contract is the sole contract seeded with SALT rewards.

As shown in figure 7.1, the `performUpkeep` function, which is responsible for sending rewards to the relevant contract, references only `stakingRewards`, which is conﬁgured as the address of the Liquidity contract; it completely overlooks the Collateral contract. This means that rewards intended for the collateral pool are misdirected, as they should properly be sent to the Collateral contract.

```solidity
// Transfer a percent (default 1% per day) of the currently held rewards to
// the specified StakingRewards pools.
// The percentage to transfer is interpolated from how long it's been since
// the last performUpkeep().
function performUpkeep( uint256 timeSinceLastUpkeep, bool isStaking ) public
…
```

```solidity
// Add the rewards so that they can later be claimed by the users
// proportional to their share of the StakingRewards derived contract( Staking,
// Liquidity or Collateral)
stakingRewards.addSALTRewards( addedRewards );
}
```

*Figure 7.1: In the above code, `stakingRewards` refers to the Liquidity contract.*  
*(src/rewards/RewardsEmitter.sol#L80-L138)*

If an actual collateral pool liquidity holder calls `claimAllRewards` on the Collateral contract, then it will revert because there are no rewards in the contract. If the user calls `claimAllRewards` on the Liquidity contract, it will revert because the user has no liquidity as far as the Liquidity contract is concerned.

## Exploit Scenario
The protocol is deployed, and Alice adds liquidity to the collateral pool. Over time, the pool accumulates arbitrage fees. Alice is unable to claim any rewards, and the rewards that are sent to the pool are permanently lost.

## Recommendations
- **Short term:** Combine the Liquidity and Collateral contracts into one.
- **Long term:** Create a speciﬁcation for all contracts with clear deﬁnitions and expectations for each process.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Salty.IO |
| Report Date | N/A |
| Finders | Damilola Edwards, Richie Humphrey |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf

### Keywords for Search

`vulnerability`

