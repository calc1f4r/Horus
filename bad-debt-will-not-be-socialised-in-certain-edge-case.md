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
solodit_id: 54142
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
finders_count: 2
finders:
  - Audittens
  - T1MOH
---

## Vulnerability Title

Bad debt will not be socialised in certain edge case 

### Overview

See description below for full details.

### Original Finding Content

## Liquidation.sol Overview

## Context
*File:* Liquidation.sol#L79-L92

## Description
At the end of the liquidation process, debt is socialized when the liquidatee has no liquidatable collateral but still has debt:

```solidity
function executeLiquidation(VaultCache memory vaultCache, LiquidationCache memory liqCache, uint256 minYieldBalance) private {
    // ...
    // Handle debt socialization
    if (
        vaultCache.configFlags.isNotSet(CFG_DONT_SOCIALIZE_DEBT) && 
        liqCache.liability > liqCache.repay && 
        checkNoCollateral(liqCache.violator, liqCache.collaterals) // <<<
    ) {
        Assets owedRemaining = liqCache.liability.subUnchecked(liqCache.repay);
        decreaseBorrow(vaultCache, liqCache.violator, owedRemaining);
        // decreaseBorrow emits Repay without any assets entering the vault. Emit Withdraw from 
        // and to zero address to cover the missing amount for offchain trackers.
        emit Withdraw(liqCache.liquidator, address(0), address(0), owedRemaining.toUint(), 0);
        emit DebtSocialized(liqCache.violator, owedRemaining.toUint());
    }
    // ...
}
```

### Parameter Submission for Liquidation
To perform a liquidation, the liquidator must submit specific parameters. The following sanity checks are performed:

```solidity
function calculateLiquidation(
    VaultCache memory vaultCache,
    address liquidator,
    address violator,
    address collateral,
    uint256 desiredRepay
) private view returns (LiquidationCache memory liqCache) {
    // ...
    // Checks
    // Same account self-liquidation is not allowed
    if (liqCache.violator == liqCache.liquidator) revert E_SelfLiquidation();
    // Only liquidate trusted collaterals to ensure yield transfer has no side effects.
    if (!isRecognizedCollateral(liqCache.collateral)) revert E_BadCollateral(); // <<<
    // Verify this vault is the controller for the violator
    validateController(liqCache.violator);
    // Violator must have enabled the collateral to be transferred to the liquidator
    if (!isCollateralEnabled(liqCache.violator, liqCache.collateral)) revert E_CollateralDisabled(); // <<<
    // Violator's health check must not be deferred, meaning no prior operations on violator's account
    // would possibly be forgiven after the enforced collateral transfer to the liquidator
    if (isAccountStatusCheckDeferred(violator)) revert E_ViolatorLiquidityDeferred();
    // A cool-off time must elapse since successful account status check in order to mitigate self-liquidation attacks
    if (isInLiquidationCoolOff(violator)) revert E_LiquidationCoolOff();
    // ...
}
```

### This process ensures:
1. The liquidated asset must be recognized for liquidation and enabled by the liquidatee in EVC.
2. To socialize bad debt, the user must have liquidatable enabled collateral.

### Issue
There exists a scenario where:
1. The user deposits collateral XYZ.
2. The user borrows an asset against XYZ.
3. XYZ collateral is acknowledged to have a critical vulnerability and is immediately removed via `Governance.clearLTV`:

```solidity
/// @inheritdoc IGovernance
/// @dev When LTV configuration is cleared, attempt to liquidate the collateral will revert.
function clearLTV(address collateral) public virtual nonReentrant governorOnly {
    uint16 originalLTV = getLTV(collateral, true).toUint16();
    vaultStorage.ltvLookup[collateral].clear();
    emit GovSetLTV(collateral, 0, 0, originalLTV, 0, 0, false);
}
```

As a result, the user has only worthless non-liquidatable collateral and debt. Therefore, this bad debt cannot be socialized due to the sanity checks in `Liquidation.calculateLiquidation()`.

## Recommendation
Introduce a method to socialize bad debt when the user does not have liquidatable enabled collateral.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | Audittens, T1MOH |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

