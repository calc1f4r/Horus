---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53560
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Function Selector Based Permissions May Break During Contract Upgrades

### Overview

See description below for full details.

### Original Finding Content

## Description

`PermissionController` uses function selectors to determine if a caller has permission to execute a specific function. This functionality may not be compatible with contract upgrades, as the function selector will change when the function parameters are modified. This will cause existing permissions to break, as the stored selector in `_permissions[account].appointeePermissions[caller]` will no longer match the new function selector.

## PermissionController.sol::canCall()

```solidity
function canCall(address account, address caller, address target, bytes4 selector) external view returns (bool) {
    return isAdmin(account, caller)
        || _permissions[account].appointeePermissions[caller].contains(_encodeTargetSelector(target, selector));
}
```

## Recommendations

Instead of using function selectors, consider using the hash of just the function name for permission checks. This would make permissions resilient to parameter changes in contract upgrades.

## Resolution

The EigenLayer team has opted to not implement the fix above and instead added documentation to inform users of this issue. The relevant documentation has been added in PR #1096.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`

