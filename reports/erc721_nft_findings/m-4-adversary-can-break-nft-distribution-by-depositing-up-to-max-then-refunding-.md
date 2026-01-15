---
# Core Classification
protocol: OpenQ
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6607
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/39
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-openq-judging/issues/262

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
  - synthetics

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - clems4ever
  - HollaDieWaldfee
  - 0x52
  - jkoppel
  - Jeiwan
---

## Vulnerability Title

M-4: Adversary can break NFT distribution by depositing up to max then refunding all of them

### Overview


This bug report is about an issue with NFT distribution found by a group of auditors. The issue is that the current system limits the number of NFT deposits to five, and an adversary can block adding NFTs by repeatedly depositing and withdrawing an NFT. The code snippet referenced in the report shows that when an NFT deposit is refunded, it does not remove the depositID from nftDeposits, leading to the blockage of legitimate NFT distribution. The impact of this issue is that the adversary can block legitimate NFT distribution. The recommendation given is to remove the depositID from nftDeposits when an NFT deposit is refunded. The discussion section shows that the issue has been fixed by removing nft funding and disabling crowdfunding, as referenced in three separate pull requests.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-openq-judging/issues/262 

## Found by 
HollaDieWaldfee, Jeiwan, 0x52, HonorLt, GimelSec, bin2chen, caventa, kiki\_dev, clems4ever, unforgiven, Ruhum, 0xmuxyz, dipp, jkoppel, libratus

## Summary

Bounties limit the number of NFT deposits to five. An adversary can block adding NFTs by repeatedly depositing and withdrawing an NFT.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/BountyCore.sol#L64-L93

All bounties use BountyCore#refundDeposit to process refunds to user. This simply transfers the NFT back to the funder but leaves the nftDeposit. This uses up the deposit limit which is current set to 5. Since the deposit cap is used up by deposits that have been refunded the slots can't be used to distribute legitimate NFTs to the bounty claimant. 

## Impact

Adversary can block legitimate NFT distribution

## Code Snippet

https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/BountyCore.sol#L64-L93

## Tool used

Manual Review

## Recommendation

When an NFT deposit is refunded it should remove the depositID from nftDeposits

## Discussion

**FlacoJones**

Valid. Will fix by removing nft funding and disbaling crowdfunding

**FlacoJones**

https://github.com/OpenQDev/OpenQ-Contracts/pull/113

and 

https://github.com/OpenQDev/OpenQ-Contracts/pull/116

and

https://github.com/OpenQDev/OpenQ-Contracts/pull/114

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | OpenQ |
| Report Date | N/A |
| Finders | clems4ever, HollaDieWaldfee, 0x52, jkoppel, Jeiwan, bin2chen, Ruhum, 0xmuxyz, kiki\_dev, dipp, caventa, unforgiven, HonorLt, libratus, GimelSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-openq-judging/issues/262
- **Contest**: https://app.sherlock.xyz/audits/contests/39

### Keywords for Search

`vulnerability`

