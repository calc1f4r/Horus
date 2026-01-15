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
solodit_id: 43690
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
finders_count: 1
finders:
  - KrisRenZo
---

## Vulnerability Title

Attacker Can Reset the Unbonding Period for Vaults in `globalState.curUnbondedVaultGroup`, Preventing User Withdrawals

### Overview

See description below for full details.

### Original Finding Content

## Summary

StakeLink offers an advantage over direct Chainlink staking by providing readily available tokens for withdrawals. This is achieved by keeping one of five vault groups unbonded at any time. However, a malicious user can exploit the `PriorityPool::performUpkeep` function to intentionally rebond vaults in the `globalState.curUnbondedVaultGroup`, locking tokens that are supposed to be readily available for withdrawal. This effectively prevents users from withdrawing their tokens and interrupts the protocol's operation.

 

## Vulnerability Details

In Chainlink staking, if an unbonded staker adds to their deposit, the bonding period resets, locking the tokens again. StakeLink allows any user to call `PriorityPool::performUpkeep` to process queued deposits, with the user able to specify the target vaults through the encoded `_performData`.

The vulnerability lies in the `VaultDepositController::_depositToVaults` function, which processes deposits into the vaults:

```js
    function _depositToVaults(
        uint256 _toDeposit,
        uint256 _minDeposits,
        uint256 _maxDeposits,
        uint64[] memory _vaultIds
    ) private returns (uint256) {
        uint256 toDeposit = _toDeposit;
        uint256 totalRebonded;
        GlobalVaultState memory globalState = globalVaultState;
        VaultGroup[] memory groups = vaultGroups;

        // deposits must continue with the vault they left off at during the previous call
        if (_vaultIds.length != 0 && _vaultIds[0] != globalState.groupDepositIndex)
            revert InvalidVaultIds();

        // deposit into vaults in the order specified in _vaultIds
        for (uint256 i = 0; i < _vaultIds.length; ++i) {
            uint256 vaultIndex = _vaultIds[i];
            if (vaultIndex >= globalState.depositIndex) revert InvalidVaultIds();

            // ...
        }
    }
```

The function only validates the first vault in the `_vaultIds` array, meaning a malicious user can pass an array of vaults targeting `globalState.curUnbondedVaultGroup` without triggering any errors. This allows the user to rebond vaults that should remain unbonded, reducing the protocol's ability to process withdrawals.

Additionally, if the protocol tries to withdraw tokens from a vault that isn't part of `globalState.curUnbondedVaultGroup`, the withdrawal will revert:

```js
// vault must be a member of the current unbonded group
if (vaultIds[i] % globalState.numVaultGroups != globalState.curUnbondedVaultGroup) revert InvalidVaultIds();
```

This means no tokens will be available for withdrawal, leading to frustrated users who are unable to access their funds.

 

## Impact

An attacker can effectively disrupt the protocol by preventing users from withdrawing their tokens. This attack costs the attacker nothing but time and can be executed repeatedly. It can cause severe financial and reputational damage to StakeLink, potentially driving users away from the platform and providing an unfair advantage to competitors.

 

## Tools Used

Manual

 

## Recommendations

Implement stricter validation within the `VaultDepositController::_depositToVaults` function to ensure that only valid vaults can be targeted. Additionally, limit the ability to target vaults in `globalState.curUnbondedVaultGroup` to prevent rebonding actions from locking up tokens meant to be available for withdrawal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Liquid Staking |
| Report Date | N/A |
| Finders | KrisRenZo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-09-stakelink
- **Contest**: https://codehawks.cyfrin.io/c/cm1el4vjp00019d2nzombxfzp

### Keywords for Search

`vulnerability`

