---
# Core Classification
protocol: Venus Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20785
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-venus
source_link: https://code4rena.com/reports/2023-05-venus
github_link: https://github.com/code-423n4/2023-05-venus-findings/issues/9

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
  - volodya
---

## Vulnerability Title

[M-16] Sometimes calculateBorrowerReward and calculateSupplierReward return incorrect results

### Overview


This bug report is about incorrect results being returned by `calculateBorrowerReward` and `calculateSupplierReward` functions. Whenever a user wants to know pending rewards they call `getPendingRewards`, sometimes it returns incorrect results. There is a bug inside `calculateBorrowerReward` and `calculateSupplierReward` code which is causing the issue. 

The bug is present in the original code of `rewardsDistributor` functions. The code has incorrect validation which is causing the issue. The recommended mitigation steps are to change the validation from `supplierIndex.mantissa == 0 && supplyIndex.mantissa > 0` to `supplierIndex.mantissa == 0 && supplyIndex.mantissa  >= rewardsDistributor.rewardTokenInitialIndex()` for `calculateSupplierReward` and from `borrowerIndex.mantissa == 0 && borrowIndex.mantissa > 0` to `borrowerIndex.mantissa == 0 && borrowIndex.mantissa >= rewardsDistributor.rewardTokenInitialIndex()` for `calculateBorrowerReward`. 

The assessed type of this bug is Invalid Validation. This has been confirmed by chechu (Venus).

### Original Finding Content


Sometimes `calculateBorrowerReward` and `calculateSupplierReward` return incorrect results.

### Proof of Concept

Whenever a user wants to know pending rewards they call `getPendingRewards`; sometimes, it returns incorrect results.

There is a bug inside `calculateBorrowerReward` and `calculateSupplierReward`

```solidity
    function calculateBorrowerReward(
        address vToken,
        RewardsDistributor rewardsDistributor,
        address borrower,
        RewardTokenState memory borrowState,
        Exp memory marketBorrowIndex
    ) internal view returns (uint256) {
        Double memory borrowIndex = Double({ mantissa: borrowState.index });
        Double memory borrowerIndex = Double({
            mantissa: rewardsDistributor.rewardTokenBorrowerIndex(vToken, borrower)
        });
//      @audit
//        if (borrowerIndex.mantissa == 0 && borrowIndex.mantissa >= rewardsDistributor.rewardTokenInitialIndex()) {
        if (borrowerIndex.mantissa == 0 && borrowIndex.mantissa > 0) {
            // Covers the case where users borrowed tokens before the market's borrow state index was set
            borrowerIndex.mantissa = rewardsDistributor.rewardTokenInitialIndex();
        }
        Double memory deltaIndex = sub_(borrowIndex, borrowerIndex);
        uint256 borrowerAmount = div_(VToken(vToken).borrowBalanceStored(borrower), marketBorrowIndex);
        uint256 borrowerDelta = mul_(borrowerAmount, deltaIndex);
        return borrowerDelta;
    }

```

[contracts/Lens/PoolLens.sol#L495](https://github.com/code-423n4/2023-05-venus/blob/9853f6f4fe906b635e214b22de9f627c6a17ba5b/contracts/Lens/PoolLens.sol#L495)

```solidity
    function calculateSupplierReward(
        address vToken,
        RewardsDistributor rewardsDistributor,
        address supplier,
        RewardTokenState memory supplyState
    ) internal view returns (uint256) {
        Double memory supplyIndex = Double({ mantissa: supplyState.index });
        Double memory supplierIndex = Double({
            mantissa: rewardsDistributor.rewardTokenSupplierIndex(vToken, supplier)
        });
//      @audit
//        if (supplierIndex.mantissa == 0 && supplyIndex.mantissa  >= rewardsDistributor.rewardTokenInitialIndex()) {
        if (supplierIndex.mantissa == 0 && supplyIndex.mantissa > 0) {
            // Covers the case where users supplied tokens before the market's supply state index was set
            supplierIndex.mantissa = rewardsDistributor.rewardTokenInitialIndex();
        }
        Double memory deltaIndex = sub_(supplyIndex, supplierIndex);
        uint256 supplierTokens = VToken(vToken).balanceOf(supplier);
        uint256 supplierDelta = mul_(supplierTokens, deltaIndex);
        return supplierDelta;
    }

```

[contracts/Lens/PoolLens.sol#L516](https://github.com/code-423n4/2023-05-venus/blob/9853f6f4fe906b635e214b22de9f627c6a17ba5b/contracts/Lens/PoolLens.sol#L516)

Inside `rewardsDistributor` original functions are written like this:

```solidity
    function _distributeSupplierRewardToken(address vToken, address supplier) internal {
...
        if (supplierIndex == 0 && supplyIndex >= rewardTokenInitialIndex) {
            // Covers the case where users supplied tokens before the market's supply state index was set.
            // Rewards the user with REWARD TOKEN accrued from the start of when supplier rewards were first
            // set for the market.
            supplierIndex = rewardTokenInitialIndex;
        }
...
    }
```

[contracts/Rewards/RewardsDistributor.sol#L340](https://github.com/code-423n4/2023-05-venus/blob/9853f6f4fe906b635e214b22de9f627c6a17ba5b/contracts/Rewards/RewardsDistributor.sol#L340)

```solidity
    function _distributeBorrowerRewardToken(
        address vToken,
        address borrower,
        Exp memory marketBorrowIndex
    ) internal {
...
        if (borrowerIndex == 0 && borrowIndex >= rewardTokenInitialIndex) {
            // Covers the case where users borrowed tokens before the market's borrow state index was set.
            // Rewards the user with REWARD TOKEN accrued from the start of when borrower rewards were first
            // set for the market.
            borrowerIndex = rewardTokenInitialIndex;
        }
...
}
```

[Rewards/RewardsDistributor.sol#L374](https://github.com/code-423n4/2023-05-venus/blob/9853f6f4fe906b635e214b22de9f627c6a17ba5b/contracts/Rewards/RewardsDistributor.sol#L374)

### Recommended Mitigation Steps

```diff
    function calculateSupplierReward(
        address vToken,
        RewardsDistributor rewardsDistributor,
        address supplier,
        RewardTokenState memory supplyState
    ) internal view returns (uint256) {
        Double memory supplyIndex = Double({ mantissa: supplyState.index });
        Double memory supplierIndex = Double({
            mantissa: rewardsDistributor.rewardTokenSupplierIndex(vToken, supplier)
        });
-        if (supplierIndex.mantissa == 0 && supplyIndex.mantissa > 0) {
+        if (supplierIndex.mantissa == 0 && supplyIndex.mantissa  >= rewardsDistributor.rewardTokenInitialIndex()) {
            // Covers the case where users supplied tokens before the market's supply state index was set
            supplierIndex.mantissa = rewardsDistributor.rewardTokenInitialIndex();
        }
        Double memory deltaIndex = sub_(supplyIndex, supplierIndex);
        uint256 supplierTokens = VToken(vToken).balanceOf(supplier);
        uint256 supplierDelta = mul_(supplierTokens, deltaIndex);
        return supplierDelta;
    }
```

```diff
    function calculateBorrowerReward(
        address vToken,
        RewardsDistributor rewardsDistributor,
        address borrower,
        RewardTokenState memory borrowState,
        Exp memory marketBorrowIndex
    ) internal view returns (uint256) {
        Double memory borrowIndex = Double({ mantissa: borrowState.index });
        Double memory borrowerIndex = Double({
            mantissa: rewardsDistributor.rewardTokenBorrowerIndex(vToken, borrower)
        });
-        if (borrowerIndex.mantissa == 0 && borrowIndex.mantissa > 0) {
+        if (borrowerIndex.mantissa == 0 && borrowIndex.mantissa >= rewardsDistributor.rewardTokenInitialIndex()) {
            // Covers the case where users borrowed tokens before the market's borrow state index was set
            borrowerIndex.mantissa = rewardsDistributor.rewardTokenInitialIndex();
        }
        Double memory deltaIndex = sub_(borrowIndex, borrowerIndex);
        uint256 borrowerAmount = div_(VToken(vToken).borrowBalanceStored(borrower), marketBorrowIndex);
        uint256 borrowerDelta = mul_(borrowerAmount, deltaIndex);
        return borrowerDelta;
    }
```

### Assessed type

Invalid Validation

**[chechu (Venus) confirmed](https://github.com/code-423n4/2023-05-venus-findings/issues/9#issuecomment-1560066298)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Venus Protocol |
| Report Date | N/A |
| Finders | volodya |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-venus
- **GitHub**: https://github.com/code-423n4/2023-05-venus-findings/issues/9
- **Contest**: https://code4rena.com/reports/2023-05-venus

### Keywords for Search

`vulnerability`

