---
# Core Classification
protocol: Carapace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6617
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/40
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/112

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 14
finders:
  - clems4ever
  - 0x52
  - immeas
  - modern\_Alchemist\_00
  - jkoppel
---

## Vulnerability Title

H-8: Protection buyer may buy multiple protections for same goldfinch NFT

### Overview


A bug was discovered in the Carapace protocol which allows a protection buyer to buy multiple protections for the same Goldfinch loan. The check for the possibility for a user to buy a protection is done in the ReferenceLendingPools.canBuyProtection which checks that the protection about to be created does not cross the remaining principal. However, it still allows the user to create multiple protections for the same loan position. This could lead to a malicious user overprotecting their loan position on Goldfinch and thus claiming a larger amount on loan default than what they lended. This could also be used to DOS the protocol by using all funds deposited into the protocol reaching the leverageRatioFloor and not allowing any new protections to be bought.

To fix this issue, the total protection subscribed for a given loan should be tracked and limited to the remaining capital. The bug was originally identified in Issue H-8, and was found by libratus, ctf_sec, minhtrng, jkoppel, clems4ever, chaduke, __141345__, Allarious, immeas, c7e7eff, 0Kage, 0x52, modern_Alchemist_00, bin2chen. A PR to fix this issue was proposed by vnadoda and can be found at https://github.com/carapace-finance/credit-default-swaps-contracts/pull/59. The sponsor comment from #193 stated that double buying of protections for the same NFT is a known issue and was planned to be tackled in an upcoming version.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/112 

## Found by 
libratus, ctf\_sec, minhtrng, jkoppel, clems4ever, chaduke, \_\_141345\_\_, Allarious, immeas, c7e7eff, 0Kage, 0x52, modern\_Alchemist\_00, bin2chen

## Summary
The Carapace protocol checks that a protection buyer does not buy a protection for an 
amount greater than the remainingPrincipal in the corresponding loan. 
However it possible for the buyer to buy multiple different protections for the same Goldfinch loan.

## Vulnerability Detail
The check for the possibility for a user to buy a protection is done here in `ReferenceLendingPools.canBuyProtection`:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ReferenceLendingPools.sol#L132-L168

It checks the protection about to be created does not cross remaining principal. But it still allows the user to create multiple protections for the same loan position.

## Impact
The malicious user can `overprotect` their loan position on Goldfinch and thus claim a larger amount on loan default than what they lended. For now as the default claiming feature is not implemented, they can use this bug to DOS the protocol by using all funds deposited into the protocol reaching `leverageRatioFloor` and not allowing any new protections to be bought.

## Code Snippet

## Tool used
Manual Review

## Recommendation
Keep track of the total protection subscribed for a given loan and limit total protection value to remaining capital

## Discussion

**vnadoda**

@clems4ev3r this is duplicate of #193 & #139

**hrishibhat**

Sponsor comment from #193:

Double buying of protections for the same NFT is a known issue and we were planning to tackle it in an upcoming version because even after buying multiple protections buyers won't be able to claim for the same position as default payout will require NFT lock/transfer in the carapace vault.

This double counting of locked capital issue seems a legit concern.
Now we are considering fixing this with other audit issues.


**vnadoda**

@clems4ev3r PR for this fix: https://github.com/carapace-finance/credit-default-swaps-contracts/pull/59

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Carapace |
| Report Date | N/A |
| Finders | clems4ever, 0x52, immeas, modern\_Alchemist\_00, jkoppel, bin2chen, Allarious, c7e7eff, \_\_141345\_\_, chaduke, 0Kage, libratus, minhtrng, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/112
- **Contest**: https://app.sherlock.xyz/audits/contests/40

### Keywords for Search

`vulnerability`

