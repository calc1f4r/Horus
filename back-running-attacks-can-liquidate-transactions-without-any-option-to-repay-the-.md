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
solodit_id: 45628
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

Back-running attacks can liquidate transactions without any option to repay the debt after changing the collateralization ratio.

### Overview


The bug report is about a vulnerability in a smart contract that could potentially allow an attacker to liquidate a user's position without giving them enough time to pay off their debt. This is caused by a key factor, called `s.CollateralizationRatio[_indexToken]`, being able to be changed without any warning or grace period by the contract owner. This means that an attacker could manipulate this factor and quickly liquidate a user's position, leaving them unable to pay off their debt. The recommendation is to add a mechanism, such as a grace period or a two-step process, to prevent sudden changes to this factor and give users time to adjust their positions. 

### Original Finding Content

**Severity**: Medium	

**Status**: Resolved

**Description**

For a position to become liquidable the following conditions must be met:

`currentCollateral <= (s.CollateralizationRatio[_indexToken] * position.collateral) / BASIS_POINTS_DIVISOR`.

This is validated by the `_validateliquidation()` function within the `TradeFacet.sol` smart contract.

Regarding the above mentioned condition, it can be observed that `s.CollateralizationRatio[_indexToken]` is a key factor for determining if the position is liquidable or not. This factor can be changed without any grace period by calling `updateCollateralizationRatio()` by a new value by the owner. If an attacker executes a back-running attack for liquidating the position just after it became liquidable the user will not be able to pay the debt to avoid the liquidation.

Consider the following scenario:
Position is healthy.
Collateralization ratio is changed.
Position suddenly becomes unhealthy
Protocol liquidator calls `transferPosition` in order to get liquidated in the Escrow.sol contract.
Attacker executes a back-running attack placing a transaction calling `liquidatePosition.sol` just after the position has been transferred to the Escrow.sol contract.
User’s position gets liquidated without the possibility of paying the debt as a result of the collateralization ratio change.


**Recommendation**:

Add a mechanism to not change the collateralization ratio without a previous warning or grace period.
For example, use a 2 step mechanism:
Set the new value for collateralization ratio but it is not applied after X time.
After X time call to the second function to apply the change.

An alternative solution: Add a grace period for existing positions, give users some time to get their positions back to health and new positions created after the change are subject to the new ratio

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

