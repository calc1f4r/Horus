---
# Core Classification
protocol: Euler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54177
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55
source_link: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - t0x1c
---

## Vulnerability Title

In spite of correctly specifying minYieldBalance , incomplete slippage protection & missing deadline in liquidate() lead to loss 

### Overview

See description below for full details.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
The `liquidate()` function allows the liquidator to specify a `minYieldBalance` parameter. The protocol explains this to be the following: "The minimum acceptable amount of collateral to be transferred from violator to sender, in collateral balance units" as per the Natspec:

## File
`src/EVault/modules/Liquidation.sol`

```solidity
46: function liquidate(address violator, address collateral, uint256 repayAssets, uint256 minYieldBalance) 
47: public
48: virtual
49: nonReentrant
50: {
51: (VaultCache memory vaultCache, address liquidator) = initOperation(OP_LIQUIDATE, CHECKACCOUNT_CALLER);
52: 
53: LiquidationCache memory liqCache = 
54: calculateLiquidation(vaultCache, liquidator, violator, collateral, repayAssets);
55: 
56: executeLiquidation(vaultCache, liqCache, minYieldBalance);
57: }
```

## Natspec
### File
`src/EVault/IEVault.sol`

```solidity
283: /// @notice Attempts to perform a liquidation
284: /// @param violator Address that may be in collateral violation
285: /// @param collateral Collateral which is to be seized
286: /// @param repayAssets The amount of underlying debt to be transferred from violator to sender, in asset units (use,
287: /// max uint256 to repay the maximum possible amount).
288: /// @param minYieldBalance The minimum acceptable amount of collateral to be transferred from violator to sender, in,
289: /// collateral balance units (shares for vaults)
290: function liquidate(address violator, address collateral, uint256 repayAssets, uint256 minYieldBalance) external;
```

"The minimum acceptable amount of collateral" however is not enough to provide slippage protection even when the user correctly specifies `minYieldBalance`, as is shown in the following Proof of Concept section. It gives the liquidator very little control over the expected price ratio of debt & collateral. They should have been able to specify a `min_CollateralValue_By_DebtValue_Ratio`. Also, there is no provision to specify a deadline parameter while calling `liquidate()`.

## Impact
This means that if the transaction does not get executed immediately, which is quite common, then a price fluctuation in either the debt asset (upward) or the collateral asset (downward) can result in the liquidator taking on a much higher debt than they had anticipated. The additional absence of a deadline means this could remain in the mempool for a long time before getting executed at a worse price. There could even be a case where the debt finally gets transferred to the liquidator at a rate just above par and then even a slight price movement causes the caller to be either in loss or, even worse, get liquidated if LTV is breached.

## Proof of Concept
Consider the following example where the liquidator specifies `10e18` as the `minYieldBalance` so that he gets at least 10 units of collateral after the transaction. This, however, is not sufficient to protect him from an adverse price movement (the examples are reproduced with the same numbers in the coded proof of concept):

- Let's assume LTV of 90%. Bob borrows `8e18` against a collateral of `10e18` (10 collateral tokens priced at `1e18` each). The configuration for current `maxLiquidationDiscount` is `0.2e4`.
- Collateral price drops to `0.8e18` per token. Debt price rises to `1.1e18` per token. Hence, total `collateralValue = 8e18` while total `liabilityValue = 8.8e18`. Debt is now greater than permissible LTV, hence Bob can be liquidated.
- The liquidator expects a decent profit to be made after doing his calculations and hence calls `liquidate(violator, collateralAddr, type(uint256).max, 10e18);`.

Note the slippage protection specified by him of `10 tokens` which is respected in both cases, yet still dangerous for him in the second case. Also, for our examples, he maintains an initial collateral balance of `10` before calling `liquidate()`.

### Let's consider 2 cases (Expectation vs Reality):
- **Case-1: (Expectation)**
   - The `liabilityValue` transferred over to him in this case is `6.545454545454545447e18` while the `collateralAdjustedValue` transferred is `7.200000000000000007e18`.
   - He is comfortably below the max LTV and enjoys a healthy profit.

- **Case-2: (Reality)**
   - The transaction with call to `liquidate()` remains in the mempool for a few seconds or minutes. Meanwhile, the debt price drops to `1e18` per token.
   - When the transaction finally gets picked up, the `liabilityValue` transferred over to the liquidator in this case is `7.2e18` while the `collateralAdjustedValue` transferred is `7.200000000000000007e18`.
   - He is just below the allowed LTV and precariously close to being eligible for being liquidated even if a slight negative price movement happens in the next few seconds. Also, his profits are negligible or could even be negative after taking into account the gas cost.

## Apply the following patch and run `test_t0x1c_incompleteSlippage()` to see the results:
```diff
diff --git a/test/unit/evault/modules/Liquidation/basic.t.sol b/test/unit/evault/modules/Liquidation/basic.t.sol
index 2a0cc6e..b273a90 100644
--- a/test/unit/evault/modules/Liquidation/basic.t.sol
+++ b/test/unit/evault/modules/Liquidation/basic.t.sol
@@ -6,7 +6,7 @@ import {EVaultTestBase} from "../../EVaultTestBase.t.sol";
import {Events} from "../../../../../src/EVault/shared/Events.sol";
import {SafeERC20Lib} from "../../../../../src/EVault/shared/lib/SafeERC20Lib.sol";
import {IAllowanceTransfer} from "permit2/src/interfaces/IAllowanceTransfer.sol";
-
+import {TestERC20} from "../../../../mocks/TestERC20.sol";
import {console} from "forge-std/Test.sol";
import "../../../../../src/EVault/shared/types/Types.sol";
@@ -183,4 +183,101 @@ contract LiquidationUnitTest is EVaultTestBase {
assertEq(eTST.debtOf(borrower), 0);
assertEq(eTST2.balanceOf(borrower), 0);
}
+
+ function test_t0x1c_incompleteSlippage() public {
+ TestERC20 assetTST3;
+ assetTST3 = new TestERC20("Test Token 3", "TST3", 18, false);
+
+ IEVault eTST3 = IEVault(
+ factory.createProxy(address(0), true, abi.encodePacked(address(assetTST3), address(oracle),
unitOfAccount)), 
+ );
+
+ oracle.setPrice(address(assetTST3), unitOfAccount, 1e18);
+
+ startHoax(borrower);
+
+ assetTST3.mint(borrower, type(uint256).max);
+ assetTST3.approve(address(eTST3), type(uint256).max);
+
+ uint256 borrowerCollateralQty = 10e18;
+ eTST3.deposit(borrowerCollateralQty, borrower);
+
+ evc.enableCollateral(borrower, address(eTST3));
+ evc.enableController(borrower, address(eTST));
+ vm.stopPrank();
+
+ uint256 ltv = 0.9e4;
+ eTST.setLTV(address(eTST3), uint16(ltv), uint16(ltv), 0);
+
+ startHoax(borrower);
+ uint borrowAmt = 8e18;
+ eTST.borrow(borrowAmt, borrower);
+ assertEq(assetTST.balanceOf(borrower), borrowAmt);
+ vm.stopPrank();
+
+ uint depositInitialAmt = 10; // buffer collateral maintained by liquidator before liquidating
+
+ uint256 collateralDroppedPrice = 0.8e18;
+
+ uint256 snapshot = vm.snapshot();
+ console.log("\n============================== Case_1 (Liquidator ' s Expectation)
==============================================\n");
+
+ uint256 newDebtAssetPrice = 1.1e18; // Case_1 (asset price rises at the same time)
+
+ oracle.setPrice(address(assetTST3), unitOfAccount, collateralDroppedPrice);
+ oracle.setPrice(address(assetTST), unitOfAccount, newDebtAssetPrice);
+
+ startHoax(liquidator);
+
+ evc.enableCollateral(liquidator, address(eTST3));
+ evc.enableController(liquidator, address(eTST));
+
+ assetTST3.mint(liquidator, type(uint256).max);
+ assetTST3.approve(address(eTST3), type(uint256).max);
+ eTST3.deposit(depositInitialAmt, liquidator);
+
+ uint prevBal1 = eTST3.balanceOf(liquidator);
+ eTST.liquidate(borrower, address(eTST3), type(uint256).max, 10e18); // @audit-info : user has provided ` minYieldBalance = 10 tokens `,
+
+ (uint256 collateralValueL, uint256 liabilityValueL) = eTST.accountLiquidity(liquidator, false);
+
+ emit log_named_decimal_uint("debt balance of liquidator =", eTST.debtOf(liquidator), 18);
+ emit log_named_decimal_uint("debtValue of liquidator =", newDebtAssetPrice * eTST.debtOf(liquidator) / 1e18, 18);
+ emit log_named_decimal_uint("collateral value received by liquidator =", collateralDroppedPrice * (eTST3.balanceOf(liquidator) - prevBal1) / 1e18, 18);
+ emit log_named_decimal_uint("collateral balance received by liquidator =", eTST3.balanceOf(liquidator) - prevBal1, 18);
+ emit log_named_decimal_uint("liquidator ' s total collateralAdjustedValue =", collateralValueL, 18);
+ emit log_named_decimal_uint("remaining debt of borrower =", eTST.debtOf(borrower), 18);
+ emit log_named_decimal_uint("collateral balance of borrower =", eTST3.balanceOf(borrower), 18);
+
+
+ console.log("\n\n============================== Case_2 (Reality)
==============================================\n");
+
+ vm.revertTo(snapshot);
+ newDebtAssetPrice = 1e18; // Case_2 (no change)
+
+ oracle.setPrice(address(assetTST3), unitOfAccount, collateralDroppedPrice);
+ oracle.setPrice(address(assetTST), unitOfAccount, newDebtAssetPrice);
+
+ startHoax(liquidator);
+
+ evc.enableCollateral(liquidator, address(eTST3));
+ evc.enableController(liquidator, address(eTST));
+
+ assetTST3.mint(liquidator, type(uint256).max);
+ assetTST3.approve(address(eTST3), type(uint256).max);
+ eTST3.deposit(depositInitialAmt, liquidator);
+
+ prevBal1 = eTST3.balanceOf(liquidator);
+ eTST.liquidate(borrower, address(eTST3), type(uint256).max, 10e18); // @audit-info : user has provided ` minYieldBalance = 10 tokens `,
+
+ (collateralValueL, liabilityValueL) = eTST.accountLiquidity(liquidator, false);
+
+ emit log_named_decimal_uint("debt balance of liquidator =", eTST.debtOf(liquidator), 18);
+ emit log_named_decimal_uint("debtValue of liquidator =", newDebtAssetPrice * eTST.debtOf(liquidator) / 1e18, 18);
+ emit log_named_decimal_uint("collateral value received by liquidator =", collateralDroppedPrice * (eTST3.balanceOf(liquidator) - prevBal1) / 1e18, 18);
+ emit log_named_decimal_uint("collateral balance received by liquidator =", eTST3.balanceOf(liquidator) - prevBal1, 18);
+ emit log_named_decimal_uint("liquidator ' s total collateralAdjustedValue =", collateralValueL, 18);
+ emit log_named_decimal_uint("remaining debt of borrower =", eTST.debtOf(borrower), 18);
+ emit log_named_decimal_uint("collateral balance of borrower =", eTST3.balanceOf(borrower), 18);
+ }
}
```

## Output
```plaintext
Ran 1 test for test/unit/evault/modules/Liquidation/basic.t.sol:LiquidationUnitTest
[PASS] test_t0x1c_incompleteSlippage() (gas: 4877933)
```

## Logs
```plaintext
============================== Case_1 (Liquidator ' s Expectation) ==============================================
debt balance of liquidator =: 5.950413223140495861
debtValue of liquidator =: 6.545454545454545447 <-------
collateral value received by liquidator =: 8.000000000000000000
collateral balance received by liquidator =: 10.000000000000000000 --------> equals 10 tokens i.e. ` minYieldBalance ` hence tx does not revert.
liquidator ' s total collateralAdjustedValue =: 7.200000000000000007 <------- Ample gap between this and the above debtValue. Liquidator is quite safe from liquidation.
remaining debt of borrower =: 0.000000000000000000
collateral balance of borrower =: 0.000000000000000000
============================== Case_2 (Reality) ==============================================
debt balance of liquidator =: 7.200000000000000000
debtValue of liquidator =: 7.200000000000000000 <------- higher debtValue than Case_1; lower profits. Might even be a loss after gas costs.
collateral value received by liquidator =: 8.000000000000000000
collateral balance received by liquidator =: 10.000000000000000000 --------> equals 10 tokens i.e. ` minYieldBalance ` hence tx does not revert.
liquidator ' s total collateralAdjustedValue =: 7.200000000000000007 <------- Precariously close to the above debtValue. Liquidator can be liquidated even if a slight negative price movement happens in next few seconds.
remaining debt of borrower =: 0.000000000000000000
collateral balance of borrower =: 0.000000000000000000
```

## Recommendation
Allow the caller to specify the lowest `min_CollateralValue_By_DebtValue_Ratio` they are comfortable with and also the deadline timestamp. If either are violated, revert the transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | t0x1c |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

