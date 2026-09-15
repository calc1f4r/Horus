---
# Core Classification
protocol: Ammplify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63191
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1054
source_link: none
github_link: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/349

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
  - tedox
---

## Vulnerability Title

M-12: `View::queryAssetBalances` does not account for JIT penalties

### Overview


The bug report discusses an issue found by a user named tedox in a code function called `View::queryAssetBalances`. This function is used to calculate the amount of assets a user would receive if they were to withdraw their funds at the moment. However, the value returned by this function is incorrect as it does not take into account potential JIT penalties that the position might incur. This is because when a user removes their maker position, the JIT penalty is calculated afterwards, but the view function does not properly account for this penalty. This can result in a mismatch between the actual withdrawal value and the value shown by the function, leading to the user receiving less funds than expected. The impact of this bug is considered medium, as it can result in incorrect return values of more than 0.01%. The suggested mitigation is to apply the JIT penalty to the view function for more accurate results. The protocol team has fixed this issue in their code.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/349 

## Found by 
tedox

### Summary

`View::queryAssetBalances` is used to query how much assets an user would receive if they were to withdraw their funds at the moment. However, the value returned will be wrong as it does not account for potential JIT penalties that the position might incur.


### Root Cause

When a user removes their maker position it calculates the amount of assets to return and then applies a JIT penalty if needed afterwards. 

[code](https://github.com/sherlock-audit/2025-09-ammplify/blob/main/Ammplify/src/facets/Maker.sol#L99-L127)
```solidity
    /// @inheritdoc IMaker
    function removeMaker(
        address recipient,
        uint256 assetId,
        uint160 minSqrtPriceX96,
        uint160 maxSqrtPriceX96,
        bytes calldata rftData
    ) external nonReentrant returns (address token0, address token1, uint256 removedX, uint256 removedY) {
        Asset storage asset = AssetLib.getAsset(assetId);
        require(asset.owner == msg.sender, NotMakerOwner(asset.owner, msg.sender));
        require(asset.liqType == LiqType.MAKER || asset.liqType == LiqType.MAKER_NC, NotMaker(assetId));
        PoolInfo memory pInfo = PoolLib.getPoolInfo(asset.poolAddr);
        Data memory data = DataImpl.make(pInfo, asset, minSqrtPriceX96, maxSqrtPriceX96, 0);
        WalkerLib.modify(pInfo, asset.lowTick, asset.highTick, data);
        // Settle balances.
        PoolWalker.settle(pInfo, asset.lowTick, asset.highTick, data);
        removedX = uint256(-data.xBalance); // These are definitely negative.
        removedY = uint256(-data.yBalance);
->      (removedX, removedY) = FeeLib.applyJITPenalties(asset, removedX, removedY);  //@audit JIT penalty applied to the full amount returned
        AssetLib.removeAsset(assetId);
        address[] memory tokens = pInfo.tokens();
        int256[] memory balances = new int256[](2);
        balances[0] = -int256(removedX); // We know they fit since they can only be less (in magnitude) than before.
        balances[1] = -int256(removedY);
        RFTLib.settle(recipient, tokens, balances, rftData);
        // Return values
        token0 = tokens[0];
        token1 = tokens[1];
    }
```

However, when the view function is used it does not properly account for the JIT penalty.

[code](https://github.com/sherlock-audit/2025-09-ammplify/blob/main/Ammplify/src/facets/View.sol#L74-L101)
```solidity
    /// Compute the token balances owned/owed by the position.
    /// @dev We separate the fee and liq balance so we can use the same method for fee earnings and total value.
    /// @return netBalance0 The amount of token0 owed to the position owner sans fees (Negative is owed by the owner).
    /// @return netBalance1 The amount of token1 owed to the position owner sans fees (Negative is owed by the owner).
    /// @return fees0 The amount of fees in token0 owed to a maker or owed by a taker depending on the liq type.
    /// @return fees1 The amount of fees in token1 owed to a maker or owed by a taker depending on the liq type.
    function queryAssetBalances(
        uint256 assetId
    ) external view returns (int256 netBalance0, int256 netBalance1, uint256 fees0, uint256 fees1) {
        Asset storage asset = AssetLib.getAsset(assetId);
        PoolInfo memory pInfo = PoolLib.getPoolInfo(asset.poolAddr);
        ViewData memory data = ViewDataImpl.make(pInfo, asset);
        ViewWalkerLib.viewAsset(pInfo, asset.lowTick, asset.highTick, data);
        if (asset.liqType == LiqType.TAKER) {
            uint256 vaultX = VaultLib.balanceOf(pInfo.token0, asset.xVaultIndex, assetId, false);
            uint256 vaultY = VaultLib.balanceOf(pInfo.token1, asset.yVaultIndex, assetId, false);
            // Balance and fees are owed, and vault balance is owned.
            netBalance0 = int256(vaultX) - int256(data.liqBalanceX);
            netBalance1 = int256(vaultY) - int256(data.liqBalanceY);
            fees0 = data.earningsX;
            fees1 = data.earningsY;
        } else {                                                              //@audit missing JIT penalty
            netBalance0 = int256(data.liqBalanceX);
            netBalance1 = int256(data.liqBalanceY);
            fees0 = data.earningsX;
            fees1 = data.earningsY;
        }
    }
```

This would cause a mismatch between the 2 values of more than 0.01% as long as the JIT penalty is more than 0.01% (which is likely the case)

### Internal Pre-conditions

1. The position is within the JIT penalty time

### External Pre-conditions

-

### Attack Path

1. User creates a maker position
2. Frontend queries `View::queryAssetBalances` in order to show the user how much they would be able to withdraw
3. User calls `removeMaker` through the frontend but receives less funds due to the JIT penalty

### Impact

Medium impact: 
>Issues that lead to getting incorrect return values (i.e. deviates from the withdrawal value of the asset by more than 0.01%) from the queryAssetBalance function (even if the appropriate input is used), which will lead to issues when executing other functions, may be considered valid with Medium severity at max.

### PoC

_No response_

### Mitigation

Apply the JIT penalty to the view function for more realistic results

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/itos-finance/Ammplify/pull/26






### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Ammplify |
| Report Date | N/A |
| Finders | tedox |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/349
- **Contest**: https://app.sherlock.xyz/audits/contests/1054

### Keywords for Search

`vulnerability`

