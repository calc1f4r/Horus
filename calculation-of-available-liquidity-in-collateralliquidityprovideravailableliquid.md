---
# Core Classification
protocol: Securitize Onofframp Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64274
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
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
  - Hans
---

## Vulnerability Title

Calculation of available liquidity in `CollateralLiquidityProvider::availableLiquidity` assumes 1:1 ratio between collateral asset and liquidity tokens

### Overview


The `availableLiquidity` function in the `CollateralLiquidityProvider` contract is returning incorrect information about the available liquidity. This is because it assumes a 1:1 ratio between the collateral asset and the liquidity tokens, but this is not always the case due to fees, exchange rates, and other conversion mechanisms. This can lead to failed transactions and incorrect information for users and integrating systems. To fix this, the `availableLiquidity` function should query the external redemption contract for the actual liquidity that can be provided. Additionally, the function should call the internal `_availableLiquidity` function instead of duplicating its logic. The issue has been fixed in the code and verified by third-party auditors. 

### Original Finding Content

**Description:** The `CollateralLiquidityProvider::availableLiquidity` function incorrectly returns the balance of the collateral asset held by the collateral provider, assuming a 1:1 ratio between the collateral asset and the liquidity tokens that will actually be provided to redeemers. This assumption is flawed because the actual liquidity supplied to redeemers goes through the `externalCollateralRedemption.redeem()` function, which may apply fees, exchange rates, or other conversion mechanisms that break the 1:1 assumption.

```solidity
function availableLiquidity() external view returns (uint256) {
    return IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
}

function _availableLiquidity() private view returns (uint256) {
    return IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
}

function supplyTo(
    address redeemer,
    uint256 amount,
    uint256 minOutputAmount
) public whenNotPaused onlySecuritizeRedemption {
    if (amount > _availableLiquidity()) {
        revert InsufficientLiquidity(amount, _availableLiquidity());
    }

    // ... collateral transfer and redemption logic ...

    // The actual liquidity provided is calculated here, not the raw collateral amount
    uint256 assetsAfterExternalCollateralRedemptionFee = externalCollateralRedemption.calculateLiquidityTokenAmount(
        amount
    );

    liquidityToken.transfer(redeemer, assetsAfterExternalCollateralRedemptionFee);
}
```

When `CollateralLiquidityProvider::supplyTo` is called, the flow involves: transferring collateral assets from the collateral provider, calling `externalCollateralRedemption.redeem()` to convert collateral to liquidity tokens, calculating the actual liquidity amount using `externalCollateralRedemption.calculateLiquidityTokenAmount()`, and finally transferring the calculated liquidity tokens to the redeemer.
The `availableLiquidity()` function should query the external redemption contract to determine the actual liquidity that can be provided, rather than using the raw collateral asset balance. (e.g. `externalCollateralRedemption.calculateLiquidityTokenAmount(IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider));`

Additionally, the external `availableLiquidity()` function duplicates the logic of the internal `_availableLiquidity()` function instead of calling it, which goes against the intended design pattern and creates unnecessary code duplication.

**Impact:** Users and integrating systems may receive incorrect information about available liquidity, potentially leading to failed transactions when the actual convertible liquidity is less than the reported collateral asset balance.

**Recommended Mitigation:** Update the `availableLiquidity()` function to calculate the actual liquidity that can be provided by querying the external redemption contract, and fix the function to call the internal `_availableLiquidity()` function as intended:

```diff
function availableLiquidity() external view returns (uint256) {
-    return IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
+    return _availableLiquidity();
}

function _availableLiquidity() private view returns (uint256) {
-    return IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
+    uint256 collateralBalance = IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
+    return externalCollateralRedemption.calculateLiquidityTokenAmount(collateralBalance);
}
```

**Securitize:** Fixed in commit [1da35c](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/bf970d6cc4152c1b22e386b6acc6095aece8f12a) and [4a426e](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/4a426e689586a37cdcb463dba2f670fd58190ef9).

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Onofframp Bridge |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

