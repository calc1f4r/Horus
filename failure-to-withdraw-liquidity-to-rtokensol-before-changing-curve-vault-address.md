---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57237
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 7
finders:
  - tejaswarambhe
  - i3arba
  - petersr
  - 0xmystery
  - kirobrejka
---

## Vulnerability Title

Failure to Withdraw Liquidity to RToken.sol Before Changing Curve Vault Address

### Overview


This bug report discusses a vulnerability in the LendingPool contract that can lead to stranded liquidity and potential loss of user-accessible funds. The issue occurs when switching the Curve crvUSD vault address without first withdrawing reserve tokens from the old vault and transferring them to RToken.sol. This can cause the protocol to be unable to access these funds, leading to reduced yield generation and potential failures in user withdrawals. The report recommends refactoring the `setCurveVault()` function to include a step for withdrawing and transferring remaining reserve tokens from the old vault to RToken.sol. 

### Original Finding Content

## Summary

A vulnerability exists in the `setCurveVault()` function of the LendingPool contract. When switching the `Curve crvUSD vault` to a new address, the function fails to withdraw the remaining reserve tokens from the old vault and transfer them to RToken.sol. As a result, any liquidity left in the old vault becomes inaccessible to the protocol, leading to capital inefficiency and potential loss of user-accessible liquidity.

## Vulnerability Details

The `setCurveVault()` function updates the address of the Curve crvUSD vault without handling the reserve tokens already deposited in the old vault:

[LendingPool.sol#L699-L708](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/LendingPool/LendingPool.sol#L699-L708)

```solidity
    /**
     * @notice Sets the address of the Curve crvUSD vault
     * @param newVault The address of the new Curve vault contract
     */
    function setCurveVault(address newVault) external onlyOwner {
        require(newVault != address(0), "Invalid vault address");
        address oldVault = address(curveVault);
        curveVault = ICurveCrvUSDVault(newVault);
        emit CurveVaultUpdated(oldVault, newVault);
    }
```

This function does not withdraw any remaining reserve tokens from the old vault before updating the vault address. Once the vault is switched, the protocol can no longer access these funds, as evidenced below where `curveVault` is now a new vault address.&#x20;

As a matter of fact, the following function serving as the only way of getting back some reserve assets from the vault is meant to be internally invoked by either [`_ensureLiquidity()`](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/LendingPool/LendingPool.sol#L765) for its `requiredAmount` or [`_rebalanceLiquidity()`](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/LendingPool/LendingPool.sol#L789) for its `shortage` as far as the inputted `amount` is concerned. :

[LendingPool.sol#L809-L812](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/LendingPool/LendingPool.sol#L809-L812)

```solidity
    function _withdrawFromVault(uint256 amount) internal {
        curveVault.withdraw(amount, address(this), msg.sender, 0, new address[](0));
        totalVaultDeposits -= amount;
    }
```

There isn't a way where the protocol may manually pre-withdraw the reserve assets balance from the old vault prior to setting a new vault address. Neither is there a way to manually post-withdraw the reserve assets balance following the change of a new vault. This oversight leads to stranded liquidity and loss of user-accessible funds unless a full recovery process has been factored into the setter function.

## Impact

1. Stranded Reserve Tokens:
   Liquidity left in the old vault is no longer usable for withdrawals, borrowing, or yield generation.

2. User Withdrawal Failures:
   Since RToken.sol relies on sufficient reserve tokens to fulfill withdrawal requests, stranded liquidity could cause partial or failed withdrawals.

3. Protocol Yield Reduction:
   With a portion of the capital stuck in the old vault, the protocol’s ability to reinvest and generate yield is diminished, affecting long-term performance.

4. Protocol Vulnerability to Shortages:
   In scenarios of high withdrawal demand, stranded funds may force the protocol to sell or borrow liquidity from external sources under unfavorable conditions.

## Tools Used

Manual

## Recommendations

Consider the following refactoring:

[LendingPool.sol#L699-L708](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/LendingPool/LendingPool.sol#L699-L708)

```diff
    function setCurveVault(address newVault) external onlyOwner {
        require(newVault != address(0), "Invalid vault address");

+    // Withdraw all remaining reserve tokens from the old vault
+    if (address(curveVault) != address(0)) {
+        uint256 remainingBalance = curveVault.balanceOf(address(this));
+        if (remainingBalance > 0) {
+            // Withdraw and transfer reserve tokens to RToken.sol
+            curveVault.withdraw(remainingBalance, address(this), address(this), 0, new address[](0));
+            IERC20(reserve.reserveAssetAddress).safeTransfer(reserve.reserveRTokenAddress, remainingBalance);
+        }
+    }

        address oldVault = address(curveVault);
        curveVault = ICurveCrvUSDVault(newVault);
        emit CurveVaultUpdated(oldVault, newVault);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | tejaswarambhe, i3arba, petersr, 0xmystery, kirobrejka, foufrix, dobrevaleri |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

