---
# Core Classification
protocol: Locke
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6995
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Locke-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Locke-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Mukesh Jaiswal
  - Eric Wang
  - Harikrishnan Mulackal
---

## Vulnerability Title

User can lose their reward due truncated division

### Overview


This bug report outlines a high risk issue in the Locke.sol#L321 code. The bug can cause users to lose rewards in an update round when any of the following conditions are true: 1.RewardToken.decimals() is too low, 2. Reward is updated too frequently, 3.StreamDuration is too large, or 4.TotalVirtualBalance is too large (e.g., stake near the end of stream). This bug is especially likely to occur when the first condition is true. 

An example scenario is given to demonstrate the bug. In this example, rewardToken.decimals() is 6, depositToken.decimals() is 18, rewardTokenAmount is 1K * 10**6, streamDuration is 1209600 (two weeks), totalVirtualBalance is streamDuration *depositTokenAmount /timeRemaining where depositToken- Amount = 100K 10**18 andtimeRemaining =streamDuration (a user stakes 100K at the beginning of the stream) lastApplicableTime() - lastUpdate = 100 (about 7 block-time). In this scenario, rewards = 100 * 1000 * 10**6 * 10**18 / 1209600 / (1209600 * 100000 * 10**18 / 1209600) which causes a truncation of the reward and the user loses their reward. 

It is important to note this bug and its potential consequences, as it can cause users to lose rewards.

### Original Finding Content

## Severity: High Risk

## Context
Locke.sol#L321

## Description
The truncated division can cause users to lose rewards in this update round, which may happen when any of the following conditions are true:

1. `RewardToken.decimals()` is too low.
2. Reward is updated too frequently.
3. `StreamDuration` is too large.
4. `TotalVirtualBalance` is too large (e.g., stake near the end of stream).

This could potentially happen especially when the first case is true. Consider the following scenario:

- `rewardToken.decimals()` = 6.
- `depositToken.decimals()` can be any (assume it’s 18).
- `rewardTokenAmount` = 1K * 10**6.
- `streamDuration` = 1209600 (two weeks).
- `totalVirtualBalance` = `streamDuration * depositTokenAmount / timeRemaining` where `depositTokenAmount` = 100K * 10**18 and `timeRemaining` = `streamDuration` (a user stakes 100K at the beginning of the stream).

`lastApplicableTime() - lastUpdate = 100` (about 7 block-time).

Then rewards = 

```
100 * 1000 * 10**6 * 10**18 / 1209600 / (1209600 * 100000 * 10**18 / 1209600)
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Locke |
| Report Date | N/A |
| Finders | Mukesh Jaiswal, Eric Wang, Harikrishnan Mulackal |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Locke-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Locke-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

