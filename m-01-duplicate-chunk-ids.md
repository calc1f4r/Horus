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
solodit_id: 34167
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SFT-security-review.md
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

[M-01] Duplicate Chunk IDs

### Overview


A bug has been found in the `ChunkProcessor` code, where the maximum number of chunks is being limited to `type(uint32).max`. This means that the total number of NFTs that can be created using this code will also be limited to `type(uint32).max`. However, this is not in compliance with EIP721, which allows for a maximum of `type(uint256).max` NFTs. This issue can cause problems when the number of NFTs exceeds `type(uint32).max`, leading to duplicate chunk IDs and violating the non-fungible property. To fix this, the code should either support `uint256` chunk IDs or ensure that the total number of NFTs does not exceed `uint32`.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

In `ChunkProcessor`, the chunk manipulation functions such as `pushChunk()` will perform a downcast of Chunk ID and Indexes from `uint256` to `uint32`. This effectively reduces the maximum number of chunks to `type(uint32).max`, As chunks represent the paired/wrapped ERC721, this means that NFT supply based on SFT418 will be similarly capped as well.

The issue is that capping of the NFT supply to 32-bit is not compliant with EIP721, which allows up to `type(uint256).max` NFTs. This is evident from the use of `uint256` to represent the account balance in `balanceOf()`.

The implication of this issue is that SFT418 will not function properly when it is used for cases where the number of NFTs exceeds `type(uint32).max`.

That will cause duplication of chunk ID as Chunk ID greater than `type(uint32).max` will be truncated to 32-bit, violating the non-fungible property.

```Solidity
    function _pushChunk(address to_, uint256 id_) internal virtual {
        require(to_ != address(0), "INVALID_TO");

        require(_chunkToOwners[id_].owner == address(0), "CHUNK_EXISTS");

        uint256 _nextIndex = _ownerToChunkIndexes[to_].length;

        _chunkToOwners[id_] = ChunkInfo(
            to_,
            //@audit index is downcasted to uint32
            uint32(_nextIndex)
        );

         //@audit chunk ID is also downcasted to uint32
        _ownerToChunkIndexes[to_].push(uint32(id_));
    }
```

**Recommendations**

Either support up to `uint256` Chunk ID/Indexes or ensure that chunk ID and total ERC721 supply does not exceed `uint32`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

