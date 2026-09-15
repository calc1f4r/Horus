---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26054
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/392

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
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - xuwinnie
---

## Vulnerability Title

[H-20] A user can bypass bandwidth limit by repeatedly "balancing" the pool

### Overview


This bug report is about a technique called "balancing" which can be used to redistribute bandwidths in a pool. This technique can be exploited to bypass the maximum limit of bandwidths that can be withdrawn from a pool. As an example, a user can repeatedly add and remove a small amount of liquidity in order to increase the bandwidth of a specific chain or token, thus bypassing the maximum limit. This technique can be used to acquire nearly all of the available liquidity in the pool, leading to unbounded LP loss.

To mitigate this issue, two steps have been recommended. Firstly, liquidity should always be distributed or taken proportionally to weight during ulyssesAddLP or ulyssesAddLP. Secondly, when swapping A for B, the bandwidth of A in the B pool should be reduced while the bandwidth of B in the A pool should be added.

The findings of the audit have been recognized and will not be rectified due to the upcoming migration of this section to Balancer Stable Pools.

### Original Finding Content


The goal with bandwidths is to have a maximum that can be withdrawn (swapped) from a pool. In case a specific chain (or token from a chain) is exploited, then it only can partially affect these pools. However, the maximum limit can be bypassed by repeatedly "balancing" the pool to increase bandwidth for the exploited chain.

### Introducing "Balancing": A Technique for Redistributing Bandwidth

During `ulyssesAddLP` or `ulyssesAddLP`, liquidity is first distributed or taken proportionally to `diff` (if any exists) and then distributed or taken proportionally to `weight`. Suppose integer `t` is far smaller than `diff` (since the action itself can also change `diff`), after repeatedly adding `t LP`, removing `t LP`, adding `t LP`, removing `t LP`, etc., the pool will finally reach another stable state where the ratio of `diff` to `weight` is a constant among destinations. This implies that the `currentBandwidth` will be proportional to `weight`.

### Proof of Concept

Suppose Avalanche is down. Unluckily, Alice holds 100 ava-hETH. They want to swap ava-hETH for bnb-hETH.

Let's take a look at bnb-hETH pool. Suppose weights are mainnet:4, Avalanche:3 and Linea:2. Total supply is 90. Target bandwidths are mainnet:40, Avalanche:30 and Linea:20. Current bandwidths are mainnet:30, Avalanche:2 (few left) and Linea:22.

Ideally Alice should only be able to swap for 2 bnb-hETH. However, they swap for 0.1 bnb-hETH first. Then they use the 0.1 bnb-hETH to "balance" the pool (as mentioned above). Current bandwidths will become mainnet:24, Avalanche:18 and Linea:12. Then, Alice swaps for 14 bnb-hETH and "balance" the pool again. By repeating the process, they can acquire nearly all of the available liquidity in pool and `LP` loss will be unbounded.

### Recommended Mitigation Steps

1.  During `ulyssesAddLP` or `ulyssesAddLP`, always distribute or take liquidity proportionally to weight.
2.  When swapping A for B, reduce the bandwidth of A in the B pool (as is currently done) while adding bandwidth of B in the A pool (instead of distributing them among all bandwidths).

### Assessed type

Context

**[0xLightt (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/392#issuecomment-1631674929)**

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/392#issuecomment-1655653646):**
 > We recognize the audit's findings on Ulysses AMM. These will not be rectified due to the upcoming migration of this section to Balancer Stable Pools.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | xuwinnie |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/392
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

