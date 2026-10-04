---
# Core Classification
protocol: Telcoin
chain: everychain
category: economic
vulnerability_type: flash_loan

# Attack Vector Details
attack_type: flash_loan
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3632
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/25
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/83

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - flash_loan
  - checkpoint

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WATCHPUG
---

## Vulnerability Title

H-1: Flashloan `TEL` tokens to stake and exit in the same block can fake a huge amount of stake with minimal material cost

### Overview


This bug report is about an issue found in the Telcoin Staking Module. It was found by WATCHPUG and is known as Issue H-1. It is related to a vulnerability in the Checkpoints#getAtBlock() function. This vulnerability allows a malicious user to fake their stake and gain high rewards with minimal material cost using a flashloan. The code snippets linked in the report can be used to understand the vulnerability in more detail. The recommendation is to require the exit to be at least 1 block later than the blocknumber of the original stake. There is also a discussion about this issue, which can be found in the link provided.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/83 

## Found by 
WATCHPUG

## Summary

`Checkpoints#getAtBlock()` can be faked with falshloan as it may return the value of the first checkpoint in the same block.

## Vulnerability Detail

`Checkpoints#getAtBlock()` will return the value on check point #0 when there are two check points in the same block (#0 and #1).

Therefore, one can take a falshloan of TEL tokens to stake and exit in the same block, which will create two checkpoints.

## Impact

Malicious user can fake their stake to gain a high percentage rewards with falshloan and avoid slashing.

## Code Snippet

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/StakingModule.sol#L147-L149

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/StakingModule.sol#L403-L406

## Tool used

Manual Review

## Recommendation

Consider requiring the `exit` to be at least 1 block later than the blocknumber of the original stake.

## Discussion

**amshirif**

https://github.com/telcoin/telcoin-staking/pull/9

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin |
| Report Date | N/A |
| Finders | WATCHPUG |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/83
- **Contest**: https://app.sherlock.xyz/audits/contests/25

### Keywords for Search

`Flash Loan, CheckPoint`

