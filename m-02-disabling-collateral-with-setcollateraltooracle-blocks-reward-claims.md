---
# Core Classification
protocol: Tanssi_2025-04-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63292
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Disabling collateral with `setCollateralToOracle()` blocks reward claims

### Overview


This bug report is about a problem that occurs when calling a specific function on a contract called "Middleware". This function, called "setCollateralToOracle", removes the associated oracle for a collateral, which is a type of asset used in the contract. This causes a critical issue where vaults, which are accounts that use this collateral, are unable to claim rewards. This is because the function that distributes rewards relies on the oracle address, and if it is removed, the function fails and prevents any rewards from being claimed. 

The severity of this bug is high, meaning it has a significant impact on the functionality of the contract. However, the likelihood of it occurring is low. 

To fix this issue, the report recommends disallowing the removal of the oracle address unless a mechanism is in place to safely handle rewards for historical vaults. They also suggest introducing a "retired" state for collaterals, which would allow historical rewards to be claimed while preventing new vaults from using the disabled collateral. Additionally, the report suggests caching oracle prices per epoch to avoid depending on live price feeds for historical calculations. 

The report concludes by stating that this issue highlights a dependency on live oracle data even for historical calculations and recommends that any administrative or governance operations that affect the oracle address should ensure backward compatibility for reward calculations.

### Original Finding Content


## Severity

**Impact:** High  

**Likelihood:** Low

## Description

Calling `setCollateralToOracle(collateral, address(0))` on `Middleware` disables the collateral by removing its associated oracle. It introduces a critical issue: **vaults that used this collateral prevent their operators from claiming rewards**.
```solidity
    function claimRewards(
        ClaimRewardsInput calldata input
    ) external nonReentrant returns (uint256 amount) {
        --Snipped--
        _distributeRewardsToStakers(
            eraRoot_.epoch, input.eraIndex, stakerAmount, recipient, middlewareAddress, tokenAddress, input.data
        );
    }

   function _distributeRewardsToStakers(
        uint48 epoch,
        uint48 eraIndex,
        uint256 stakerAmount,
        address operator,
        address middlewareAddress,
        address tokenAddress,
        bytes calldata data
    ) private {
        --Snipped--
        uint256[] memory amountPerVault = _getRewardsAmountPerVault(
            operatorVaults, totalVaults, epochStartTs, operator, middlewareAddress, stakerAmount
        );

        _distributeRewardsPerVault(epoch, eraIndex, tokenAddress, totalVaults, operatorVaults, amountPerVault, data);
    }
```
The problem arises during `claimRewards()` execution. This function calls `_distributeRewardsToStakers()`, which relies on `stakeToPower()` to calculate vault power. `stakeToPower()` fetches the oracle address via `collateralToOracle()`. If the mapping returns `address(0)`, the function reverts, blocking the entire reward claim process.


## Recommendations

- **Disallow setting `collateralToOracle` to `address(0)`** unless a mechanism is in place to safely handle rewards for historical vaults.
- Introduce a **"retired" state for collaterals**, allowing historical rewards to be claimed while preventing new vaults from using the disabled collateral.
- Consider **caching oracle prices per epoch** to avoid depending on live price feeds for historical calculations.

Additional Notes

This issue reflects a systemic dependency on live oracle data even for historical accounting. Administrative or governance operations that affect `collateralToOracle` should ensure backward compatibility for reward calculations.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tanssi_2025-04-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

