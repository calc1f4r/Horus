---
# Core Classification
protocol: GainsNetwork-February
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37795
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-06] Wrong validation in `toggleCollateralActiveState()`

### Overview


The report discusses a bug in the code that allows governance to disable specific types of collateral in an emergency situation. The bug occurs in a function called `toggleCollateralActiveState()` which is used to set the active state of a collateral. The bug prevents the governance from disabling certain types of collateral because of an error in the validation check. This could be a problem in emergency situations where the stablecoin collateral needs to be depegged. The report recommends changing the check to `collateral.precision == 0` to fix the bug.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The active state of the collateral can be toggled using `toggleCollateralActiveState()`, which will set `isActive` for the specified collateral index. This allows the governance to disable specified collateral when required and prevent opening of new trades using that collateral.

However, `toggleCollateralActiveState()` has an error in the validation check. It reverts when `collateral.precision > 0`, which would occur for all existing collateral as precision is set upon added.

This will prevent governance from disabling the collateral for trading when required in an emergency situation such as depegging of the stablecoin collateral.

```Solidity
    function toggleCollateralActiveState(uint8 _collateralIndex) internal {
        ITradingStorage.TradingStorage storage s = _getStorage();
        ITradingStorage.Collateral storage collateral = s.collaterals[_collateralIndex];

        //@audit this will revert as precision is > 0 for existing collaterals
        if (collateral.precision > 0) {
            revert IGeneralErrors.DoesntExist();
        }

        bool toggled = !collateral.isActive;
        collateral.isActive = toggled;

        emit ITradingStorageUtils.CollateralUpdated(_collateralIndex, toggled);
    }
```

## Recommendations

Change the check to `collateral.precision == 0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GainsNetwork-February |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

