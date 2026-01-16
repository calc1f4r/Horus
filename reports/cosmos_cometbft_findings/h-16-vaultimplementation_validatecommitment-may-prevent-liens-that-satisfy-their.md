---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3654
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/182

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - Jeiwan
  - 0xRajeev
  - hansfriese
  - tives
  - rvierdiiev
---

## Vulnerability Title

H-16: `VaultImplementation._validateCommitment` may prevent liens that satisfy their terms of `maxPotentialDebt`

### Overview


Issue H-16 is a bug report found by obront, 0xRajeev, hansfriese, rvierdiiev, zzykxx, Jeiwan, and tives on the GitHub repository of sherlock-audit/2022-10-astaria-judging/issues/182. The issue is related to the calculation of `potentialDebt` in `VaultImplementation._validateCommitment()`, which incorrectly adds a factor of `ld.duration` to `seniorDebt` thus making the potential debt much higher than it should be. This miscalculation will cause a DoS to legitimate borrowers as liens that would have otherwise satisfied the constraint of `potentialDebt <= ld.maxPotentialDebt` will fail. The code snippet of the issue can be found at https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/VaultImplementation.sol#L221-L225 and https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L256-L262. The recommended solution is to change the calculation to `uint256 potentialDebt = seniorDebt * (ld.rate * ld.duration + 1).mulDivDown(1, INTEREST_DENOMINATOR);` and to consider the implied rate of all the liens against the collateral instead of only this lien. The issue was escalated for 2 USDC, accepted, and the contestants' payouts and scores will be updated according to the changes made on this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/182 

## Found by 
obront, 0xRajeev, hansfriese, rvierdiiev, zzykxx, Jeiwan, tives

## Summary

The calculation of `potentialDebt` in `VaultImplementation._validateCommitment()` is incorrect and will cause a DoS to legitimate borrowers.

## Vulnerability Detail

The calculation of potentialDebt in `VaultImplementation._validateCommitment()` is incorrect because it computes `uint256 potentialDebt = seniorDebt * (ld.rate + 1) * ld.duration;` which incorrectly adds a factor of `ld.duration` to `seniorDebt` thus making the potential debt much higher by that factor than it will be. The use of `INTEREST_DENOMINATOR` and implied lien rate is also missing here. 


## Impact

Liens that would have otherwise satisfied the constraint of `potentialDebt <= ld.maxPotentialDebt` will fail because of this miscalculation and will cause a DoS to legitimate borrowers and likely all of them.

## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/VaultImplementation.sol#L221-L225
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L256-L262

## Tool used

Manual Review

## Recommendation

Change the calculation to `uint256 potentialDebt = seniorDebt * (ld.rate * ld.duration + 1).mulDivDown(1, INTEREST_DENOMINATOR);`. This should also consider the implied rate of all the liens against the collateral instead of only this lien.

## Discussion

**secureum**

Escalate for 2 USDC.

Given the potential impact to different flows/contexts, we still think this is a high-severity impact (not Medium as judged). A majority of the dups (4 of 6) also reported this as a High.

cc @berndartmueller @lucyoa

**sherlock-admin**

 > Escalate for 2 USDC.
> 
> Given the potential impact to different flows/contexts, we still think this is a high-severity impact (not Medium as judged). A majority of the dups (4 of 6) also reported this as a High.
> 
> cc @berndartmueller @lucyoa

You've created a valid escalation for 2 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Evert0x**

Escalation accepted.


**sherlock-admin**

> Escalation accepted.
> 

This issue's escalations have been accepted!

Contestants' payouts and scores will be updated according to the changes made on this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Jeiwan, 0xRajeev, hansfriese, tives, rvierdiiev, obront, zzykxx |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/182
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

