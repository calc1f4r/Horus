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
solodit_id: 21385
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
github_link: none

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
  - dexes
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Xiaoming90
  - 0xNazgul
  - Jonatas Martins
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Bribe and fee token emissions can be gamed by users

### Overview


This bug report is about a vulnerability in the Voter.sol contract that could allow users to gain an unfair advantage in the reward distribution contracts. The vulnerability is that users can vote or reset their vote once per epoch, and their votes will persist across epochs. The poke() function can be called by any user to update the target user's decayed veNFT token balance. However, the poke() function is not hooked into any of the reward distribution contracts, meaning users are incentivized to vote as soon as they create their lock and avoid re-voting in subsequent epochs. This could allow them to earn trading fees and bribes even after their lock has expired.

The recommendation is to re-design the FeesVotingReward and BribeVotingRewards contracts to decay user deposits automatically. Velodrome proposed a solution to incentivize the poking of tokenIds that have been passively voting for too long. The parameters of this solution will be mutable and can be adjusted to reduce the cost of incentivization. Spearbit acknowledged that this solution is inefficient and does not scale with users.

### Original Finding Content

## Security Assessment Report

## Severity: Medium Risk

### Context
`Voter.sol#L154-L224`

### Description
A user may vote or reset their vote once per epoch. Votes persist across epochs, and once a user has distributed their votes among their chosen pools, the `poke()` function may be called by any user to update the target user's decayed veNFT token balance. However, the `poke()` function is not hooked into any of the reward distribution contracts.

As a result, a user is incentivized to vote as soon as they create their lock and avoid re-voting in subsequent epochs. The amount deposited via `Reward._deposit()` does not decay linearly as defined under veToken mechanics. Therefore, users could continue to earn trading fees and bribes even after their lock has expired. Simultaneously, users can call `poke()` on other users to lower their voting weight and maximize their own earnings.

### Recommendation
Re-designing the `FeesVotingReward` and `BribeVotingRewards` contracts may be worthwhile to decay user deposits automatically.

### Velodrome
Given the numerous assumptions surrounding the severity of the attack (i.e., how likely a user would wish to execute this, considering competing incentives around maximizing returns and the risk that they can be poked at any time), we have elected to pursue a solution that incentivizes the poking of token IDs that have been passively voting for too long.

The proposed mechanism will look something like this: on the last day of every epoch, any token ID that exceeds a certain value and has been passively voting for an extended period will be incentivized to be poked. This approach will reduce that NFT's contribution and discourage long-term passive behavior as well as abuse. The parameters ("some value" and "some time") will be adjustable to optimize the cost of incentivization. Initial ideas for these thresholds include poking any NFT worth more than `1,000 VELO` that has passively voted for `4 weeks`. We will assess the severity of the issue in practice and make adjustments as necessary.

### Spearbit
Acknowledged. While it is true that users are incentivized to poke other users who are passively voting on pools for too long, this mechanism remains inefficient and does not scale effectively with the number of users.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | Xiaoming90, 0xNazgul, Jonatas Martins, 0xLeastwood, Jonah1005, Alex the Entreprenerd |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

