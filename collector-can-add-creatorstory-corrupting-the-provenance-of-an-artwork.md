---
# Core Classification
protocol: Cryptoart
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55571
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:
  - business_logic

protocol_categories:
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Hans
  - Dacian
---

## Vulnerability Title

Collector can add `CreatorStory`, corrupting the provenance of an artwork

### Overview


The `IStory` interface is used to add "Stories" about a given artwork (NFT) to record its "provenance" or history. However, in the CryptoArt implementation, anyone who owns the artwork can add a `CreatorStory` event, corrupting the provenance by allowing non-Creators to add to it. To fix this, only the Creator should be able to emit the `CreatorStory` event and the contract owner could act as a proxy for the Creator. This issue has been fixed in the CryptoArt contract.

### Original Finding Content

**Description:** The purpose of the `IStory` interface is to allow 3 different entities (Admin, Creator and Collectors) to add "Stories" about a given artwork (NFT) which [describes the provenance of the artwork](https://docs.transientlabs.xyz/tl-creator-contracts/common-features/story-inscriptions). In the art world the "provenance" of an item can affect its status and price, so the `IStory` interface aims to facilitate an on-chain record of an artwork's "provenance".

`IStory` is designed to work like this:
* Creator/Admin can add a `CollectionsStory` for when a collection is added to a contract
* Creator of an artwork can add a `CreatorStory`
* Collector of an artwork can add one or more `Story` about their experience while holding the artwork

The `IStory` interface specification requires that `addCreatorStory` is only called by the creator:
```solidity
/// @notice Function to let the creator add a story to any token they have created
/// @dev This function MUST implement logic to restrict access to only the creator
function addCreatorStory(uint256 tokenId, string calldata creatorName, string calldata story) external;
```

But in the CryptoArt implementation of the `IStory` interface, the current token owner can always emit `CreatorStory` events:
```solidity
function addCreatorStory(uint256 tokenId, string calldata, /*creatorName*/ string calldata story)
    external
    onlyTokenOwner(tokenId)
{
    emit CreatorStory(tokenId, msg.sender, msg.sender.toHexString(), story);
}
```

**Impact:** As an NFT is sold or transferred to new owners, each subsequent owner can continue to add new `CreatorStory` events even though they aren't the Creator of the artwork. This corrupts the provenance of the artwork by allowing Collectors to add to the `CreatorStory` as if they were the Creator.

**Recommended Mitigation:** Only the Creator of an artwork should be able to emit the `CreatorStory` event. Currently the on-chain protocol does not record the address of the creator; this could either be added or `onlyOwner` could be used where the contract owner acts as a proxy for the creator.

**CryptoArt:**
Fixed in commit [94bfc1b](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/94bfc1b1454e783ef1fb9627cfaf0328ebe17b47#diff-1c61f2d0e364fa26a4245d1033cdf73f09117fbee360a672a3cb98bc0eef02adL439-R439).

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Cyfrin |
| Protocol | Cryptoart |
| Report Date | N/A |
| Finders | Hans, Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Business Logic`

