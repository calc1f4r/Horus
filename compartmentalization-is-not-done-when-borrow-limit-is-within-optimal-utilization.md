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
solodit_id: 45631
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

Compartmentalization is not done when borrow limit is within optimal utilization.

### Overview


Report Summary:

The report discusses a bug in the `compartmentalize()` function in the `VaultFacet.sol` smart contract. This function is used to manage assets by checking for imbalances and rebalancing accordingly. The bug occurs when the function calls `isBorrowLimitHit` and the condition is met, causing the compartmentalization to not take place. The recommendation is to change the condition from `<=` to `<` in order to fix the bug. 

### Original Finding Content

**Severity**: Medium	

**Status**: Invalid

**Description**

The function `compartmentalize()` within the `VaultFacet.sol` smart contract is used to compartmentalize assets based on current balances and assigned percentages by  checking for imbalance in the system and rebalancing assets accordingly. This function internally calls `isBorrowLimitHit` to check if a borrowing limit is hit after deducting a specified amount from the compartment balance. 

If `isBorrowLimitHit` returns true then the compartmentalization is not executed and `isBorrowLimitHit`returns true if the following condition is met:

`balAfterDeduct <= (_compBalance * s.optmialUtilization[_indexToken]) / BASIS_POINTS_DIVISOR`

What we can derive from the previous expression is that the compartmentalization is not going to take place even if the borrow limit is exactly in equilibrium because it returns true if `<=` instead of only if `<`.

**Recommendation**:

Change `<=` by `<` in `balAfterDeduct <= (_compBalance * s.optmialUtilization[_indexToken]) / BASIS_POINTS_DIVISOR`.

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

