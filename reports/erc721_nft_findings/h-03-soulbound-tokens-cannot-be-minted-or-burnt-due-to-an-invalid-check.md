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
solodit_id: 53286
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Gigaverse-security-review_2025-01-18.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

[H-03] Soulbound tokens cannot be minted or burnt due to an invalid check

### Overview


This bug report discusses a problem with the `GameNFT` contract, which is used by `GigaNoobNFT` and `GigaNameNFT` contracts. When a token is minted, transferred, or burnt, an inherited function called `_update()` is called. However, this function has an incorrect check that prevents the minting or burning process from completing if the token is a soulbound token. This can cause issues with the functionality of the contract. The report recommends updating the `_update()` function to include additional checks when minting or burning a token to ensure that the process can be completed correctly.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `GameNFT` contract is inherited by `GigaNoobNFT` and `GigaNameNFT` contracts, and when a token is minted, transferred, or burnt, the inherited `_update()` function (that overrides the `ERC721._update()`) is called, however, the function contains an invalid check when determining if a token is a soulbound, if a soulbound token is being minted, the check incorrectly prevents the minting/burning processes from completing:

```solidity
function _update(
        address to,
        uint256 tokenId,
        address auth
    )
        internal
        virtual
        override(
            ERC721
        ) returns (address)
    {

         if (beforeUpdateHandler != address(0)) {
            IERC721UpdateHandler(
                    beforeUpdateHandler
                ).update(
                address(this),
                to,
                tokenId,
                auth
            );
        }

        address prevOwner = _ownerOf(tokenId);

        //...
        bool isSoulbound = getDocBoolValue(tokenId, IS_SOULBOUND_CID);
        require(!isSoulbound, "GameNFT: Token is soulbound");
        //...
    }

```

## Recommendations

Update the `GameNFT._update()` function to add the following checks:

- when minting a token: verify that the previous owner is `address(0)` (indicating no prior owner).
- when burning a token: ensure that the recipient address (to) is `address(0)` (indicating the token is being burnt).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

