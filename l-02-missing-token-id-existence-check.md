---
# Core Classification
protocol: Sft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34170
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SFT-security-review.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-02] Missing token id existence check

### Overview

See description below for full details.

### Original Finding Content

The [EIP-721 specification](https://eips.ethereum.org/EIPS/eip-721#specification) states that "every ERC-721 compliant contract must implement the ERC721 interface (subject to caveats below)".

For the `getApproved()` function, it states that it "Throws if `_tokenId` is not a valid NFT":

```solidity
    /// @notice Get the approved address for a single NFT
@>  /// @dev Throws if `_tokenId` is not a valid NFT.
    /// @param _tokenId The NFT to find the approved address for
    /// @return The approved address for this NFT, or the zero address if there is none
    function getApproved(uint256 _tokenId) external view returns (address);
```

This breaks compatibility with the ERC-721 standard and any integrations expected to follow it.

Consider reverting if the token id is not a valid NFT:

```diff
    function _FB721GetApproved(uint256 id_) internal virtual view returns (address) {
+       require(_chunkToOwners[id_].owner != address(0), "INVALID_ID");
        return _getApproved[id_];
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sft |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SFT-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

