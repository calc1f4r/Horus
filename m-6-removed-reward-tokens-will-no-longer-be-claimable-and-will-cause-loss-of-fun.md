---
# Core Classification
protocol: Olympusdao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6682
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/50
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/127

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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - Cryptor
  - Bauer
  - 0x52
  - Ruhum
  - KingNFT
---

## Vulnerability Title

M-6: Removed reward tokens will no longer be claimable and will cause loss of funds to users who haven't claimed

### Overview


This bug report is about a vulnerability that can cause users to lose unclaimed rewards when a reward token is removed. This vulnerability is found in the SingleSidedLiquidityVault.sol code, which is used to manage rewards tokens. The code cycles through the current reward token array and claims each token. When a reward token is removed, its entire reward struct is deleted from the array, making it impossible to claim any unclaimed rewards for that token. As a result, any unclaimed balance that a user had will be permanently lost. The bug was found by Cryptor, CRYP70, kiki_dev, Bauer, hansfriese, HonorLt, gerdusx, KingNFT, 0x52, Ruhum, and rvierdiiev, and was identified as high priority due to the potential for users to lose funds. The recommended solution is to move the reward token into a "claim only" mode when it is removed, so that rewards will no longer accrue but all outstanding balances will still be claimable.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/127 

## Found by 
Cryptor, CRYP70, kiki\_dev, Bauer, hansfriese, HonorLt, gerdusx, KingNFT, 0x52, Ruhum, rvierdiiev

## Summary

When a reward token is removed, it's entire reward structs is deleted from the reward token array. The results is that after it has been removed it is impossible to claim. User's who haven't claimed will permanently lose all their unclaimed rewards.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L694-L703

When a reward token is removed the entire reward token struct is deleted from the array

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L288-L310

When claiming rewards it cycles through the current reward token array and claims each token. As a result of this, after a reward token has been removed it becomes impossible to claim. Any unclaimed balance that a user had will be permanently lost.

Submitting this as high because the way that internal tokens are accrued (see "Internal reward tokens can and likely will over commit rewards") will force this issue and therefore loss of funds to users to happen.

## Impact

Users will lose all unclaimed rewards when a reward token is removed

## Code Snippet

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L694-L703

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L723-L732

## Tool used

ChatGPT

## Recommendation

When a reward token is removed it should be moved into a "claim only" mode. In this state rewards will no longer accrue but all outstanding balances will still be claimable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Olympusdao |
| Report Date | N/A |
| Finders | Cryptor, Bauer, 0x52, Ruhum, KingNFT, kiki\_dev, hansfriese, HonorLt, CRYP70, rvierdiiev, gerdusx |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/127
- **Contest**: https://app.sherlock.xyz/audits/contests/50

### Keywords for Search

`vulnerability`

