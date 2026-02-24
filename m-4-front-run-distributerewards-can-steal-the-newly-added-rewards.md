---
# Core Classification
protocol: Merit Circle
chain: everychain
category: economic
vulnerability_type: share_inflation

# Attack Vector Details
attack_type: share_inflation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3473
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/9
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-merit-circle-judging/issues/106

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - share_inflation
  - front-running

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - payments

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - WATCHPUG
  - hyh
  - hickuphh3
---

## Vulnerability Title

M-4: Front run `distributeRewards()` can steal the newly added rewards

### Overview


This bug report is about a vulnerability in the Merit Circle Judgement protocol, which allows an attacker to steal newly added rewards. The attack vector is triggered by a surge of pointsPerShare every time the `distributeRewards()` function is called. This enables the attacker to deposit a large portion of the pool, trigger the surge, and exit after stealing the major part of the newly added rewards. The vulnerability was discovered by WATCHPUG, hickuphh3, and hyh, who used manual review as the tool. A recommendation is made to consider using a rewardRate-based gradual release model to prevent the attack. The discussion section includes a suggestion to raise the `MIN_LOCK_DURATION` from 10 minutes to 1 day, as well as a link to a pull request from this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-merit-circle-judging/issues/106 

## Found by 
WATCHPUG, hickuphh3, hyh

## Summary

A surge of pointsPerShare on each `distributeRewards()` call can be used by the attacker to steal part of the newly added rewards.

## Vulnerability Detail

Every time the `distributeRewards()` gets called, there will be a surge of `pointsPerShare` for the existing stakeholders.

This enables a well-known attack vector, in which the attacker will deposit a huge amount of underlying tokens and take a large portion of the pool, then trigger the surge, and exit right after.

## Impact

While the existence of the `MIN_LOCK_DURATION` prevented the usage of flashloan, it's still possible for the attackers with sufficient funds or can acquire sufficient funds in other ways.

In which case, the attack is quite practical and effectively steal the major part of the newly added rewards

## Code Snippet

https://github.com/sherlock-audit/2022-10-merit-circle/blob/main/merit-liquidity-mining/contracts/base/BasePool.sol#L95-L98

https://github.com/sherlock-audit/2022-10-merit-circle/blob/main/merit-liquidity-mining/contracts/base/AbstractRewards.sol#L89-L99

## Tool used

Manual Review

## Recommendation

Consider using a `rewardRate`-based gradual release model, pioneered by Synthetix's StakingRewards contract.

See: https://github.com/Synthetixio/synthetix/blob/develop/contracts/StakingRewards.sol#L113-L132

## Discussion

**federava**

Raising the MIN_LOCK_DURATION from 10 minutes to 1 day.

**federava**

[PR](https://github.com/Merit-Circle/merit-liquidity-mining/pull/14) from this issue

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Merit Circle |
| Report Date | N/A |
| Finders | WATCHPUG, hyh, hickuphh3 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-merit-circle-judging/issues/106
- **Contest**: https://app.sherlock.xyz/audits/contests/9

### Keywords for Search

`Share Inflation, Front-Running`

