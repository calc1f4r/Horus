---
# Core Classification
protocol: BendDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36876
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-benddao
source_link: https://code4rena.com/reports/2024-07-benddao
github_link: https://github.com/code-423n4/2024-07-benddao-findings/issues/44

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - bin2chen
---

## Vulnerability Title

[H-02] `isolateRepay()` lack of check `onBehalf == nftOwner`

### Overview


The bug report discusses an issue with the `isolateRepay()` function, which allows users to specify `nftTokenIds` and `onBehalf` when making a repayment. However, the current implementation does not restrict the `onBehalf` address to be the same as the NFT owner. This can be exploited by maliciously setting `onBehalf` to be different from the NFT owner, resulting in an `underflow` when the victim is liquidated or makes a repayment. This can prevent the victim from being repaid or liquidated. The recommended mitigation is to limit `onBehalf` to be the same as the NFT owner. The bug has been confirmed and fixed by the BendDAO team.

### Original Finding Content


When calling `isolateRepay()` we can specify `nftTokenIds` and `onBehalf`.
The current implementation just restricts `onBehalf!=address(0)` and does not restrict `onBehalf == nftOwner`.

```solidity
  function validateIsolateRepayBasic(
    InputTypes.ExecuteIsolateRepayParams memory inputParams,
    DataTypes.PoolData storage poolData,
    DataTypes.AssetData storage debtAssetData,
    DataTypes.AssetData storage nftAssetData
  ) internal view {
    validatePoolBasic(poolData);

    validateAssetBasic(debtAssetData);
    require(debtAssetData.assetType == Constants.ASSET_TYPE_ERC20, Errors.ASSET_TYPE_NOT_ERC20);

    validateAssetBasic(nftAssetData);
    require(nftAssetData.assetType == Constants.ASSET_TYPE_ERC721, Errors.ASSET_TYPE_NOT_ERC721);

@>  require(inputParams.onBehalf != address(0), Errors.INVALID_ONBEHALF_ADDRESS);

    require(inputParams.nftTokenIds.length > 0, Errors.INVALID_ID_LIST);
    require(inputParams.nftTokenIds.length == inputParams.amounts.length, Errors.INCONSISTENT_PARAMS_LENGTH);
    validateArrayDuplicateUInt256(inputParams.nftTokenIds);

    for (uint256 i = 0; i < inputParams.amounts.length; i++) {
      require(inputParams.amounts[i] > 0, Errors.INVALID_AMOUNT);
    }
  }
```

This way, we can maliciously specify `onBehalf!=nftOwner` and when the method is executed `userScaledIsolateBorrow[onBehalf]` will be maliciously reduced. When the victim makes a real repayment or is liquidated, it will not be repaid or liquidated due to insufficient `userScaledIsolateBorrow[onBehalf]` resulting in an `underflow`.

Example:
1. Alice depositERC721(NFT\_1).
2. Bob depositERC721(NFT\_2).
3. Alice isolateBorrow(NFT\_1, 100).
   -  userScaledIsolateBorrow\[alice] = 100
   -  loanData\[NFT\_1].scaledAmount = 100
4. Bob isolateBorrow(NFT\_2, 100)
   - userScaledIsolateBorrow\[bob] = 100
   - loanData\[NFT\_2].scaledAmount = 100
5. Alice malicious repay, isolateRepay(NFT\_1,amounts = 1, onBehalf = bob)
   - userScaledIsolateBorrow\[bob] = 99
6. When NFT\_2 be liquidated, isolateLiquidate(NFT\_2)
   - userScaledIsolateBorrow\[bob] = loanData\[NFT\_2].scaledAmount = 99 - 100 =====> underflow.

*Note: `isolateRedeem()` is similar.*

### Impact

Maliciously prevent being liquidated or repaid.

### Recommended Mitigation

limit `onBehalf==owner`:

```diff
  function validateIsolateRepayBasic(
    InputTypes.ExecuteIsolateRepayParams memory inputParams,
    DataTypes.PoolData storage poolData,
    DataTypes.AssetData storage debtAssetData,
    DataTypes.AssetData storage nftAssetData
  ) internal view {
    validatePoolBasic(poolData);

    validateAssetBasic(debtAssetData);
    require(debtAssetData.assetType == Constants.ASSET_TYPE_ERC20, Errors.ASSET_TYPE_NOT_ERC20);

    validateAssetBasic(nftAssetData);
    require(nftAssetData.assetType == Constants.ASSET_TYPE_ERC721, Errors.ASSET_TYPE_NOT_ERC721);

    require(inputParams.onBehalf != address(0), Errors.INVALID_ONBEHALF_ADDRESS);

    require(inputParams.nftTokenIds.length > 0, Errors.INVALID_ID_LIST);
    require(inputParams.nftTokenIds.length == inputParams.amounts.length, Errors.INCONSISTENT_PARAMS_LENGTH);
    validateArrayDuplicateUInt256(inputParams.nftTokenIds);

    for (uint256 i = 0; i < inputParams.amounts.length; i++) {
      require(inputParams.amounts[i] > 0, Errors.INVALID_AMOUNT);

+     DataTypes.ERC721TokenData storage tokenData = VaultLogic.erc721GetTokenData(
+       nftAssetData,
+       inputParams.nftTokenIds[i]
+     );
+     require(tokenData.owner == inputParams.onBehalf, Errors.ISOLATE_LOAN_OWNER_NOT_MATCH);
    }
  }
```

### Assessed type

Context

**[thorseldon (BendDAO) confirmed and commented](https://github.com/code-423n4/2024-07-benddao-findings/issues/44#issuecomment-2297884205):**
 > Fixed [here](https://github.com/BendDAO/bend-v2/commit/83b544354ec1dd2d630ceda347e0cefabd17d677).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | BendDAO |
| Report Date | N/A |
| Finders | bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-benddao
- **GitHub**: https://github.com/code-423n4/2024-07-benddao-findings/issues/44
- **Contest**: https://code4rena.com/reports/2024-07-benddao

### Keywords for Search

`vulnerability`

