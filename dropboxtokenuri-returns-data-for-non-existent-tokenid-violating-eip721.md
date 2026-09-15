---
# Core Classification
protocol: Earnm Dropbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41172
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
github_link: none

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
finders_count: 1
finders:
  - Dacian
---

## Vulnerability Title

`DropBox::tokenURI` returns data for non-existent `tokenId` violating `EIP721`

### Overview


The bug report is about a function called `DropBox::tokenURI` in a smart contract that overrides a default implementation from OpenZeppelin. The problem is that this function does not check if the token ID exists, which can lead to incorrect data being returned. This goes against the standards set by EIP721 and can cause issues with NFT marketplaces. The recommended solution is to add a check to make sure the token ID exists before returning data. This bug has been fixed in a recent commit and has been verified.

### Original Finding Content

**Description:** `DropBox::tokenURI` overrides OpenZeppelin's default implementation with the following code:
```solidity
function tokenURI(uint256 tokenId) public view override returns (string memory) {
  return string(abi.encodePacked(bytes(_baseTokenURI), Strings.toString(tokenId), ".json"));
}
```

This implementation does not check that `tokenId` exists and hence will return data for non-existent `tokenId`. This is in contrast to OpenZeppelin's [implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L88-L93) and contrary to [EIP721](https://eips.ethereum.org/EIPS/eip-721) which states:

```solidity
/// @notice A distinct Uniform Resource Identifier (URI) for a given asset.
/// @dev Throws if `_tokenId` is not a valid NFT. URIs are defined in RFC
///  3986. The URI may point to a JSON file that conforms to the "ERC721
///  Metadata JSON Schema".
function tokenURI(uint256 _tokenId) external view returns (string);
```

**Impact:** Apart from simply returning incorrect data, the most likely negative effect is integration problems with NFT marketplaces.

**Recommended Mitigation:** Revert if `tokenId` does not exist:
```diff
function tokenURI(uint256 tokenId) public view override returns (string memory) {
+ _requireOwned(tokenId);
  return string(abi.encodePacked(bytes(_baseTokenURI), Strings.toString(tokenId), ".json"));
}
```

**Mode:**
Fixed in commit [2d8c3c0](https://github.com/Earnft/dropbox-smart-contracts/commit/2d8c3c0142f70fae183f1185ea1987a0707711ef).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Earnm Dropbox |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

