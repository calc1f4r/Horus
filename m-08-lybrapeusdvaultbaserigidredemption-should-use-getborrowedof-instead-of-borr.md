---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21153
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
github_link: https://github.com/code-423n4/2023-06-lybra-findings/issues/679

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
  - cccz
---

## Vulnerability Title

[M-08] `LybraPeUSDVaultBase.rigidRedemption` should use `getBorrowedOf` instead of `borrowed`

### Overview


This bug report is about the `LybraPeUSDVaultBase` smart contract. The return value of `getBorrowedOf` represents the user's debt, while `borrowed` only represents the user's borrowed funds and does not include fees. Using `borrowed` instead of `getBorrowedOf` in `rigidRedemption` results in two issues: 1) The requirement for the `peusdAmount` parameter is smaller than it actually is and 2) The calculated `providerCollateralRatio` is larger, so that `rigidRedemption` can be performed, even if the actual `providerCollateralRatio` is less than 100e18. The recommended mitigation step is to change the code to use `getBorrowedOf` instead of `borrowed`. The assessed type of this bug is an error. The bug has been confirmed by LybraFinance.

### Original Finding Content


In `LybraPeUSDVaultBase`, the return value of `getBorrowedOf` represents the user's debt, while `borrowed` only represents the user's borrowed funds and does not include fees.
Using `borrowed` instead of `getBorrowedOf` in `rigidRedemption` results in:

1.  The requirement for the `peusdAmount` parameter is smaller than it actually is.
2.  The calculated `providerCollateralRatio` is larger, so that `rigidRedemption` can be performed, even if the actual `providerCollateralRatio` is less than 100e18.

```solidity
    function rigidRedemption(address provider, uint256 peusdAmount) external virtual {
        require(configurator.isRedemptionProvider(provider), "provider is not a RedemptionProvider");
        require(borrowed[provider] >= peusdAmount, "peusdAmount cannot surpass providers debt");
        uint256 assetPrice = getAssetPrice();
        uint256 providerCollateralRatio = (depositedAsset[provider] * assetPrice * 100) / borrowed[provider];
        require(providerCollateralRatio >= 100 * 1e18, "provider's collateral ratio should more than 100%");
        _repay(msg.sender, provider, peusdAmount);
        uint256 collateralAmount = (((peusdAmount * 1e18) / assetPrice) * (10000 - configurator.redemptionFee())) / 10000;
        depositedAsset[provider] -= collateralAmount;
        collateralAsset.transfer(msg.sender, collateralAmount);
        emit RigidRedemption(msg.sender, provider, peusdAmount, collateralAmount, block.timestamp);
    }
```

### Proof of Concept

<https://github.com/code-423n4/2023-06-lybra/blob/5d70170f2c68dbd3f7b8c0c8fd6b0b2218784ea6/contracts/lybra/pools/base/LybraPeUSDVaultBase.sol#L157-L168>

### Recommended Mitigation Steps

Change to:

```diff
    function rigidRedemption(address provider, uint256 peusdAmount) external virtual {
        require(configurator.isRedemptionProvider(provider), "provider is not a RedemptionProvider");
-       require(borrowed[provider] >= peusdAmount, "peusdAmount cannot surpass providers debt");
+       require(getBorrowedOf(provider) >= peusdAmount, "peusdAmount cannot surpass providers debt");
        uint256 assetPrice = getAssetPrice();
-       uint256 providerCollateralRatio = (depositedAsset[provider] * assetPrice * 100) / borrowed[provider];
+       uint256 providerCollateralRatio = (depositedAsset[provider] * assetPrice * 100) / getBorrowedOf(provider);
        require(providerCollateralRatio >= 100 * 1e18, "provider's collateral ratio should more than 100%");
        _repay(msg.sender, provider, peusdAmount);
        uint256 collateralAmount = (((peusdAmount * 1e18) / assetPrice) * (10000 - configurator.redemptionFee())) / 10000;
        depositedAsset[provider] -= collateralAmount;
        collateralAsset.transfer(msg.sender, collateralAmount);
        emit RigidRedemption(msg.sender, provider, peusdAmount, collateralAmount, block.timestamp);
    }
```

### Assessed type

Error

**[LybraFinance confirmed](https://github.com/code-423n4/2023-06-lybra-findings/issues/679#issuecomment-1639677893)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: https://github.com/code-423n4/2023-06-lybra-findings/issues/679
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`vulnerability`

