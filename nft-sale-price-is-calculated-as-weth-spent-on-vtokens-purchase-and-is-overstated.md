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
solodit_id: 54556
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

NFT sale price is calculated as WETH spent on vTokens purchase and is overstated this way in royalty deductions 

### Overview


In this bug report, the user has reported that there is a problem with the `wethSpent` variable in the `MarketplaceUniversalRouterZap.sol` file. This variable is used to calculate the amount spent on vTokens, but it is not taking into account all of the vTokens that are used for NFT purchases. This leads to an overstatement of the royalty amounts, as the actual sale price is lower than what is being calculated. This bug can have a high impact on users, as they may be losing extra funds due to this overstatement. The recommendation is to calculate the exact price of the tokens purchased to ensure that the `wethSpent` variable is accurate. 

### Original Finding Content

## Context
- `MarketplaceUniversalRouterZap.sol#L228-L250`
- `MarketplaceUniversalRouterZap.sol#L465-L502`

## Description
The `wethSpent` is the amount spent on vTokens, not all of which are used for NFT purchases. In fact, the amount of vTokens left is uncapped and can be arbitrarily large. This leads to overstated royalty amounts, as the actual sale price is lower than `wethSpent / tokenCount`, which is used in the `_deductRoyalty()` and `_deductRoyalty1155()` functions.

## MarketplaceUniversalRouterZap.sol#L228-L250
```solidity
// swap WETH to vTokens
uint256 iniWETHBal = WETH.balanceOf(address(this));
address vault = nftxVaultFactory.vault(vaultId);
_swapTokens(address(WETH), vault, executeCallData);
uint256 wethSpent = iniWETHBal - WETH.balanceOf(address(this));
uint256 wethLeft = msg.value - wethSpent;
// redeem NFTs. Forcing to deduct vault fees
TransferLib.unSafeMaxApprove(address(WETH), vault, wethLeft);
uint256 wethFees = INFTXVaultV3(vault).redeem(
    idsOut,
    to,
    wethLeft,
    vTokenPremiumLimit,
    true
);
uint256 netRoyaltyAmount;
if (deductRoyalty) {
    address assetAddress = INFTXVaultV3(vault).assetAddress();
    netRoyaltyAmount = _deductRoyalty(assetAddress, idsOut, wethSpent);
}
```

## MarketplaceUniversalRouterZap.sol#L465-L502
```solidity
// swap some WETH to vTokens
uint256 iniWETHBal = WETH.balanceOf(address(this));
address vault = nftxVaultFactory.vault(params.vaultId);
_swapTokens(address(WETH), vault, params.executeToVTokenCallData);
uint256 wethLeft = WETH.balanceOf(address(this));
uint256 wethSpent = iniWETHBal - wethLeft;
// redeem NFTs
TransferLib.unSafeMaxApprove(address(WETH), vault, wethLeft);
uint256 wethFees = INFTXVaultV3(vault).redeem(
    params.idsOut,
    params.to,
    wethLeft,
    params.vTokenPremiumLimit,
    true
);
uint256 netRoyaltyAmount;
if (params.deductRoyalty) {
    address assetAddress = INFTXVaultV3(vault).assetAddress();
    netRoyaltyAmount = _deductRoyalty(
        assetAddress,
        params.idsOut,
        wethSpent
    );
}
// transfer vToken dust and remaining WETH balance
_transferDust(vault, true);
emit Buy(
    params.idsOut,
    wethSpent + wethFees + netRoyaltyAmount,
    params.to,
    netRoyaltyAmount
);
```

## Impact
The `netRoyaltyAmount` is overstated, causing users to systematically lose the extra deducted funds. Given the high likelihood and medium impact, the severity is considered high.

## Recommendation
Consider calculating the exact price of the tokens purchased, for example:

```solidity
uint256 constant BASE = 10 ** 18;

// swap WETH to vTokens
uint256 iniWETHBal = WETH.balanceOf(address(this));
address vault = nftxVaultFactory.vault(vaultId);
(uint256 vTokenAmount, ) = _swapTokens(address(WETH), vault, executeCallData);
if (vTokenAmount < idsOut.length * BASE) revert NotEnoughFundsForRedeem();
uint256 wethSpent = iniWETHBal - WETH.balanceOf(address(this));
uint256 wethLeft = msg.value - wethSpent;
// redeem NFTs. Forcing to deduct vault fees
TransferLib.unSafeMaxApprove(address(WETH), vault, wethLeft);
uint256 wethFees = INFTXVaultV3(vault).redeem(
    idsOut,
    to,
    wethLeft,
    vTokenPremiumLimit,
    true
);
// the (1 - idsOut.length * BASE / vTokenAmount) share of wethSpent is not spend,
// but swapped to vTokens and returned to the caller via _transferDust() below
wethSpent = (wethSpent * idsOut.length * BASE) / vTokenAmount;
uint256 netRoyaltyAmount;
if (deductRoyalty) {
    address assetAddress = INFTXVaultV3(vault).assetAddress();
    netRoyaltyAmount = _deductRoyalty(assetAddress, idsOut, wethSpent);
}
// transfer vToken dust and remaining WETH balance
_transferDust(vault, true);
emit Buy(
    idsOut,
    wethSpent + wethFees + netRoyaltyAmount,
    to,
    netRoyaltyAmount
);
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

