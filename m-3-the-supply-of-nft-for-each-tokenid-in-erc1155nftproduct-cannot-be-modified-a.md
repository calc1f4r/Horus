---
# Core Classification
protocol: NFTPort
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3548
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/14
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/95

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cccz
  - GimelSec
---

## Vulnerability Title

M-3: The supply of NFT for each tokenID in ERC1155NFTProduct cannot be modified after the first minting

### Overview


This bug report discusses an issue found in the ERC1155NFTProduct contract, which is part of the Sherlock Audit 2022-10-nftport project. The issue is that the supply of NFT for each tokenID in the contract cannot be modified after the first minting. This will greatly limit the application scenarios of ERC1155NFTProduct. The vulnerability was found by GimelSec and cccz through manual review, and the source code snippets were provided. The recommendation is to consider removing the exists check when minting ERC1155 NFT in the ERC1155NFTProduct contract. However, this suggestion was not implemented as it is working as designed.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/95 

## Found by 
GimelSec, cccz

## Summary
The supply of NFT for each tokenID in ERC1155NFTProduct cannot be modified after the first minting
## Vulnerability Detail
When minting NFT in the ERC1155NFTProduct contract, it will check whether the tokenID already exists, that is, as long as tokenSupply[tokenId] > 0, the ERC1155 NFT of this tokenId will not be able to be minted again.
This will lead to
1. The supply of NFT for each tokenID is determined after the first mint
2. Unable to mint ERC1155 NFT with the same tokenId for different users

This will greatly limit the application scenarios of ERC1155NFTProduct
## Impact

1. The supply of NFT for each tokenID is determined after the first mint
2. Unable to mint ERC1155 NFT with the same tokenId for different users

## Code Snippet
https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/ERC1155NFTProduct.sol#L279-L286
https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/ERC1155NFTProduct.sol#L259-L265
https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/ERC1155NFTProduct.sol#L388-L390
## Tool used

Manual Review

## Recommendation
Consider removing the _exists check when minting ERC1155 NFT in the ERC1155NFTProduct contract

## Discussion

**hyperspacebunny**

We've decided to not change the behaviour at this point and revisit it once we have requests from users. It's currently working as designed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | NFTPort |
| Report Date | N/A |
| Finders | cccz, GimelSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/95
- **Contest**: https://app.sherlock.xyz/audits/contests/14

### Keywords for Search

`vulnerability`

