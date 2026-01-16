---
# Core Classification
protocol: Telcoin
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3637
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/25
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/45

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - front-running

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - cccz
  - hickuphh3
  - yixxas
---

## Vulnerability Title

M-5: `slash()` can be frontrunned to avoid the penalty imposed on them

### Overview


This bug report is about a vulnerability in the `slash()` function of the StakingModule.sol contract. This function is used to take funds away from a user when they misbehave. However, a malicious user can frontrun this operation or the `pause()` function and call `fullClaimAndExit()` to fully exit before the penalty can affect them. This means that the slashing mechanism implemented can be bypassed by malicious users. The bug was found by yixxas, hickuphh3, and cccz and was confirmed by manual review. It is recommended that the sponsors explore alternatives to this slashing mechanism as it can be easily bypassed, especially by sophisticated users who are likely the ones who will be getting slashed. A discussion around the issue can be found in the pull request #21 on the telcoin-staking repository.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/45 

## Found by 
yixxas, hickuphh3, cccz

## Summary
I believe `slash()` is used to take funds away from a user when they misbehave. However, a malicious user can frontrun this operation or the `pause()` function and call `fullClaimAndExit()` to fully exit before the penalty can affect them. 

## Vulnerability Detail
Malicious users who have intentionally committed some offenses that would lead to getting slashed can listen to the mempool and frontrun the `slash()` or `pause()` function call by the protocol to protect all his assets before slashing can happen.

## Impact
Slashing mechanism implemented can be bypassed by malicious user.

## Code Snippet
https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/StakingModule.sol#L403-L406

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/StakingModule.sol#L202-L207

## Tool used

Manual Review

## Recommendation
I implore the sponsors to explore alternatives to this slashing mechanism as they can be easily bypassed, especially so by sophisticated users who presumably are the ones who will be getting slashed.

## Discussion

**amshirif**

https://github.com/telcoin/telcoin-staking/pull/21

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin |
| Report Date | N/A |
| Finders | cccz, hickuphh3, yixxas |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/45
- **Contest**: https://app.sherlock.xyz/audits/contests/25

### Keywords for Search

`Front-Running`

