---
# Core Classification
protocol: Liquid Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43678
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm1el4vjp00019d2nzombxfzp
source_link: none
github_link: https://github.com/Cyfrin/2024-09-stakelink

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 8olidity
  - ald
---

## Vulnerability Title

Potential Deposit Reverts Due to Removed Operator Vaults

### Overview

See description below for full details.

### Original Finding Content

## Summary

The `_depositToVaults` function in the `OperatorVCS::deposit` process lacks a mechanism to prevent deposits into vaults that have been removed from Chainlink's staking contract but not yet removed from the operator strategy. Since `removeVault` can only be called after the unbonding period ends, the function may attempt to deposit into a removed vault, causing transaction reverts that halt the deposit process.

## Vulnerability Details

When a vault is removed from Chainlink's staking contract, it must also be removed from the operator strategy by calling `queueVaultRemoval` followed by `removeVault`. However, `removeVault` cannot be executed immediately until the unbonding period concludes. This creates a delay where the vault remains in the operator strategy but has already been marked for removal in the Chainlink staking contract. If `_depositToVaults` attempts to deposit into such a vault, the Chainlink contract will revert the transaction.&#x20;

The `_depositToVaults` function handles deposits into vault groups as well as vaults that do not belong to a group. When depositing to group vaults, the function checks whether the vault has been removed:

```Solidity
        if (canDeposit != 0 && vaultIndex != group.withdrawalIndex && !vault.isRemoved()) {
            if (deposits < _minDeposits && toDeposit < (_minDeposits - deposits)) {
                break;
            }
```

<https://github.com/Cyfrin/2024-09-stakelink/blob/f5824f9ad67058b24a2c08494e51ddd7efdbb90b/contracts/linkStaking/base/VaultControllerStrategy.sol#L209>

However, when the function reaches the section where it deposits into vaults that do not yet belong to a group, it does not check if the vault has been removed:

```Solidity
    while (i < numVaults) {
        IVault vault = vaults[i];
        uint256 deposits = vault.getPrincipalDeposits();
        uint256 canDeposit = _maxDeposits - deposits;

        // cannot leave a vault with less than minimum deposits
        if (deposits < _minDeposits && toDeposit < (_minDeposits - deposits)) {
            break;
        }

        if (toDeposit > canDeposit) {
            vault.deposit(canDeposit);
            toDeposit -= canDeposit;
```

<https://github.com/Cyfrin/2024-09-stakelink/blob/f5824f9ad67058b24a2c08494e51ddd7efdbb90b/contracts/linkStaking/base/VaultControllerStrategy.sol#L264>

This can lead to a scenario where, if all the group vaults are full, the contract will attempt to deposit into a removed vault, causing a revert in the Chainlink staking contract. This prevents the users from depositing in to staking pool.

## Impact

Deposit could fail due to removed operator vaults

## Tools Used

manual

## Recommendations

Modify the `_depositToVaults` function to include a check that ensures a vault has not been removed before attempting to deposit into it, similar to how the function checks for group vaults.

```Solidity
    while (i < numVaults) {
        IVault vault = vaults[i];
        uint256 deposits = vault.getPrincipalDeposits();
        uint256 canDeposit = _maxDeposits - deposits;
+      if (vault.isRemoved()){
+        continue;
+      }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Liquid Staking |
| Report Date | N/A |
| Finders | 8olidity, ald |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-09-stakelink
- **Contest**: https://codehawks.cyfrin.io/c/cm1el4vjp00019d2nzombxfzp

### Keywords for Search

`vulnerability`

