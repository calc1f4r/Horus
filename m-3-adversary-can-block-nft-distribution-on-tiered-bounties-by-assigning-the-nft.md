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
solodit_id: 6606
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/39
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-openq-judging/issues/264

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

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
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-3: Adversary can block NFT distribution on tiered bounties by assigning the NFTs to unused tiers

### Overview


This bug report is about an issue in the DepositManagerV1.sol contract where an adversary can block the distribution of NFTs on tiered bounties by assigning the NFTs to unused tiers. The vulnerability is found in the code snippet at https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/DepositManager/Implementations/DepositManagerV1.sol#L113-L131, where DepositMangerV1#fundBountyNFT passes the user supplied _data to TieredBountyCore#receiveNft. This allows the user to specify any tier they wish, and an adversary can abuse this by filling all eligible NFT deposit slots with NFTs that can't be claimed by any tier. This effectively disables NFT prizes for any tiered bounty. 

The impact of this vulnerability is that an adversary can effectively disable NFT prizes for any tiered bounty. The recommended solution is for TieredBountyCore#receiveNFT to check that the specified tier is within bounds (i.e. by comparing it to the length of tierWinners). This issue was incorrectly duped with #261 and was missed during the processing of the initial results. It was found by 0x52 through manual review and is a valid medium, and also unique. The attacker can fill tiers large enough so that it is not possible to set the payout schedule for any tier due to out of gas.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-openq-judging/issues/264 

## Found by 
0x52

## Summary

Bounties limit the number of NFT deposits to five. An adversary can block adding NFTs by assigning NFTs to tiers that don't exist.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/DepositManager/Implementations/DepositManagerV1.sol#L113-L131

DepositMangerV1#fundBountyNFT passes the user supplied _data to TieredBountyCore#receiveNft

https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/TieredBountyCore.sol#L41-L42

_data is decoded and stored in _tier allowing the user to specify any tier they wish.

An adversary can abuse this fill all eligible nft deposit slots with nfts that can't be claimed by any tier. This allows them to effectively disable nft prizes for any tiered bounty. Using a large enough tier will make it impossible to ever claim the nfts because it would cost too much gas to set a large enough payout schedule

## Impact

Adversary can effectively disable nft prizes for any tiered bounty 

## Code Snippet

https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/TieredBountyCore.sol#L18-L48

## Tool used

Manual Review

## Recommendation

TieredBountyCore#receiveNFT should check that specified tier is a within bound (i.e. by comparing it to the length of tierWinners)


## Discussion

**IAm0x52**

Not a dupe of #261 and a separate issue. This discusses supplying NFTs to the incorrect tiers of tiered bounties

**hrishibhat**

This issue was incorrectly duped with #261 and was missed during the processing of the initial results. 
This issue is a valid medium, and also unique.
As mentioned above, the attacker can fill tiers large enough so that it is not possible to set the payout schedule for any tier due to out of gas.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | OpenQ |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-openq-judging/issues/264
- **Contest**: https://app.sherlock.xyz/audits/contests/39

### Keywords for Search

`vulnerability`

