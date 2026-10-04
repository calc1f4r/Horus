---
# Core Classification
protocol: Gigaverse_2025-01-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53289
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Gigaverse-security-review_2025-01-18.md
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

[M-01] Missing cleanup of certain registered data when burning an NFT

### Overview


The report discusses a bug in two NFT contracts, `GigaNameNFT` and `GigaNoobNFT`, where data entries are not being removed when an NFT is burned. This means that even after an NFT is destroyed, its data can still be accessed by others. The severity of this bug is considered medium, and the likelihood of it occurring is also medium. The report recommends that the relevant data be cleared during the minting process.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

For `GigaNameNFT`, when minting, `IS_GIGA_NAME_CID`, `NAME_CID`, and `INITIALIZED_CID` are set. However, these data entries are not removed upon burning the NFT.

```solidity
    function _initializeTraits(uint256 tokenId, string memory username) internal nonReentrant onlyRole(GAME_LOGIC_CONTRACT_ROLE) {
        require(validateUsername(username), "Invalid username");
        require(tokenId == uint256(keccak256(abi.encodePacked(username))), "Token ID does not match name");

        _setDocBoolValue(tokenId, IS_GIGA_NAME_CID, true);
        validateUsername(username);
        _setDocStringValue(tokenId, NAME_CID, username);
    }
```

```solidity
    function _safeMint(address to, uint256 tokenId, bytes memory data) internal override {
        ...
        // Conditionally initialize traits
        if (getDocBoolValue(tokenId, INITIALIZED_CID) == false) {
            _initializeTraits(tokenId);
            _setDocBoolValue(tokenId, INITIALIZED_CID, true);
        }
    }
```

For `GigaNoobNFT`, during minting, `IS_NOOB_CID`, `LEVEL_CID`, and `INITIALIZED_CID` are set. However, these data entries are not removed upon burning the NFT.

```solidity
    function _initializeTraits(uint256 tokenId) internal override {
        _setDocBoolValue(tokenId, IS_NOOB_CID, true);
        _setDocUint256Value(tokenId, LEVEL_CID, 1);
    }
```

## Recommendations

It is recommended to clear the relevant data set during minting in the table when destroying.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Gigaverse_2025-01-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Gigaverse-security-review_2025-01-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

