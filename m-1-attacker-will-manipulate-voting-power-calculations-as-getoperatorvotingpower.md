---
# Core Classification
protocol: Symbiotic Relay
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62099
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/967
source_link: none
github_link: https://github.com/sherlock-audit/2025-06-symbiotic-relay-judging/issues/196

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
finders_count: 10
finders:
  - patitonar
  - zark
  - 0xapple
  - roshark
  - katz
---

## Vulnerability Title

M-1: Attacker will manipulate voting power calculations as `getOperatorVotingPower()` and `getOperatorVotingPowerAt()` functions lack vault validation

### Overview


This bug report discusses an issue with the `VotingPowerProvider` contract that can lead to incorrect voting power calculations. The problem is caused by missing validation for the `vault` parameter, which can allow an attacker to provide an unregistered or invalid vault address and gain unauthorized voting influence. This issue has been acknowledged by the team, but will not be fixed at this time. The report suggests adding vault validation to the affected functions to prevent this vulnerability.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-06-symbiotic-relay-judging/issues/196 

This issue has been acknowledged by the team but won't be fixed at this time.

## Found by 
0xapple, 0xmaverick, Drynooo, Jeffy, PASCAL, Ziusz, katz, patitonar, roshark, zark

### Summary

The missing vault validation in `VotingPowerProvider::getOperatorVotingPower()` and `VotingPowerProvider::getOperatorVotingPowerAt()` functions that receives the `vault` external parameter will cause incorrect voting power calculations as an attacker can provide unregistered or invalid vault addresses to gain unauthorized voting influence

### Root Cause

In `VotingPowerProviderLogic::getOperatorVotingPower(address operator, address vault, bytes memory extraData)` and `VotingPowerProviderLogic::getOperatorVotingPowerAt(address operator, address vault, bytes memory extraData, uint48 timestamp, bytes memory hints)` the `vault` parameter is not validated to be a registered vault before processing voting power calculations.

https://github.com/sherlock-audit/2025-06-symbiotic-relay/blob/main/middleware-sdk/src/contracts/modules/voting-power/VotingPowerProvider.sol#L273-L295

The functions only validate that the vault's collateral token is registered via `isTokenRegistered(IVault(vault).collateral())`, but they do not verify that the vault itself is properly registered in the system.

A vault can be unregistered by:
- SharedVaults::unregisterSharedVault()
- OperatorVaults::unregisterOperatorVault()

### Internal Pre-conditions

A vault with valid collateral token exists but is not registered in the `VotingPowerProvider` contract, OR the vault was registered but unregistered later.

### External Pre-conditions

N/A

### Attack Path

1. Attacker identifies an unregistered vault that has a registered collateral token
2. Attacker calls some contract that calls `VotingPowerProvider::getOperatorVotingPower()` with the unregistered vault address
3. Function calculates voting power using the retrieved stake and returns it as valid voting power
4. Attacker uses this voting power, gaining influence they should not have

### Impact

The protocol using `VotingPowerProvider` suffers incorrect voting power calculations as attackers gain unauthorized voting influence through unregistered vaults.

### PoC

_No response_

### Mitigation

Add vault validation to both `getOperatorVotingPower()` and `getOperatorVotingPowerAt()` functions by checking if the vault is registered before processing voting power calculations:

```solidity
// Add vault validation
if (!isSharedVaultRegistered(vault) && !isOperatorVaultRegistered(vault)) {
    return 0;
}
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Symbiotic Relay |
| Report Date | N/A |
| Finders | patitonar, zark, 0xapple, roshark, katz, Drynooo, Jeffy, PASCAL, Ziusz, 0xmaverick |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-06-symbiotic-relay-judging/issues/196
- **Contest**: https://app.sherlock.xyz/audits/contests/967

### Keywords for Search

`vulnerability`

