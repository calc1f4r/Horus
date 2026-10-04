---
# Core Classification
protocol: Behodler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1375
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-behodler-contest
source_link: https://code4rena.com/reports/2022-01-behodler
github_link: https://github.com/code-423n4/2022-01-behodler-findings/issues/146

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
  - cross_chain
  - services
  - cdp
  - dexes
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Ryyy
  - CertoraInc
---

## Vulnerability Title

[M-10] user won’t be able to get his rewards in case of staking with amount = 0

### Overview


A bug was reported in the Limbo.sol smart contract's `stake()` function. If a user has a pending reward and calls the `stake` function with `amount = 0`, they will not be able to collect their reward. This is because the reward calculation is only done if the staked amount is greater than 0. As a result, the reward debt will be updated without the user being able to collect their reward.

### Original Finding Content

## Handle

CertoraInc


## Vulnerability details

## Limbo.sol (`stake()` function)
if a user has a pending reward and he call the `stake` function with `amount = 0`, he won't be able to get his reward (he won't get the reward, and the reward debt will cover the reward)

that's happening because the reward calculation is done only if the staked amount (given as a parameter) is greater than 0, and it updates the reward debt also if the amount is 0, so the reward debt will be updated without the user will be able to get his reward

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Behodler |
| Report Date | N/A |
| Finders | Ryyy, CertoraInc |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-behodler
- **GitHub**: https://github.com/code-423n4/2022-01-behodler-findings/issues/146
- **Contest**: https://code4rena.com/contests/2022-01-behodler-contest

### Keywords for Search

`vulnerability`

