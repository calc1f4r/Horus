---
# Core Classification
protocol: DittoETH
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27484
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc
source_link: none
github_link: https://github.com/Cyfrin/2023-09-ditto

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
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - ubermensch
  - Bernd
---

## Vulnerability Title

Loss of ETH yield due to rounding error when updating the yield rate in the `updateYield` function

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibVault.sol#L92">https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibVault.sol#L92</a>


## Summary

Updating the vault's yield rate in the `LibVault.updateYield` function can lead to a loss of yield if the newly received ETH yield is small due to rounding errors.

## Vulnerability Details

The `updateYield` function in the `LibVault` library is called by the permissionless [`YieldFacet.updateYield`](https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/facets/YieldFacet.sol#L42) function and used to update the vault's yield rate from staking rewards earned by bridge contracts holding LSD.

The newly accumulated yield, i.e., ETH received since the last update, is calculated by subtracting the current `zethTotalNew` from the previously stored yield `zethTotal`, as seen in line 75 of the `updateYield` function.

[contracts/libraries/LibVault.sol#L92](https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibVault.sol#L92)

```solidity
62: function updateYield(uint256 vault) internal {
63:     AppStorage storage s = appStorage();
64:
65:     STypes.Vault storage Vault = s.vault[vault];
66:     STypes.VaultUser storage TAPP = s.vaultUser[vault][address(this)];
67:     // Retrieve vault variables
68:     uint88 zethTotalNew = uint88(getZethTotal(vault)); // @dev(safe-cast)
69:     uint88 zethTotal = Vault.zethTotal;
70:     uint88 zethCollateral = Vault.zethCollateral;
71:     uint88 zethTreasury = TAPP.ethEscrowed;
72:
73:     // Calculate vault yield and overwrite previous total
74:     if (zethTotalNew <= zethTotal) return;
75:     uint88 yield = zethTotalNew - zethTotal;
76:     Vault.zethTotal = zethTotalNew;
77:
78:     // If no short records, yield goes to treasury
79:     if (zethCollateral == 0) {
80:         TAPP.ethEscrowed += yield;
81:         return;
82:     }
83:
84:     // Assign yield to zethTreasury
85:     uint88 zethTreasuryReward = yield.mul(zethTreasury).divU88(zethTotal);
86:     yield -= zethTreasuryReward;
87:     // Assign tithe of the remaining yield to treasuryF
88:     uint88 tithe = yield.mulU88(vault.zethTithePercent());
89:     yield -= tithe;
90:     // Realize assigned yields
91:     TAPP.ethEscrowed += zethTreasuryReward + tithe;
92: ❌  Vault.zethYieldRate += yield.divU80(zethCollateral);
93:     Vault.zethCollateralReward += yield;
94: }
```

After determining the new yield (ETH), a fraction of the yield is assigned to the TAPP (treasury). Thereafter, the remaining yield is realized by adding it to the vault's yield rate (`zethYieldRate`), which is calculated by dividing the `yield` by the vault's short collateral, `zethCollateral`.

> [!NOTE]
> Both the `yield` and `zethCollateral` values are in 18 decimal precision due to tracking ETH balances.

By using the [`divU80` function](https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/PRBMathHelper.sol#L111), the `zethYieldRate` is calculated as $zethYieldRate = \frac{yield \cdot 10^{18}}{zethCollateral}$

However, if the numerator is smaller than the denominator, i.e., the received ETH yield is very small and the vault's collateral large enough, the result of the division will be rounded down to 0, leading to a loss of the remaining yield.

As anyone is able to call the public `YieldFacet.updateYield` function, this can be used to maliciously cause a loss of yield for all users if the newly received yield is small.

The following test case demonstrates the described rounding error:

<details>
  <summary><strong>Test case (click to reveal)</strong></summary>

```diff
diff --git a/test/Yield.t.sol b/test/Yield.t.sol
index cc770f2..8174aed 100644
--- a/test/Yield.t.sol
+++ b/test/Yield.t.sol
@@ -160,6 +160,19 @@ contract YieldTest is OBFixture {
         assertApproxEqAbs(ethEscrowed2 - ethEscrowed, 900000000000000000, MAX_DELTA);
     }

+    function test_DistributeYieldRoundingError() public {
+        fundLimitShortOpt(DEFAULT_PRICE, DEFAULT_AMOUNT * 10, receiver);
+        fundLimitBidOpt(DEFAULT_PRICE, DEFAULT_AMOUNT * 10, sender);
+        skip(yieldEligibleTime);
+        generateYield(65 wei);
+
+        assertEq(diamond.getVaultStruct(vault).zethCollateral, 6e19);
+
+        assertEq(diamond.getVaultStruct(vault).zethYieldRate, 0); // Vault's yield rate is 0 -> yield is lost
+
+        assertEq(diamond.getVaultUserStruct(vault, tapp).ethEscrowed, 6); // TAPP received 6 wei of yield
+    }
+
     function test_view_getTithe() public {
         assertEq(diamond.getTithe(vault), 0.1 ether);
     }
```

**How to run this test case:**

Save git diff to a file named `test.patch` and run with

```bash
git apply test.patch
forge test -vv --match-test "test_DistributeYieldRoundingError"
```

**Result:**

```bash
Running 1 test for test/Yield.t.sol:YieldTest
[PASS] test_DistributeYieldRoundingError() (gas: 791907)
Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 51.04ms

Ran 1 test suites: 1 tests passed, 0 failed, 0 skipped (1 total tests)
```

</details>

## Impact

Loss of LSD ETH yield for users of the same vault.

## Tools Used

Manual Review

## Recommendations

Consider storing the rounding error and applying the correcting factor (error stored) the next time, or alternatively, prevent (skip) updating the yield if the resulting yield is 0.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | DittoETH |
| Report Date | N/A |
| Finders | ubermensch, Bernd |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-09-ditto
- **Contest**: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc

### Keywords for Search

`vulnerability`

