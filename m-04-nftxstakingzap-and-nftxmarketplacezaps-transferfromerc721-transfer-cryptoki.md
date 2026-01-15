---
# Core Classification
protocol: NFTX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42413
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-12-nftx
source_link: https://code4rena.com/reports/2021-12-nftx
github_link: https://github.com/code-423n4/2021-12-nftx-findings/issues/185

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
  - cross_chain
  - rwa
  - leveraged_farming
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] NFTXStakingZap and NFTXMarketplaceZap's transferFromERC721 transfer Cryptokitties to the wrong address

### Overview


The report is about a bug in the transferFromERC721 function, which is used to transfer non-fungible tokens (NFTs) from one address to another. The function is supposed to transfer the NFT from the sender to the specified address, but when used with Cryptokitties, it instead transfers the NFT to the contract address. This can cause problems with the NFT accounting and result in the NFT being lost in the contract. The bug has been identified in two user-facing functions, NFTXStakingZap and NFTXMarketplaceZap, which are used for buying, selling, and adding liquidity to NFTs. The recommended solution is to fix the address in the code to ensure that the NFT is transferred to the correct address. The project team has confirmed the bug, but disagrees with the severity and has resolved the issue.

### Original Finding Content

_Submitted by hyh_

`transferFromERC721(address assetAddr, uint256 tokenId, address to)` should transfer from `msg.sender` to `to`.
It transfers to `address(this)` instead when ERC721 is Cryptokitties.
As there is no additional logic for this case it seems to be a mistake that leads to wrong NFT accounting after such a transfer as NFT will be missed in the vault (which is `to`).

#### Proof of Concept

NFTXStakingZap:
transferFromERC721
<https://github.com/code-423n4/2021-12-nftx/blob/main/nftx-protocol-v2/contracts/solidity/NFTXStakingZap.sol#L416>

NFTXMarketplaceZap:
transferFromERC721
<https://github.com/code-423n4/2021-12-nftx/blob/main/nftx-protocol-v2/contracts/solidity/NFTXMarketplaceZap.sol#L556>

Both functions are called by user facing Marketplace buy/sell and Staking addLiquidity/provideInventory functions.

#### Recommended Mitigation Steps

Fix the address:

Now:

```solidity
  // Cryptokitties.
  data = abi.encodeWithSignature("transferFrom(address,address,uint256)", msg.sender, address(this), tokenId);
```

To be:
```solidity
  // Cryptokitties.
  data = abi.encodeWithSignature("transferFrom(address,address,uint256)", msg.sender, to, tokenId);
```

**[0xKiwi (NFTX) confirmed, but disagreed with medium severity and commented](https://github.com/code-423n4/2021-12-nftx-findings/issues/185#issuecomment-1003211591):**
 > This was intentional, as I thought it was needed for the contract to require custody, but it should work fine to send directly to the vault.

**[0xKiwi (NFTX) resolved](https://github.com/code-423n4/2021-12-nftx-findings/issues/185)**


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-nftx
- **GitHub**: https://github.com/code-423n4/2021-12-nftx-findings/issues/185
- **Contest**: https://code4rena.com/reports/2021-12-nftx

### Keywords for Search

`vulnerability`

