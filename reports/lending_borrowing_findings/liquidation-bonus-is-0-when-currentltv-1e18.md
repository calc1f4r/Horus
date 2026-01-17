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
solodit_id: 37521
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro Finance.md
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
  - Zokyo
---

## Vulnerability Title

Liquidation bonus is 0% when `currentLTV > 1e18`

### Overview


The report discusses a bug in the Contract LiquidationManager.sol file, specifically in the `liquidate(..)` method. The bug causes the liquidation bonus to be 0 if the current loan-to-value ratio (LTV) is greater than 1e18. This means there is no incentive for liquidators to take on the risk of liquidating loans, leading to a buildup of bad debts. The recommendation is to update the logic to assign a discount amount for liquidation, providing an incentive for liquidators. The client has stated that the current logic is meant to prevent a toxic liquidation spiral, but the recommendation still stands.

### Original Finding Content

**Severity**: High

**Status**: Acknowledged

**Description**

In Contract LiquidationManager.sol, the method `liquidate(..)` has the following check:
```solidity
       uint256 discount; 
       uint256 liqPercent = 1e18;
       if (currentLTV < 1e18) {
           discount = 1e36 / currentLTV - 999000000000000000;
           console.log("discount", discount);
           if (discount > config.liqMaxDiscount) {
               discount = config.liqMaxDiscount;
           }
…}}
```
Here discount is 0 if `currentLTV` is more than 1e18. This means there is no liquidation bonus for liquidators and will lead to a pile of bad debts as there is no incentive for users to liquidate.

**Recommendation**: 

Update the liquidation logic to assign a discount amount for liquidation to provide the incentive for the same.

**Client commented**: 

We have implemented the liquidation logic in a way to mitigate the toxic liquidation spiral. So for that reason the liquidation bonus is 0% when currentLTV>1e18. Please refer to https://arxiv.org/pdf/2212.07306.pdf

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

