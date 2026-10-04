---
# Core Classification
protocol: RipIt_2025-04-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62551
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-04-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] Non-compliance with EIP-721 in `tokenURI()` function

### Overview


The `tokenURI` function in the `RipFunPacks` and `Card` contracts does not follow the EIP-721 standard. Instead of throwing an error when an invalid `tokenId` is provided, the function returns an empty string. This can cause confusion and make it difficult for clients and applications to determine the validity of a token. To fix this issue, the function should be modified to revert when an invalid `tokenId` is provided.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Low

**Likelihood:** High

## Description

Similar Finding: [Link](https://solodit.cyfrin.io/issues/dropboxtokenuri-returns-data-for-non-existent-tokenid-violating-eip721-cyfrin-none-earnm-dropbox-markdown)

The `tokenURI` function in the`RipFunPacks` contract does not strictly adhere to the EIP-721 standard. 

```solidity
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        return _packetUris[tokenId];
    }
```

According to the [EIP-721 specification](https://eips.ethereum.org/EIPS/eip-721), the function should throw an error if the provided _tokenId does not correspond to a valid NFT.

```solidity
    /// @notice A distinct Uniform Resource Identifier (URI) for a given asset.
    /// @dev Throws if `_tokenId` is not a valid NFT. URIs are defined in RFC
    ///  3986. The URI may point to a JSON file that conforms to the "ERC721
    ///  Metadata JSON Schema".
    function tokenURI(uint256 _tokenId) external view returns (string);
```

However, the current implementation simply returns an empty string for non-existent tokenId values. This behavior can lead to confusion and makes it difficult for clients and applications to determine the validity of a token.

Note: this is the same for `Card` contract.

```solidity
    /**
     * @dev Returns the metadata URI for a given card
     * @param tokenId ID of the card
     * @return Metadata URI for the card
     */
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        return _cardUris[tokenId];
    }
```

## Recommendations

To ensure compliance with the EIP-721 standard, modify the `tokenURI` function to revert when an invalid `tokenId` is provided. 





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RipIt_2025-04-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-04-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

