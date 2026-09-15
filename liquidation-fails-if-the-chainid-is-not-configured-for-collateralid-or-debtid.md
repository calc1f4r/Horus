---
# Core Classification
protocol: Cedro Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37524
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro Finance.md
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

Liquidation fails if the chainId is not configured for `collateralId` or `debtId`

### Overview


The report describes a bug in the `liquidate(...)` method in the `LiquidationManager.sol` contract. This method allows a liquidator to liquidate a borrower's default loan. However, there is a check in the method that can prevent liquidations if the `chainId` is not set for either the collateral or debt. This means that if a borrower has multiple types of collateral, the liquidator may not be able to liquidate all of them if the `chainId` is not set for each one. The recommendation is to ensure that the `chainId` is set for all collateral IDs to prevent this issue.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

In Contract `LiquidationManager.sol`, the method `liquidate(...)` allows a liquidator to liquidate a borrowers’ default loan.

This method has the following check:
```solidity
if (chainId[collateralId] == "" || chainId[debtId] == "")
           revert ChainIdNotConfigured(TAG);
```
This check can prevent liquidations if the `chainId` not set for either `collateralId` or `debtId`. 

For ex. Initially MATIC, FTM, BNB price is 1$ and MATIC’s chainID is set.
User A deposited 10 MATIC 
User A deposited 10 BNB
User B deposited 10 FTM
User A borrowed 5 FTM 

FTM price surges to 3.5$ 

Now User B can liquidate User B for a max amount of ~12$ (as per liquidation percent)
But User B can at max liquidate User A’s MATIC collateral as it’s chainID is set but BNB will be untouched until chainID is set.

**Recommendation**: 

It is to be ensured that chainID is set for borrowers with all collateral IDs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Cedro Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

