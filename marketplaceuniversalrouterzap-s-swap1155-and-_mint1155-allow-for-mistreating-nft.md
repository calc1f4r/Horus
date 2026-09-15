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
solodit_id: 54559
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/473be50c-f610-474d-874d-e85e682ec81d
source_link: https://cdn.cantina.xyz/reports/cantina_nftx_aug2023.pdf
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

MarketplaceUniversalRouterZap 's swap1155() and _mint1155() allow for mistreating NFT type and freezing the tokens on the contract balance 

### Overview


This bug report is about a vulnerability in the code of a smart contract called MarketplaceUniversalRouterZap.sol. The contract has two functions, swap1155 and _mint1155, that both use the ERC-1155 standard for handling tokens. However, the contract also allows for the use of a different standard, ERC-721, and this can cause problems. If a user makes a mistake when using the contract and sends both ERC-1155 and ERC-721 tokens, the ERC-721 tokens can get stuck in the contract and become unusable. This is a medium severity issue, and the recommendation is to add code to check for the token type and prevent this from happening.

### Original Finding Content

## Vulnerability Analysis: MarketplaceUniversalRouterZap.sol

## Context
- MarketplaceUniversalRouterZap.sol#L380-L410
- MarketplaceUniversalRouterZap.sol#L521-L535

## Description
Similarly to core protocol NFT type issue 70, there is a possibility for mistreating the type of the Vault, as both functions follow the ERC-1155 path, while the Vault can be ERC-721 and treat the supplied ids without reverting, but differently (e.g., with amounts fixed to be 1).

### Code Snippet
```solidity
MarketplaceUniversalRouterZap.sol L380-L410
function swap1155(
...
) external payable onlyOwnerIfPaused {
    address vault = nftxVaultFactory.vault(vaultId);
    address assetAddress = INFTXVaultV3(vault).assetAddress();
    >> IERC1155(assetAddress).safeBatchTransferFrom(
        msg.sender,
        address(this),
        idsIn,
        amounts,
        ""
    );
    IERC1155(assetAddress).setApprovalForAll(vault, true);
    // Swap our tokens. Forcing to deduct vault fees
    >> uint256 ethFees = INFTXVaultV3(vault).swap{value: msg.value}(
        idsIn,
        amounts,
        idsOut,
        msg.sender,
        to,
        vTokenPremiumLimit,
        true
    );
}
```

As an example, Bob the user can supply to `MarketplaceUniversalRouterZap` ERC-1155 3 NFTs, while Vault, being of ERC-721 type, will fetch only 1 of them, with the remaining 2 stuck in the contract.

## Impact
User operational mistakes when dealing with NFTs supporting both ERC-1155 and ERC-721 can lead to permanent freeze of these tokens on the `MarketplaceUniversalRouterZap` balance. Given the low likelihood and high impact, the severity is set to medium.

## Recommendation
Consider directly controlling for the Vault type in `swap1155()` and `_mint1155()`, for example:

### Code Snippet
```solidity
MarketplaceUniversalRouterZap.sol L380-L410
function swap1155(
...
) external payable onlyOwnerIfPaused {
    address vault = nftxVaultFactory.vault(vaultId);
    + if (!INFTXVaultV3(vault).is1155()) revert WrongVaultType();
    address assetAddress = INFTXVaultV3(vault).assetAddress();
    IERC1155(assetAddress).safeBatchTransferFrom(
        msg.sender,
        address(this),
        idsIn,
        amounts,
        ""
    );
    IERC1155(assetAddress).setApprovalForAll(vault, true);
    // Swap our tokens. Forcing to deduct vault fees
    uint256 ethFees = INFTXVaultV3(vault).swap{value: msg.value}(
        idsIn,
        amounts,
        idsOut,
        msg.sender,
        to,
        vTokenPremiumLimit,
        true
    );
}
```

```solidity
MarketplaceUniversalRouterZap.sol L521-L535
function _mint1155(
    uint256 vaultId,
    uint256[] calldata ids,
    uint256[] calldata amounts
) internal returns (address vault, address assetAddress) {
    vault = nftxVaultFactory.vault(vaultId);
    + if (!INFTXVaultV3(vault).is1155()) revert WrongVaultType();
    assetAddress = INFTXVaultV3(vault).assetAddress();
    IERC1155(assetAddress).safeBatchTransferFrom(
        msg.sender,
        address(this),
        ids,
        amounts,
        ""
    );
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

