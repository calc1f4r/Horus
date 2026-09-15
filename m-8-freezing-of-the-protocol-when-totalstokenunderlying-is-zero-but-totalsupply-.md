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
solodit_id: 6629
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/40
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/117

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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - clems4ever
  - jprod15
  - Bauer
  - Ruhum
  - chaduke
---

## Vulnerability Title

M-8: Freezing of the protocol when totalSTokenUnderlying is zero but totalSupply is non-zero

### Overview


A bug was identified in the code of the protocol, where it can freeze if the totalSTokenUnderlying is zero but totalSupply is non-zero. This was found by clems4ever, chaduke, Ruhum, jprod15, Bauer, Kumpa, mert_eren, and Web3SecurityDAO. In this case, the protocol will not be able to accept any new deposits or new protection buys, effectively halting the protocol. This is due to the fact that the `_getExchangeRate()` is zero, and `convertToSToken` tries to divide by this, causing the transaction to revert. This means any new protection buying attempts will also revert due to the `_leverageRatio` being zero. The only way to fix this is if every SToken holder burns their shares by calling `withdraw` after enough cycles have passed. It is recommended to keep a minimum amount of totalSTokenUnderlying in the contract in any case.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/117 

## Found by 
clems4ever, chaduke, Ruhum, jprod15, Bauer, Kumpa, mert\_eren, Web3SecurityDAO

## Summary
In some cases the protocol can contain zero funds while having a non zero totalSupply of STokens. In that case the protocol will not be able to accept any new deposits and any new protection buys, thus coming to a halt, unless all STokens are burned by their respective holders.

## Vulnerability Detail
In the case `lockCapital` has to lock all available capital:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L415-L419

`totalSTokenUnderlying` becomes zero, but `totalSupply` is still non-zero since no SToken have been burned. 
Which means that new deposits will revert because `_getExchangeRate()` is zero:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L602-L605

And `convertToSToken` tries to divide by `_getExchangeRate()`;
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L602-L605 

Also all new protection buying attempts will revert because `_leverageRatio` is zero, and thus under `leverageRatioFloor`.

## Impact
The protocol comes to a halt, unless every SToken holder burn their shares by calling `withdraw` after enough cycles have passed, returning to the case `totalSupply == 0`.

## Code Snippet

## Tool used

Manual Review

## Recommendation
Keep a minimum amount of totalSTokenUnderlying in the contract in any case (can be 1e6).

## Discussion

**vnadoda**

@clems4ev3r we plan to fix this

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Carapace |
| Report Date | N/A |
| Finders | clems4ever, jprod15, Bauer, Ruhum, chaduke, mert\_eren, Web3SecurityDAO, Kumpa |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/117
- **Contest**: https://app.sherlock.xyz/audits/contests/40

### Keywords for Search

`vulnerability`

