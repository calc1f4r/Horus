---
# Core Classification
protocol: Timeswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24910
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-timeswap
source_link: https://code4rena.com/reports/2023-01-timeswap
github_link: https://github.com/code-423n4/2023-01-timeswap-findings/issues/158

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
  - yield
  - services
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0Kage
---

## Vulnerability Title

[M-07] `Mint` function does not update `LiquidityPosition` state of caller before minting LP tokens. This

### Overview


This bug report is about a potential issue in the code of the 2023-01-timeswap project. The code in question is located in the Pool.sol and LiquidityPosition.sol files. The issue is that when a liquidity provider (LP) mints V2 Pool tokens, the code fails to update the LP's state, which can lead to incorrect calculations of long0/long1 and short fees of LP holders. This could result in the LP receiving lower fees than they should, leading to a potential loss of fees.

The bug was confirmed by vhawk19 (Timeswap). To mitigate the issue, the code should be updated to update the liquidity position state right before minting. This can be done by adding a line of code after line 302 of Pool.sol, which updates the LiquidityPosition with the pool's long0FeeGrowth, long1FeeGrowth, and shortFeeGrowth.

### Original Finding Content


<https://github.com/code-423n4/2023-01-timeswap/blob/ef4c84fb8535aad8abd6b67cc45d994337ec4514/packages/v2-pool/src/structs/Pool.sol#L302> 

<https://github.com/code-423n4/2023-01-timeswap/blob/ef4c84fb8535aad8abd6b67cc45d994337ec4514/packages/v2-pool/src/structs/LiquidityPosition.sol#L60>

### Impact

When a LP mints V2 Pool tokens, `mint` function in [PoolLibrary](https://github.com/code-423n4/2023-01-timeswap/blob/ef4c84fb8535aad8abd6b67cc45d994337ec4514/packages/v2-pool/src/structs/Pool.sol#L302) gets called. Inside this function `updateDurationWeightBeforeMaturity` updates global `short`, `long0` and `long1` fee growth.

Change in global fee growth necessitates an update to `LiquidityPosition` state of caller (specifically updating fees & fee growth rates) when there are state changes made to that position (in this case, increasing liquidity). This principle is followed in functions such as `burn`, `transferLiquidity`, `transferFees`. However when calling `mint`, this update is missing. As a result, `growth` & `fee` levels in liquidity position of caller are inconsistent with global fee growth rates.

Inconsistent state leads to incorrect calculations of long0/long1 and short fees of LP holders which in turn can lead to loss of fees. Since this impacts actual rewards for users, I've marked it as MEDIUM risk.

### Proof of Concept

Let's say, Bob has following sequence of events

*   MINT at T0: Bob is a LP who mints N pool tokens at T0

*   MINT at T1: Bob mints another M pool tokens at T1. At this point, had the protocol correctly updated fees before minting new pool tokens, Bob's fees & growth rate would be a function of current liquidity (N), global updated short fee growth rate at t1 (s_t1) and Bob's previous growth rate at t\_0 (b_t0)

*   BURN at T2: Bob burns N + M tokens at T2. At this point, Bob's fees should be a function of previous liquidity (N+M), global short fee growth rate (s_t2) and Bob's previous growth rate at t\_1(b_t1) -> since this update never happened, Bob's previous growth rate is wrongly referenced b_t0 instead of b_t1.

Bob could collect a lower fees because of this state inconsistency.

### Recommended Mitigation Steps

Update the liquidity position state right before minting.

After [line 302 of Pool.sol](https://github.com/code-423n4/2023-01-timeswap/blob/ef4c84fb8535aad8abd6b67cc45d994337ec4514/packages/v2-pool/src/structs/Pool.sol#L302), update the LiquidityPosition by adding

      liquidityPosition.update(pool.long0FeeGrowth, pool.long1FeeGrowth, pool.shortFeeGrowth);

**[vhawk19 (Timeswap) confirmed](https://github.com/code-423n4/2023-01-timeswap-findings/issues/158)**


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Timeswap |
| Report Date | N/A |
| Finders | 0Kage |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-timeswap
- **GitHub**: https://github.com/code-423n4/2023-01-timeswap-findings/issues/158
- **Contest**: https://code4rena.com/reports/2023-01-timeswap

### Keywords for Search

`vulnerability`

