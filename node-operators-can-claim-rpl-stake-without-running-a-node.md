---
# Core Classification
protocol: Rocketpool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19515
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/rocket-pool/rocket-pool-5-lower-eth-bond/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/rocket-pool/rocket-pool-5-lower-eth-bond/review.pdf
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
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Node Operators Can Claim RPL Stake Without Running A Node

### Overview


This bug report is about a Node Operator who can submit a full withdrawal of their node, receive the ETH from their withdrawal and continue to receive RPL from their staked RPL. This is possible by initiating the counter for a user to distribute the funds via, beginUserDistribute() and claiming the withdrawn ETH via refund() without calling finalise(). This means that the Node Operator has managed to obtain their owed ETH without running the _finalise() function and their RPL stake remains in the system and they continue to receive RPL staking rewards. 

The authors have acknowledged this issue and the rewards generation process is planned to be upgraded before the launch of the contract upgrade. This upgraded process will exclude validators that have exited the beacon chain. A governance thread has been started to discuss the rewards generation process. 

To mitigage this issue, some solutions have been proposed such as including decrementNodeStakingMinipoolCount() as part of a final distribution, requiring a Node Operator to mark the minipool as finalised after refunding a certain amount of ETH, moving the ethMatched modification to within decrementNodeStakingMinipoolCount() and handling non-finalised minipools in the off-chain calculations of staking rewards.

### Original Finding Content

## Description

A Node Operator can submit a full withdrawal of their node, receive the ETH from their withdrawal, and continue to receive RPL from their staked RPL.

To achieve this state, a Node Operator submits a full withdrawal. They initiate the counter for a user to distribute the funds via `beginUserDistribute()`. They then distribute funds via another user after the user distribute timeout has elapsed. Finally, they claim the withdrawn ETH via `refund()` without calling `finalise()`. 

In this series of events, the Node Operator has managed to obtain their owed ETH without running the `_finalise()` function.

The Node Operator’s RPL stake remains in the system, and they continue to receive RPL staking rewards. If the minipool has a large `nodeFee` that skews the average, they receive a larger share of the tip fee portion distributed to them. The actual reward calculation occurs off-chain, so the actual staking rewards are not verified in this review. However, it appears that staking rewards are included for non-finalised minipools.

## Recommendations

There are a number of ways that this issue might be handled. The resolution should account for this scenario when calculating RPL staking rewards and smoothing pool rewards for Node Operators who refuse to finalise. Some examples of possible mitigations are:

- Include `decrementNodeStakingMinipoolCount()` as part of a final distribution to allow network users to modify this counter if the operator refuses to.
- Require a Node Operator to mark the minipool as finalised after refunding over a specific amount of ETH.
- Move the `ethMatched` modification to within `decrementNodeStakingMinipoolCount()`.
- Handle non-finalised minipools in the off-chain calculations of staking rewards.

## Resolution

The authors have acknowledged this issue. The rewards generation process is planned to be upgraded before the launch of the contract upgrade. The upgraded process will exclude validators that have exited the beacon chain. A governance thread has been started to discuss the rewards generation process.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Rocketpool |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/rocket-pool/rocket-pool-5-lower-eth-bond/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/rocket-pool/rocket-pool-5-lower-eth-bond/review.pdf

### Keywords for Search

`vulnerability`

