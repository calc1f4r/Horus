---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5888
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/32

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3.000389490001792
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - clems4ever
---

## Vulnerability Title

[H-01] Any user being the first to claim rewards from GiantMevAndFeesPool can unexepectedly collect them all

### Overview


This bug report is about an issue in the code for the 2022-11-stakehouse project. The code can be found on GitHub at the specified links. The vulnerability allows any user to claim rewards from the GiantMevAndFeesPool, regardless of whether or not they participated in generating those rewards. The proof of concept can be found in the given gist, and the recommended mitigation steps are to rework the way the variables `accumulatedETHPerLPShare` and `claimed` are used. This issue is likely caused by an interaction between the two variables, which may have other bugs as well.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/SyndicateRewardsProcessor.sol#L85
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/SyndicateRewardsProcessor.sol#L61
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L203


## Vulnerability details

## Impact
Any user being the first to claim rewards from GiantMevAndFeesPool, can get all the previously generated rewards whatever the amount and even if he did not participate to generate those rewards...

## Proof of Concept

https://gist.github.com/clems4ever/c9fe06ce454ff6c4124f4bd29d3598de

Copy paste it in the test suite and run it.

## Tools Used

forge test

## Recommended Mitigation Steps

Rework the way `accumulatedETHPerLPShare` and `claimed` is used. There are multiple bugs due to the interaction between those variables as you will see in my other reports.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3.000389490001792/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | clems4ever |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/32
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Business Logic`

