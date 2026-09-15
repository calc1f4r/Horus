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
solodit_id: 54217
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
  - oakcobalt
---

## Vulnerability Title

checkVaultStatus() might cause chained liquidation DOS 

### Overview

See description below for full details.

### Original Finding Content

## Context

**File:** `RiskManager.sol#L118`  
**Description:** `callHookWithLock()` in `RiskManager::checkVaultStatus()` allows a vault’s governor to set checks on various vault states and revert when necessary. For example, a vault's governor might choose to revert `checkVaultStatus()` when a utilization cap is reached. This can be necessary for a nested vault where debt value has nested compounding or any interest-bearing underlying assets that increase total borrow without new borrows.

In any case, where `callHookWithLock()` in `checkVaultStatus()` reverts, this can have a chained effect on liquidation in all dependent vaults. Liquidation can be denied for all vaults that enlist the collateral vault as legal collateral.

## Flow Impacted

`RiskManager::liquidate() → executeLiquidation() → enforceCollateralTransfer() → evc.controlCollateral() → (collateral vault) Token::transfer() → initOperation()`

> Note: this adds vaultA's status check at the end of the liquidate transaction.

### Function Code

```solidity
// RiskManager.sol#L118
function checkVaultStatus() public virtual reentrantOK onlyEVCChecks returns (bytes4 magicValue) {
    // ...
    callHookWithLock(vaultCache.hookedOps, OP_VAULT_STATUS_CHECK, address(evc));
    magicValue = IEVCVault.checkVaultStatus.selector;
}
```

## Proof of Concept

1. Suppose `vaultB` enlists `vaultA` as one of the legal collateral assets. When `vaultA`'s `checkVaultStatus()` reverts (e.g., utilization cap is reached), this will revert `vaultB`'s liquidation calls during collateral transfer.

    ```
    VaultB: liquidate() → executeLiquidation() → enforceCollateralTransfer() → evc.controlCollateral() → VaultA: transfer() → VaultA: initOperation()
    ```

   As a result, when `vaultB` needs liquidation the most, any debt positions that include `vaultA` as collateral cannot be liquidated.

2. Suppose `vaultB` is a synthetic vault. `vaultB` enlists `vaultA` as one of the legal collateral assets. Similarly, `vaultB`’s borrow positions cannot be liquidated if `vaultA`’s `checkVaultStatus()` reverts. This will affect the pegging of the synthetic asset in `vaultB`.

3. `vaultB` enlists `vaultA` as one of the legal collateral assets, and `vaultC` enlists `vaultB` as one of the legal collateral assets. Similarly, `vaultB`'s debt positions cannot be liquidated if `vaultA`'s `checkVaultStatus()` reverts. This might cause `vaultB`'s total borrow to be undercollateralized. `vaultB`'s share price will be inflated. Because `vaultB` is a collateral vault in `vaultC`, `vaultC`'s debt positions can also be impacted.

## Recommendation

Consider allowing `checkVaultStatus` to fail in an emergency mode for liquidation, when `evc’s executionContext.isControlCollateralInProgress() == true`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | oakcobalt |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

