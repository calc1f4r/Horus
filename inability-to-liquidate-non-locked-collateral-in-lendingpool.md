---
# Core Classification
protocol: Liquorice
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49440
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#6-inability-to-liquidate-non-locked-collateral-in-lendingpool
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
  - liquidation

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Inability to liquidate non-locked collateral in LendingPool

### Overview


The bug report describes an issue where an argument called `isLockedCollateral` was removed from a function called `LendingPool.liquidate()`, which is used for liquidating assets. This means that it is currently not possible to liquidate assets that are not locked. The report recommends restoring the argument in order to fix this issue.

### Original Finding Content

##### Description

Argument `isLockedCollateral` was removed from the function `LendingPool.liquidate()`, making it impossible to liquidate non-locked collateral:
```
function liquidate(
    address _user,
    LiquidateParams[] memory _withdrawalParams,
    LiquidateParams[] memory _repayParams,
    bytes memory _receiverData
)
```
https://github.com/Liquorice-HQ/contracts/blob/85c1eb77f404b0421bd3d1bdec548085006a3945/src/contracts/LendingPool.sol#L278-L283

##### Recommendation

We recommend restoring the argument `isLockedCollateral` in liquidation functions.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Liquorice |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#6-inability-to-liquidate-non-locked-collateral-in-lendingpool
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Liquidation`

