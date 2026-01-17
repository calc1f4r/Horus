---
# Core Classification
protocol: Telcoin
chain: everychain
category: dos
vulnerability_type: denial-of-service

# Attack Vector Details
attack_type: denial-of-service
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3638
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/25
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/5

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
  - denial-of-service
  - dos

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
  - hickuphh3
---

## Vulnerability Title

M-6: Slashing fails if claims revert

### Overview


This bug report is about the slashing process in the Telcoin Staking Module. Slashing is a process used to reduce the yield of an account that has violated the rules of the contract. During the process, the slashing calls the underlying `_claimAndExit()` function, which claims yield from all plugins. If one or more of these claims fail, the slashing process will also fail. This could lead to the slashed user being able to claim their yield and exit, leading to a loss of yield for the contract.

The bug was found by hickuphh3 and was verified by manual review. To fix the bug, a recommendation was made to create another `slash()` method that skips claiming yields of the slashed account. A discussion was also linked to a pull request on the Telcoin Staking repository.

In conclusion, this bug report is about a bug in the Telcoin Staking Module that could lead to a loss of yield for the contract. A recommendation was made to create another `slash()` method that skips claiming yields of the slashed account.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/5 

## Found by 
hickuphh3

## Summary
Slashing claims yields for the slashed account as part of the process. Should claims revert, slashing attempts will revert too.

## Vulnerability Detail
Slashing calls the underlying `_claimAndExit()` function, which claims yield from all plugins. Should one or more claims fail, slashing will revert as well.

## Impact
Failing claims brick the slashing functionality until the erroneous plugin(s) are removed. During which, the slashed user could have claimed his yield and exited.

## Code Snippet
https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/StakingModule.sol#L403-L406
https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/StakingModule.sol#L356-L379

## Tool used

Manual Review

## Recommendation
Create another `slash()` method that skips claiming yields of the slashed account.

## Discussion

**amshirif**

https://github.com/telcoin/telcoin-staking/pull/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin |
| Report Date | N/A |
| Finders | hickuphh3 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/5
- **Contest**: https://app.sherlock.xyz/audits/contests/25

### Keywords for Search

`Denial-Of-Service, DOS`

