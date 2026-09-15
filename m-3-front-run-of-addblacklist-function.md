---
# Core Classification
protocol: Telcoin Update
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6669
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/49
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-telcoin-judging/issues/43

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - front-running

protocol_categories:
  - dexes
  - cdp
  - services
  - liquidity_manager
  - payments

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Inspex
  - gmx
  - 0xAgro
  - J4de
---

## Vulnerability Title

M-3: Front Run of addBlackList() function

### Overview


This bug report is about a vulnerability in the addBlackList() function of the Stablecoin.sol contract. The vulnerability is called "front running" which is when a malicious user is able to send a transaction with a higher gas price to prevent their funds from being removed by the removeBlackFunds() function. The code snippet for this can be found at the link provided. The bug was found manually by Inspex, J4de, 0xAgro, and gmx. The recommendation is to use the same mechanism as in StakingModule.sol to prevent users from withdrawing their funds if they are blacklisted, so front running won't be useful.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-telcoin-judging/issues/43 

## Found by 
Inspex, J4de, 0xAgro, gmx

## Summary

**Front Run of addBlackList() function** 

## Vulnerability Detail

Front running can be done either by sending a tx with a higher gas price (usually tx are ordered in a block by the gas price / total fee), or by paying an additional fee to the validator if they manage to run their tx without reverting (i.e. by sending additional ETH to block.coinbase, hoping validator will notice it).

## Impact

Malicious user could listen the mempool in order to check if he sees a tx of blacklisting for his address , if it happens he could front run this tx by sending a tx with higher gas fee to transfer his funds to prevent them to be removed by removeBlackFunds() function

## Code Snippet

https://github.com/sherlock-audit/2023-02-telcoin/blob/main/telcoin-audit/contracts/stablecoin/Stablecoin.sol#L159

## Tool used

Manual Review

## Recommendation
Use the same mechanism as in StakingModule.sol to prevent user from withdrawing their funds if blacklisted so that front running won't be useful

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin Update |
| Report Date | N/A |
| Finders | Inspex, gmx, 0xAgro, J4de |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-telcoin-judging/issues/43
- **Contest**: https://app.sherlock.xyz/audits/contests/49

### Keywords for Search

`Front-Running`

