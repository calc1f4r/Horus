---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40503
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/2c5aba7f-d561-4b2b-bbcc-184095521c35
source_link: https://cdn.cantina.xyz/reports/cantina_competition_aave_may2024.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - 99Crits
  - StErMi
  - Chad0
  - krikolkk
  - r0bert
---

## Vulnerability Title

_pendingltv[asset] will be set to 0 if 2 consecutive calls to setreservefreeze(asset, true) are executed 

### Overview


The function setReserveFreeze() in PoolConfigurator.sol was modified in the 3.1 update. However, there is a bug where if the function is called twice in a row, it will reset the pending LTV to 0. This can happen if both the risk admin and emergency admin call the function at the same time. This can temporarily prevent users from using the affected asset as collateral for borrowing. The likelihood of this bug occurring is medium and it is recommended to update the function to fix the issue.

### Original Finding Content

## Context
**File:** PoolConfigurator.sol  
**Line:** 228  

## Description
The function `setReserveFreeze()` was modified in this 3.1 update to set LTV to 0 on freeze, or revert to the previous value in case of unfreezing:

```solidity
function setReserveFreeze(
    address asset,
    bool freeze
) external override onlyRiskOrPoolOrEmergencyAdmins {
    DataTypes.ReserveConfigurationMap memory currentConfig = _pool.getConfiguration(asset);
    currentConfig.setFrozen(freeze);
    if (freeze) {
        _pendingLtv[asset] = currentConfig.getLtv();
        _isPendingLtvSet[asset] = true;
        currentConfig.setLtv(0);
        emit PendingLtvChanged(asset, currentConfig.getLtv());
    } else if (_isPendingLtvSet[asset]) {
        uint256 ltv = _pendingLtv[asset];
        currentConfig.setLtv(ltv);
        delete _pendingLtv[asset];
        delete _isPendingLtvSet[asset];
        emit PendingLtvRemoved(asset);
    }
}
```

With the current implementation, if 2 consecutive calls to `setReserveFreeze(asset, true)` are executed, the second one will reset the `_pendingLtv[asset]` to 0. This is entirely possible as the function contains the `onlyRiskOrPoolOrEmergencyAdmins` modifier:

```solidity
function _onlyRiskOrPoolOrEmergencyAdmins() internal view {
    IACLManager aclManager = IACLManager(_addressesProvider.getACLManager());
    require(
        aclManager.isRiskAdmin(msg.sender) ||
        aclManager.isPoolAdmin(msg.sender) ||
        aclManager.isEmergencyAdmin(msg.sender),
        Errors.CALLER_NOT_RISK_OR_POOL_OR_EMERGENCY_ADMIN
    );
}
```

### Let's imagine the following scenario:
1. The USDC asset experiences significant price fluctuations.
2. The risk admin decides to freeze the asset by calling `setReserveFreeze(USDC, true)`. `_pendingLtv[USDC]` is set to 7700.
3. The emergency admin has the same thought and also calls `setReserveFreeze(USDC, true)`. `_pendingLtv[USDC]` is set to `currentConfig.getLtv()`, which, since the asset is already frozen, is 0.
4. Once USDC price fluctuations have stopped, the risk admin decides to call `setReserveFreeze(USDC, false)`. USDC LTV is set to 0 as the `_pendingLtv[USDC]` mapping was previously overwritten.

Temporarily, as the LTV of USDC is 0, the users can still deposit the asset into the Aave protocol and earn interest on it, but they cannot use it as collateral for borrowing purposes.

## Impact
**Severity:** Medium  
Due to this issue, users cannot use the unfrozen asset as collateral for borrowing purposes temporarily, until this is noticed by an admin.

## Likelihood
**Assessment:** Medium  
There are multiple risk admins, pool admins, and emergency admins that could potentially call this function.

## Recommendation
It is recommended to update the `setReserveFreeze()` function as shown below:

```solidity
function setReserveFreeze(
    address asset,
    bool freeze
) external override onlyRiskOrPoolOrEmergencyAdmins {
    DataTypes.ReserveConfigurationMap memory currentConfig = _pool.getConfiguration(asset);
    currentConfig.setFrozen(freeze);
    if (freeze && (currentConfig.getLtv() != 0)) { // <---------
        _pendingLtv[asset] = currentConfig.getLtv();
        _isPendingLtvSet[asset] = true;
        currentConfig.setLtv(0);
        emit PendingLtvChanged(asset, currentConfig.getLtv());
    } else if (_isPendingLtvSet[asset]) {
        uint256 ltv = _pendingLtv[asset];
        currentConfig.setLtv(ltv);
        delete _pendingLtv[asset];
        delete _isPendingLtvSet[asset];
        emit PendingLtvRemoved(asset);
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Cantina |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | 99Crits, StErMi, Chad0, krikolkk, r0bert, lukaprini, zigtur |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_aave_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/2c5aba7f-d561-4b2b-bbcc-184095521c35

### Keywords for Search

`vulnerability`

