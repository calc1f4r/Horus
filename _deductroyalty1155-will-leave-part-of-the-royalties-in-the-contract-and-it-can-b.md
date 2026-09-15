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
solodit_id: 54554
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

_deductRoyalty1155 will leave part of the royalties in the contract and it can be taken out by other users 

### Overview


This bug report is about a code in MarketplaceUniversalRouterZap.sol that calculates royalties for ERC1155 tokens. The code currently calculates royalties as `royaltyAmount * amount`, but only `royaltyAmount` is sent to the owner while the rest stays in the contract. This can lead to an incorrect calculation of the remaining royalties. The recommendation is to change the code to a new function that properly calculates and sends the full amount of royalties to the owner. The bug can also cause all WETH in the contract to be sent to a user if they call the `buyNFTsWithETH` function.

### Original Finding Content

## Context
- MarketplaceUniversalRouterZap.sol#L672-L676
- MarketplaceUniversalRouterZap.sol#L358-L370

## Description
`_deductRoyalty1155` collects royalties from ERC1155, but in the code below, the royalties are calculated as `royaltyAmount * amount`. However, only the `royaltyAmount` will be sent to the royalty owner, and the rest of the royalties of `royaltyAmount * amount - 1` will be left in the contract.

```solidity
netRoyaltyAmount += royaltyAmount * amounts[i];
if (royaltyAmount > 0) {
    WETH.transfer(receiver, royaltyAmount);
}
...
if (deductRoyalty) {
    netRoyaltyAmount = _deductRoyalty1155(
        assetAddress,
        idsIn,
        amounts,
        wethAmount
    );
}
wethAmount -= (wethFees + netRoyaltyAmount); // if underflow, then revert desired

// convert WETH to ETH and send remaining ETH to `to`
_wethToETHResidue(to, wethAmount);
```

Other users can call the `buyNFTsWithETH`, in `_allWethToETHResidue` all WETH in the contract will be sent to the user.

```solidity
function _allWethToETHResidue(
    address to
) internal returns (uint256 wethAmount) {
    wethAmount = WETH.balanceOf(address(this));
    _wethToETHResidue(to, wethAmount);
}
```

## Recommendation
Change to:

```solidity
function _deductRoyalty1155(
    address nft,
    uint256[] calldata idsIn,
    uint256[] calldata amounts,
    uint256 netWethAmount
) internal returns (uint256 netRoyaltyAmount) {
    bool success = IERC2981(nft).supportsInterface(_INTERFACE_ID_ERC2981);
    if (success) {
        uint256 salePrice = netWethAmount / idsIn.length;
        for (uint256 i; i < idsIn.length; ) {
            (address receiver, uint256 royaltyAmount) = IERC2981(nft)
            .royaltyInfo(idsIn[i], salePrice);
            netRoyaltyAmount += royaltyAmount * amounts[i];
            if (royaltyAmount > 0) {
                WETH.transfer(receiver, royaltyAmount * amounts[i]);
            }
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

