---
# Core Classification
protocol: Plume Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53272
audit_firm: OtterSec
contest_link: https://plumenetwork.xyz/
source_link: https://plumenetwork.xyz/
github_link: https://github.com/plumenetwork/contracts

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
finders_count: 3
finders:
  - Nicholas R. Putra
  - Robert Chen
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Inconsistent Function Override Logic

### Overview


This bug report discusses a vulnerability in the ERC4626 implementation that can cause inconsistencies when certain functions are used. The issue arises when custom logic is defined in the YieldToken contract without overriding the dependent functions in the base ERC4626 contract. This can result in incorrect calculations for functions such as maxWithdraw, previewDeposit, previewMint, previewWithdraw, previewRedeem, and deposit/mint in ERC4626. To fix this issue, all dependent functions should be overridden to align with the custom logic defined in convertToShares and convertToAssets. This issue has been resolved in the 4f16028 patch.

### Original Finding Content

## Vulnerability Overview

The vulnerability concerns inconsistencies that arise when certain functions in the ERC4626 implementation define custom logic without overriding the dependent functions in the base ERC4626 contract to reflect this custom logic. 

## YieldToken Custom Logic

`YieldToken` redefines `convertToShares` and `convertToAssets` with custom logic that differs from the inherited ERC4626 contract’s expectations. These methods directly impact proportionality calculations between assets and shares.

```solidity
// smart-wallets/src/token/YieldToken.sol
function convertToShares(
    uint256 assets
) public view override(ERC4626, IComponentToken) returns (uint256 shares) {
    uint256 supply = totalSupply();
    uint256 totalAssets_ = totalAssets();
    if (supply == 0 || totalAssets_ == 0) {
        return assets;
    }
    return (assets * supply) / totalAssets_;
}

function convertToAssets(
    uint256 shares
) public view override(ERC4626, IComponentToken) returns (uint256 assets) {
    uint256 supply = totalSupply();
    if (supply == 0) {
        return shares;
    }
    return (shares * totalAssets()) / supply;
}
```

Functions such as `maxWithdraw`, `previewDeposit`, `previewMint`, `previewWithdraw`, and `previewRedeem` depend on `convertToShares` and `convertToAssets` for accurate calculations. However, the `YieldToken` implementation does not override these functions, resulting in their reliance on the base ERC4626 versions. 

Similarly, `deposit` and `mint` in ERC4626 also depend indirectly on `convertToShares` or `convertToAssets`.

## User Impact

When users interact with `YieldToken` through inherited methods, these methods, which utilize the ERC4626 logic that assumes the default behavior of `convertToShares` and `convertToAssets`, may yield incorrect results. This also applies to `ComponentToken::maxWithdraw`.

## Remediation

Override all the dependent functions to align their behavior with the custom logic defined in `convertToShares` and `convertToAssets` to ensure consistency across all operations.

## Patch

Resolved in commit `4f16028`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Plume Network |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Robert Chen, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://plumenetwork.xyz/
- **GitHub**: https://github.com/plumenetwork/contracts
- **Contest**: https://plumenetwork.xyz/

### Keywords for Search

`vulnerability`

