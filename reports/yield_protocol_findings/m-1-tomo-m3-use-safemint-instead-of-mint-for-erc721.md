---
# Core Classification
protocol: FrankenDAO
chain: everychain
category: uncategorized
vulnerability_type: nft

# Attack Vector Details
attack_type: nft
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3593
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/18
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/65

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 5

# Context Tags
tags:
  - nft
  - mint_vs_safemint
  - erc721

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Tomo
---

## Vulnerability Title

M-1: [Tomo-M3] Use safeMint instead of mint for ERC721

### Overview


This bug report is about an issue found by Tomo in the code of the Sherlock Audit project. The issue is related to the minting of an ERC721 token when the _stakeToken() function is called. The problem is that if the `msg.sender` is a contract address that does not support ERC721, the token can be frozen in the contract. This could lead to users losing their NFTs. The code snippet provided is from the Staking.sol file, line 411, which shows the `_mint(msg.sender, _tokenId)` function.

The recommendation is to use the `safeMint` function instead of `mint` to check if the received address supports ERC721 implementation. This is in line with the documentation of EIP-721, which states that a wallet/broker/auction application must implement the wallet interface if it will accept safe transfers. The code for the `safeMint` function can be found in the ERC721.sol file by Openzeppelin.

The issue was fixed in the Pull Request #14 by zobront, who did not need to add `safeMint`, as they made a change for another issue that removed the ability to non-holder to unstake, which ensured they had the ability to hold NFTs.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/65 

## Found by 
Tomo

## Summary

Use safeMint instead of mint for ERC721

## Vulnerability Detail

The `msg.sender` will be minted as a proof of staking NFT when `_stakeToken()` is called. 

However, if `msg.sender` is a contract address that does not support ERC721, the NFT can be frozen in the contract.

As per the documentation of EIP-721:

> A wallet/broker/auction application MUST implement the wallet interface if it will accept safe transfers.
> 

Ref: [https://eips.ethereum.org/EIPS/eip-721](https://eips.ethereum.org/EIPS/eip-721)

As per the documentation of ERC721.sol by Openzeppelin

Ref: [https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L274-L285](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L274-L285)

```solidity
/**
 * @dev Mints `tokenId` and transfers it to `to`.
 *
 * WARNING: Usage of this method is discouraged, use {_safeMint} whenever possible
 *
 * Requirements:
 *
 * - `tokenId` must not exist.
 * - `to` cannot be the zero address.
 *
 * Emits a {Transfer} event.
 */
function _mint(address to, uint256 tokenId) internal virtual {
```

## Impact

Users possibly lose their NFTs

## Code Snippet
https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L411
``` solidity
  _mint(msg.sender, _tokenId);
```
## Tool used

Manual Review

## Recommendation

Use `safeMint` instead of `mint` to check received address support for ERC721 implementation.

[https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L262](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L262)

## Discussion

**zobront**

I might consider this a duplicate of #55 but not sure how this is usually judged. We will be changing this function based on other issues to not allow "approved" spenders, so msg.sender will be the owner of the FrankenPunk, which ensures they are able to hold NFTs.

**zobront**

Fixed: https://github.com/Solidity-Guild/FrankenDAO/pull/14

I didn't need to add safeMint, as I made a change for another issue that removed the ability to non holder to unstake, which means they have the ability to hold NFTs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | FrankenDAO |
| Report Date | N/A |
| Finders | Tomo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/65
- **Contest**: https://app.sherlock.xyz/audits/contests/18

### Keywords for Search

`NFT, mint vs safeMint, ERC721`

