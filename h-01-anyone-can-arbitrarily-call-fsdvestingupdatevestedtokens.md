---
# Core Classification
protocol: FairSide
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 980
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-fairside-contest
source_link: https://code4rena.com/reports/2021-11-fairside
github_link: https://github.com/code-423n4/2021-11-fairside-findings/issues/101

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - access_control

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - rfa
  - cmichel
  - leastwood
  - hickuphh3
  - WatchPug
---

## Vulnerability Title

[H-01] Anyone Can Arbitrarily Call FSDVesting.updateVestedTokens()

### Overview


This bug report concerns the `updateVestedTokens()` function in the `FSDVesting.sol` contract. This function is intended to be called by the `FSD.sol` contract when updating a user's vested token amount. However, a check is not performed to make sure that the call originates from a trusted source, meaning that anyone can call this function and add any amount to the vested contract. 

There are two main reasons why the beneficiary or an attacker would want to call this function: to increase the vested amount such that `calculateVestingClaim()` allows them to withdraw their entire vested amount without waiting the entire duration, or to block withdrawals from other vested contracts by preventing successful calls to `claimVestedTokens()`.

The bug was identified through manual code review and discussions with the development team. The recommended mitigation step is to ensure that the `updateVestedTokens()` function is only callable from the `FSD.sol` contract by implementing an `onlyFSD` role.

### Original Finding Content

## Handle

leastwood


## Vulnerability details

## Impact

The `updateVestedTokens()` function is intended to be called by the `FSD.sol` contract when updating a user's vested token amount. A check is performed to ensure that `_user == beneficiary`, however, as `_user` is a user controlled argument, it is possible to spoof calls to `updateVestedTokens()` such that anyone can arbitrarily add any amount to the vested contract. Additionally, there is no check to ensure that the call originated from a trusted/whitelisted source.

There are two main reasons as to why the beneficiary or an attacker would want to call this function:
- To increase the vested amount such that `calculateVestingClaim()` allows them to withdraw their entire vested amount without waiting the entire duration.
- An attacker wishes to block withdrawals from other vested contracts by preventing successful calls to `claimVestedTokens()` by the beneficiary account. This can be done by increasing the vested amount such that `safeTransfer()` calls fail due to insufficient token balance within the contract.

## Proof of Concept

https://github.com/code-423n4/2021-11-fairside/blob/main/contracts/token/FSDVesting.sol#L147-L161
https://github.com/code-423n4/2021-11-fairside/blob/main/contracts/token/FSDVesting.sol#L100-L115
https://github.com/code-423n4/2021-11-fairside/blob/main/contracts/token/FSDVesting.sol#L125
https://github.com/code-423n4/2021-11-fairside/blob/main/contracts/token/FSDVesting.sol#L134

## Tools Used

Manual code review.
Discussions with dev.

## Recommended Mitigation Steps

Ensure that the `updateVestedTokens()` function is only callable from the `FSD.sol` contract. This can be done by implementing an `onlyFSD` role.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | FairSide |
| Report Date | N/A |
| Finders | rfa, cmichel, leastwood, hickuphh3, WatchPug, hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-fairside
- **GitHub**: https://github.com/code-423n4/2021-11-fairside-findings/issues/101
- **Contest**: https://code4rena.com/contests/2021-11-fairside-contest

### Keywords for Search

`Access Control`

