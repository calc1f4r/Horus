---
# Core Classification
protocol: infiniFi contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55068
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - R0bert
  - Slowfi
  - Jonatas Martins
  - Noah Marconi
---

## Vulnerability Title

Reward multiplier skew in LockingController causes disproportionate reward allocation over time

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
YieldSharing.sol#L143-L152

## Description
In the LockingController contract, a static `rewardMultiplier` is used to enhance the reward weight of locked tokens relative to staked tokens, incentivizing token locking. While this mechanism intends to balance participation between staking and locking, its static implementation introduces a significant skew in the reward distribution over time. As rewards are periodically distributed with every `accrue` call, the fixed multiplier fails to adjust to the changing proportions of staked and locked tokens, disproportionately favoring locked positions (due to the higher multiplier). 

Over time, this results in an escalating concentration of rewards among locked token holders, which undermines the fairness and long-term sustainability of the protocol's incentive framework. The issue stems from the interplay between the unchanging `rewardMultiplier` (e.g., 1.2x) and the dynamic total reward weight of the system. Rewards are distributed according to the weighted contributions of staked and locked tokens, with locked tokens consistently receiving an amplified share due to the multiplier. 

Over successive reward cycles, this effect compounds, enabling locked positions to accrue a disproportionately large portion of rewards, even if the quantity of locked tokens remains constant. Consequently, staked tokens experience a diminishing share of rewards, which discourages staking participation and disrupts the intended equilibrium between the two mechanisms.

## Example
1. 10,000 iUSDC in the StakedToken contract. Staked tokens multiplier = 1x.
2. 10,000 iUSDC locked in the LockingController. Locked tokens multiplier = 1.2x.
3. 30,000 iUSDC are distributed as yield through the `accrue` call.
4. Due to the higher multiplier, LockingController receives 55% of the yield distributed while the StakedToken contract receives 45%.
5. However, after the addition of these rewards, the next `accrue` call will allocate 42% of the yield to the StakedToken and 48% to the LockingController.
6. Locked token holders progressively capture a larger share of rewards, diminishing returns for staked token holders and skewing the distribution in favor of locking.

The reward rate should fairly reflect user actions or, which is the same, deposits into and withdrawals from the StakedToken or LockingController contracts. These actions represent the users' intentional allocation of tokens and the reward system should adjust accordingly to maintain equity. Instead, the static multiplier distorts this balance, allowing locked token holders to accrue disproportionate rewards without further effort, while penalizing staked token holders. This violates the fairness principle that reward distribution should be driven solely by user-initiated changes in the system.

## Recommendation
To mitigate this skew and restore fairness to the reward distribution, do not count the distributed rewards when calculating `stakedReceiptTokens` and `lockingReceiptTokens`. These variables should only hold user-provided receipt tokens and not earned yield.

## infiniFi
Acknowledged as this is by design. All users are auto-compounding; the result would be the same if we distributed iUSD rewards and everyone compounded into their own position. A growing locked tranche is also allowing more allocation to illiquid farms, which increase the yield for everyone.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | infiniFi contracts |
| Report Date | N/A |
| Finders | R0bert, Slowfi, Jonatas Martins, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

