---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45635
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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
  - Zokyo
---

## Vulnerability Title

`collateralizationRatio` can be set higher than 100% which would result in no positions getting liquidated.

### Overview


This bug report describes a medium severity issue that has been resolved. The problem was found in the `updateCollateralizationRatio()` function in the `VaultFacet.sol` file. The issue allowed the contract owner to set the collateralization ratio higher than 100%, which could lead to no positions being liquidated. This means that users could maintain positions without enough collateral, giving them an unfair advantage over others and potentially causing financial damage to the protocol. The recommendation is to implement a minimum allowable collateralization ratio and add a validation check to prevent the owner from setting it to zero or a value higher than 100%.

### Original Finding Content

**Severity**: Medium	

**Status**: Resolved

**Description**

The `updateCollateralizationRatio()` within the `VaultFacet.sol` function is used by the owner to change the collateralizationRatio of an asset. It is possible to set the value higher than 100% by error because there are no restrictions. 

The `CollateralizationRatio` value is used for checking if a position is in a liquidable state or not. As a result of setting its value higher than 100% would result in no positions getting liquidated:
```solidity
if (currentCollateral <= (s.CollateralizationRatio[_indexToken] * position.collateral) / BASIS_POINTS_DIVISOR) {
           return (true, currentCollateral);
       }
```

**Scenario**

The contract owner sets the collateralization ratio for a particular token to zero using the updateCollateralizationRatio function.
A user with an under-collateralized position in that token will not be liquidated, as the validateLiquidation function checks if the current collateral is less than or equal to zero, which is always false.
This allows users to maintain positions without sufficient collateral, leading to potential insolvency and an unfair advantage over other users.
In a worst-case scenario, this could result in a complete collapse of the collateralization mechanism, causing substantial financial damage to the protocol and its users.

**Recommendation**:

Implement a minimum allowable collateralization ratio to prevent the owner from setting it to zero.
Add a validation check within the updateCollateralizationRatio function to ensure the new value is greater than zero and within an acceptable range (e.g., less than or equal to 100%).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

