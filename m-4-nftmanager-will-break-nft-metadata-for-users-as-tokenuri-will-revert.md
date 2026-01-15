---
# Core Classification
protocol: Ammplify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63183
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1054
source_link: none
github_link: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/94

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

# Audit Details
report_date: unknown
finders_count: 17
finders:
  - Sa1ntRobi
  - befree3x
  - 8olidity
  - jayjoshix
  - OxNoble
---

## Vulnerability Title

M-4: NFTManager will break NFT metadata for users as tokenURI() will revert

### Overview


The bug report discusses an issue found by multiple users with the code for Ammplify's NFTManager. The issue is caused by the use of AssetLib.getAsset inside NFTManager._generateMetadata/_generateSVG, which reads diamond storage directly and always sees asset.owner == address(0), causing a revert for users requesting NFT metadata. This means that users are unable to retrieve NFT metadata, making the NFTs unusable in external integrations. The protocol team has fixed this issue in their code.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/94 

## Found by 
0xAsen, 8olidity, JeRRy0422, OxNoble, Sa1ntRobi, axelot, befree3x, drdee, fullstop, glitch-Hunter, jayjoshix, kimnoic, soloking, thimthor, veerendravamshi, vivekd, vtim

### Summary

The use of AssetLib.getAsset inside NFTManager._generateMetadata/_generateSVG will cause a revert for users requesting NFT metadata, as NFTManager will read diamond storage directly and always see asset.owner == address(0).

### Root Cause

In [NFTManager.sol:_generateMetadata](https://github.com/sherlock-audit/2025-09-ammplify/blob/main/Ammplify/src/integrations/NFTManager.sol#L421-L469), the call to AssetLib.getAsset(assetId) reads from Store.assets() (diamond storage). Since the call originates from NFTManager, it resolves against the ERC721’s own storage instead of the diamond’s, making every asset appear unset.

### Internal Pre-conditions

1. A user must have minted a position through NFTManager.mintNewMaker.

2. The user (or marketplace) calls NFTManager.tokenURI(tokenId) to query metadata.

### External Pre-conditions

None.

### Attack Path

1. User calls NFTManager.mintNewMaker → NFT minted successfully, mappings updated.

2. Any party calls NFTManager.tokenURI(tokenId) → _generateMetadata calls AssetLib.getAsset(assetId).

3. AssetLib resolves Store.assets() against NFTManager storage, not the diamond.

4. asset.owner == address(0) → require fails → transaction reverts.

### Impact

The users cannot retrieve NFT metadata. As a result, wallets, explorers, and marketplaces cannot display Ammplify NFTs, effectively breaking NFT usability. This makes minted NFTs indistinguishable and practically unusable in external integrations.

### PoC

_No response_

### Mitigation

Refactor _generateMetadata and _generateSVG to avoid AssetLib. Fetch asset data through the IView facet (getAssetInfo and getPoolInfo) as already done in positions().

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/itos-finance/Ammplify/pull/36






### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Ammplify |
| Report Date | N/A |
| Finders | Sa1ntRobi, befree3x, 8olidity, jayjoshix, OxNoble, kimnoic, veerendravamshi, drdee, axelot, 0xAsen, thimthor, vivekd, soloking, JeRRy0422, vtim, fullstop, glitch-Hunter |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/94
- **Contest**: https://app.sherlock.xyz/audits/contests/1054

### Keywords for Search

`vulnerability`

