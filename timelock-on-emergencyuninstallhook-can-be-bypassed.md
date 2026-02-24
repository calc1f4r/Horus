---
# Core Classification
protocol: Biconomy Nexus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43814
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 7
finders:
  - Blockdev
  - Devtooligan
  - Chinmay Farkya
  - Christoph Michel
  - Víctor Martínez
---

## Vulnerability Title

Timelock on emergencyUninstallHook() can be bypassed

### Overview


Summary:

The emergencyUninstallHook() function in Nexus.sol is meant to allow account owners to remove a hook from their account. However, it fails to check if the hook was actually installed before allowing the uninstallation. This can be exploited by calling the function before installing the hook and then immediately after, bypassing the timelock. The recommendation is to add a check for installed modules before allowing emergency uninstallation. This issue has been fixed by Biconomy and Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
(No context files were provided by the reviewer)

## Description
The `emergencyUninstallHook()` function is meant to allow the account owner to remove a hook from the account (minus the pre and post checks on the hook). It serves as an alternative to the `uninstallModule()` function, which offers hook checks on calls to uninstall any type of modules.

A timelock has been placed to only allow the account to emergency-uninstall the hook after 1 day of placing an uninstall request. However, `emergencyUninstallHook()` fails to check that the hook was actually installed.

```solidity
function emergencyUninstallHook(address hook, bytes calldata deInitData) external payable onlyEntryPoint {
    AccountStorage storage accountStorage = _getAccountStorage();
    uint256 hookTimelock = accountStorage.emergencyUninstallTimelock[hook];

    if (hookTimelock == 0) {
        // if the timelock hasn't been initiated, initiate it
        accountStorage.emergencyUninstallTimelock[hook] = block.timestamp;
        emit EmergencyHookUninstallRequest(hook, block.timestamp);
    } else if (block.timestamp >= hookTimelock + 3 * _EMERGENCY_TIMELOCK) {
        // if the timelock has been left for too long, reset it
        accountStorage.emergencyUninstallTimelock[hook] = block.timestamp;
        emit EmergencyHookUninstallRequest(hook, block.timestamp);
    } else if (block.timestamp >= hookTimelock + _EMERGENCY_TIMELOCK) {
        // if the timelock expired, clear it and uninstall the hook
        accountStorage.emergencyUninstallTimelock[hook] = 0;
        _uninstallHook(hook, deInitData);
        emit ModuleUninstalled(MODULE_TYPE_HOOK, hook);
    } else {
        // if the timelock is initiated but not expired, revert
        revert EmergencyTimeLockNotExpired();
    }
}
```

This allows the timelock to be bypassed through the following steps:
- Call `emergencyUninstallHook()` to place an uninstall request even before installing the hook; this records a timestamp corresponding to the hook address.
- After nearly a day has passed, install the hook and use it.
- Immediately call `emergencyUninstallHook()` to utilize the request that was placed before.
- As only a day has passed, the call will go through.
- The timelock has been effectively bypassed by the account.

## Recommendation
`uninstallModule()` on Nexus.sol checks that the module they are trying to uninstall through the call is actually installed. Add the same check to `emergencyUninstallHook()`.

## Biconomy
Fixed in PR 175.

## Spearbit
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Biconomy Nexus |
| Report Date | N/A |
| Finders | Blockdev, Devtooligan, Chinmay Farkya, Christoph Michel, Víctor Martínez, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

