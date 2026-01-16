---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31530
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-02-01-TapiocaDAO.md
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

[H-03] AssetTotsDaiLeverageExecutor.getAsset() should use `redeem(collateralAmountIn)` instead of `redeem(convertToShares(collateralAmountIn))`

### Overview


This bug report discusses an issue with the AssetTotsDaiLeverageExecutor contract, which is causing users to receive less DAI when converting their sDAI. This is due to a function called `getAsset()` which is supposed to return the amount of the underlying asset, but instead is returning a lower amount. This is happening because the function is calling `convertToShares()` which is intended for converting assets to shares, but since sDAI is already a share, it is returning a lower amount. The recommended solution is to not call `convertToShares()` in `getAsset()`.

### Original Finding Content

**Severity**

**Impact:** Medium, users will get lesser DAI when converting their sDAI.

**Likelihood:** High, will happen every time `getAsset()` is called.

**Description**

sDai is an ERC4626 contract. Dai is the native asset and sDai is the share. When withdrawing assets, if `withdraw()` is called, the function takes in the asset value and returns the amount of the underlying asset. When `redeem()` is called, the function takes in the share value and returns the amount of the underlying asset. Usually, the shares are worth more than the asset, eg 1 sDai : 1.05 Dai.

In AssetTotsDaiLeverageExecutor.getAsset(), the function intends to unwrap tsDai > withdraw sDai > Dai > USDO. When withdrawing sDai, it calls `redeem(convertToShares())`.

```
//unwrap tsDai
        ITOFT(collateralAddress).unwrap(address(this), collateralAmountIn);
        //redeem from sDai
>       uint256 obtainedDai = ISavingsDai(sDaiAddress).redeem(
>           ISavingsDai(sDaiAddress).convertToShares(collateralAmountIn), address(this), address(this)
        );
```

Since sDai is already the share, by calling `convertToShares()`, it returns lesser Dai than intended since `convertToShares()` takes in an asset amount and returns the amount of the share. The user will get back lesser Dai and the remaining shares will be stuck in the AssetTotsDaiLeverageExecutor contract.

**Recommendations**

Recommend not calling `convertToShares()` in `getAsset()`

```
- uint256 obtainedDai = ISavingsDai(sDaiAddress).redeem(
-             ISavingsDai(sDaiAddress).convertToShares(collateralAmountIn), address(this), address(this)
+ uint256 obtainedDai = ISavingsDai(sDaiAddress).redeem(collateralAmountIn, address(this), address(this));
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-02-01-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

