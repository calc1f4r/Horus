---
# Core Classification
protocol: Resolv-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41547
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Resolv-security-review-August.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] No mechanism to exit isolation mode once entered

### Overview


This bug report discusses a problem with the `supply()` function in the `AaveV3TreasuryConnector` contract. This function is used to allow users to supply ETH or ERC20 tokens as collateral. However, there is an issue where if a user supplies an isolated asset as collateral, they are unable to enable any other assets as collateral, including other isolated assets. This is because the function attempts to enable all newly supplied assets as collateral, which is not compatible with isolation mode. To fix this, it is recommended to separate the `setUserUseReserveAsCollateral()` function from the `supply()` function. This will allow users to exit isolation mode by disabling the isolated asset as collateral.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `supply()` function in the `AaveV3TreasuryConnector` contract allows users to supply ETH or ERC20 tokens as collateral. The function checks if the asset’s usage as collateral is enabled. If not, it enables it using the following code:

```solidity
            if (!_isUsageAsCollateralEnabled(_token)) {
                aavePool.setUserUseReserveAsCollateral(_token, true);
            }
```

- The issue arises because in Aave v3, if a user supplies an isolated asset as collateral, they can only borrow assets that are permitted in isolation mode.

- Additionally, users in isolation mode cannot enable other assets, including other isolated assets, as collateral.

- As a result, if the first asset supplied is an isolated asset, no other non-isolated assets can be supplied through the `AaveV3TreasuryConnector`, because the `supply()` function will attempt to enable all newly supplied assets as collateral, which is incompatible with isolation mode.

## Recommendations

To address this issue, consider separating the `setUserUseReserveAsCollateral()` function from the `supply()` function. The only way to exit isolation mode is to disable the isolated asset as collateral, which is currently not possible with the existing implementation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Resolv-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Resolv-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

