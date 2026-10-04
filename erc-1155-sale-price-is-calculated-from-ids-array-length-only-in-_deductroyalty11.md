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
solodit_id: 54553
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/473be50c-f610-474d-874d-e85e682ec81d
source_link: https://cdn.cantina.xyz/reports/cantina_nftx_aug2023.pdf
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

protocol_categories:
  - dexes
  - cross_chain
  - rwa
  - leveraged_farming
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cccz
  - hyh
---

## Vulnerability Title

ERC-1155 sale price is calculated from ids array length only in _deductRoyalty1155() and can be signiﬁcantly overstated 

### Overview


This report is about a bug in a code file called MarketplaceUniversalRouterZap.sol. The bug causes the sale price to be overstated, which means users are losing more money than they should. This can be a big problem, especially when dealing with large amounts of money. The report recommends changing the code to use a different method for calculating the sale price, which should fix the bug.

### Original Finding Content

## Context
- **File:** MarketplaceUniversalRouterZap.sol#L667
- **Description:** Since amounts can differ, the length based salePrice can be overstated:
  - **Relevant Lines:** MarketplaceUniversalRouterZap.sol#L659-L671

## Function Overview
```solidity
function _deductRoyalty1155(
...
) internal returns (uint256 netRoyaltyAmount) {
    bool success = IERC2981(nft).supportsInterface(_INTERFACE_ID_ERC2981);
    if (success) {
        uint256 salePrice = netWethAmount / idsIn.length;
        for (uint256 i; i < idsIn.length; ) {
            (address receiver, uint256 royaltyAmount) = IERC2981(nft)
                .royaltyInfo(idsIn[i], salePrice);
            // Total NFT number needs to be used here instead.
        }
    }
}
```

## Impact
The `salePrice` is overstated, causing users to systematically lose the extra deducted funds. This loss can be substantial, especially when amounts can be arbitrarily large, leading to the price being overstated by magnitudes. For instance, an amount of 50 would mean that 50 times the price is used for royalty deduction.

Given the high likelihood of this issue and its significant impact, the severity is categorized as critical.

## Recommendation
Consider using the total NFT amount instead of the array length, as demonstrated in the `MarketplaceUniversalRouterZap`'s `_validate1155Ids()` function:
```solidity
function _validate1155Ids(
    uint256[] calldata ids,
    uint256[] calldata amounts
) internal pure returns (uint256 totalAmount) {
    // Sum the amounts for our emitted events
    for (uint i; i < ids.length; ) {
        unchecked {
            // simultaneously verifies that lengths of `ids` and `amounts` match.
            totalAmount += amounts[i];
            ++i;
        }
    }
}
```

### Suggested Code Change
```solidity
function _deductRoyalty1155(
...
) internal returns (uint256 netRoyaltyAmount) {
    bool success = IERC2981(nft).supportsInterface(_INTERFACE_ID_ERC2981);
    if (success) {
        // Change made here
        // - uint256 salePrice = netWethAmount / idsIn.length;
        // + uint256 salePrice = netWethAmount / _validate1155Ids(idsIn, amounts);
        for (uint256 i; i < idsIn.length; ) {
            (address receiver, uint256 royaltyAmount) = IERC2981(nft)
                .royaltyInfo(idsIn[i], salePrice);
        }
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | cccz, hyh |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_nftx_aug2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/473be50c-f610-474d-874d-e85e682ec81d

### Keywords for Search

`vulnerability`

