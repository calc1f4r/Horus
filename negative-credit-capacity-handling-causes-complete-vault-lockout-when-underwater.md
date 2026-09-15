---
# Core Classification
protocol: Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49972
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl
source_link: none
github_link: https://github.com/Cyfrin/2025-01-zaros-part-2

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
finders_count: 3
finders:
  - smol_korok
  - cheatc0d33
  - qpzm
---

## Vulnerability Title

Negative Credit Capacity Handling Causes Complete Vault Lockout When Underwater

### Overview


The report discusses a bug in the VaultRouterBranch.sol file that causes a complete system lockout when a vault is underwater, meaning its debt exceeds its assets. This is due to a failure to properly handle negative credit capacity when converting from signed to unsigned values. The vulnerability causes critical vault functions to become completely unusable, such as withdrawals and redemptions. A proof of concept test is provided to demonstrate the failure of these functions. The bug can be fixed by modifying the `convertSd59x18ToTokenAmount` function to properly handle negative values. 

### Original Finding Content

## Summary

The `getVaultCreditCapacity` function in VaultRouterBranch.sol fails to properly handle underwater vaults where debt exceeds assets. When calculating negative credit capacity, the conversion from signed to unsigned values in `convertSd59x18ToTokenAmount` reverts, causing a complete system lockout of critical vault functions including withdrawals.

## Vulnerability Details

When a vault's debt exceeds its assets, credit capacity becomes negative. The system fails to handle this scenario in the following sequence:

```solidity
function getVaultCreditCapacity(uint128 vaultId) public view returns (uint256) {
    // Calculate total assets minus debt (can be negative)
    SD59x18 totalAssetsMinusVaultDebtX18 = totalAssetsX18.sub(vaultDebtInAssetsX18);

    // Attempts to convert negative value to unsigned - reverts
    return vault.collateral.convertSd59x18ToTokenAmount(totalAssetsMinusVaultDebtX18);
}
```

The core issue occurs in `Math.sol`:

```solidity
function convertSd59x18ToTokenAmount(uint8 decimals, SD59x18 amountX18) internal pure returns (uint256) {
    // Always reverts when amountX18 is negative
    return amountX18.intoUint256();
}
```

This causes critical vault functions to become completely unusable once a vault becomes underwater, as they all depend on `getVaultCreditCapacity`.

## Impact

1. **Sudden System Lockout**
   * When debt exceeds assets, all redemptions become impossible
   * No partial withdrawals allowed even if assets remain
   * Users completely locked out of withdrawing any funds

2. **Core Function Failure**
   * `getIndexTokenSwapRate` fails due to credit capacity revert
   * `getVaultAssetSwapRate` fails due to credit capacity revert
   * `redeem()` becomes completely unusable

## Proof of Concept

The following test demonstrates how vault functions fail completely when underwater:

```solidity
function test_UnderwaterVaultBehavior() public {
    UD60x18 price = ud60x18(2000e18);  // $2000 per ETH
    UD60x18 assets = ud60x18(100e18);  // 100 ETH = $200,000
    
    // Case 1: Healthy vault - $190,000 debt
    SD59x18 debt = sd59x18(190_000e18);
    ethVault.setMockState(assets, debt);
    uint256 capacity = getVaultCreditCapacity(vaultId);
    // Returns positive credit capacity, system functions normally
    
    // Case 2: Underwater vault - $210,000 debt
    debt = sd59x18(210_000e18);
    ethVault.setMockState(assets, debt);
    // Complete system lockout - all functions revert
    vm.expectRevert();
    getVaultCreditCapacity(vaultId);
    
    // Demonstrate critical function failures
    vm.expectRevert();
    vaultRouter.redeem(vaultId, requestId, minAssets);
}
```

## Tools Used

Manual Analysis, Foundry

## Recommendations

1. Modify `convertSd59x18ToTokenAmount` to properly handle negative values:

```solidity
function convertSd59x18ToTokenAmount(uint8 decimals, SD59x18 amountX18) 
    internal pure returns (int256) 
{
    if (Constants.SYSTEM_DECIMALS == decimals) {
        return amountX18.intoInt256();
    }
    return amountX18.intoInt256() / int256(10 ** (Constants.SYSTEM_DECIMALS - decimals));
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | smol_korok, cheatc0d33, qpzm |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

