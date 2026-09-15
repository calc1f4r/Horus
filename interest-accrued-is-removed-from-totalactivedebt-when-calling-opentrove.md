---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46262
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a
source_link: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
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
finders_count: 4
finders:
  - pkqs90
  - etherSky
  - T1MOH
  - santipu
---

## Vulnerability Title

Interest Accrued is removed from totalActiveDebt when calling openTrove 

### Overview


The report describes a bug in the TroveManager smart contract where the total active debt is not being updated correctly when a new Trove is opened. This results in the interest accrued since the last update being completely removed from the total active debt calculation. This can lead to issues such as inaccurate checks for maximum system debt, excessive rewards being distributed, and Troves being unable to be closed or redeemed. The recommendation to resolve this issue is to ensure that the total active debt is correctly updated when a Trove is opened.

### Original Finding Content

## Issue Report

## Context
TroveManager.sol#L1061

## Description
The total active debt in a `TroveManager` is not correctly updated when a new Trove is opened, resulting in the complete removal of the interest accrued since the last update.

When a Trove is opened within a `TroveManager`, the total active debt is initially updated through `_accrueActiveInterests`. This function calculates and adds the accumulated interest since the last update to the total active debt. However, this update is subsequently ignored and overwritten when the total active debt is recalculated as the sum of the previous debt and the new debt from the opening Trove.

This final update to the total active debt completely overwrites the earlier interest accrual, effectively removing it from the total active debt calculation.

```solidity
function openTrove(
    address _borrower,
    uint256 _collateralAmount,
    uint256 _compositeDebt,
    uint256 NICR,
    address _upperHint,
    address _lowerHint,
    bool _isRecoveryMode
) external whenNotPaused returns (uint256 stake, uint256 arrayIndex) {
    // ...
    // cache total active debt
    uint256 totalActiveDebtPre = totalActiveDebt; // <<<
    // ...
    t.activeInterestIndex = _accrueActiveInterests(); // <<<
    // ...
    // enforce collateral debt limit
    uint256 _newTotalDebt = totalActiveDebtPre + _compositeDebt; // <<<
    require(_newTotalDebt + defaultedDebt <= maxSystemDebt, "Collateral debt limit reached");
    // update storage new total active debt
    totalActiveDebt = _newTotalDebt; // <<<
}
```

This issue causes the `totalActiveDebt` variable to become desynchronized from the actual total active debt in the `TroveManager`. While the individual Trove debt balances remain accurate (as `activeInterestIndex` remains unaffected), the sum of these balances will exceed the value of `totalActiveDebt`.

This discrepancy can lead to the following issues:
- Checks for `maxSystemDebt` will be inaccurate because they rely on the incorrect `totalActiveDebt`.
- The reward distribution system will distribute excessive rewards to users, resulting in insufficient funds for later claimants.
- The last Troves to be closed or redeemed from the `TroveManager` will fail due to an underflow in `totalActiveDebt`.

## Recommendation
To resolve this issue, ensure `totalActiveDebt` is correctly updated when a Trove is opened:
```solidity
uint256 _newTotalDebt = totalActiveDebtPre + _compositeDebt; 
+ uint256 _newTotalDebt = totalActiveDebt + _compositeDebt;
require(_newTotalDebt + defaultedDebt <= maxSystemDebt, "Collateral debt limit reached");
// update storage new total active debt
totalActiveDebt = _newTotalDebt;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bima |
| Report Date | N/A |
| Finders | pkqs90, etherSky, T1MOH, santipu |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a

### Keywords for Search

`vulnerability`

