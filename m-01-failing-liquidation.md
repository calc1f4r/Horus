---
# Core Classification
protocol: Hyperstable_2025-03-19
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57825
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
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

[M-01] Failing liquidation

### Overview


This report highlights a bug in the `setLiquidationManager()` function of the `PositionManager` contract. When the `liquidationManager` address is changed, the new contract is not given approval on the share tokens for all registered vaults. This results in the failure of liquidation for these vaults when the `liquidationManager` tries to redeem assets to pay for the liquidator. To fix this, a mechanism should be implemented to grant the new `liquidationManager` address approval on all registered vaults shares.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the `setLiquidationManager()` function of the `PositionManager` contract, when the `liquidationManager` address is changed, the new contract is not granted approval on the share tokens for all registered vaults. This results in the **failure of liquidation for these vaults** when the `liquidationManager` attempts to redeem assets to pay for the liquidator:

```solidity
 function setLiquidationManager(address _newLiquidationManager) external onlyOwner {
        emit NewLiquidationManager(liquidationManager, _newLiquidationManager);

        liquidationManager = _newLiquidationManager;
    }
```

## Recommendations

Implement a mechanism to grant the new `liquidationManager` address approval on all registered vaults shares.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-03-19 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

