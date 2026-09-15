---
# Core Classification
protocol: Peapods_2024-11-16
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45997
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
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

[M-03] `addInterest()` does not obtain the `currentRateInfo` from storage

### Overview


This bug report is about a low severity issue in the `FraxlendPairCore.addInterest()` function. The function is supposed to calculate the current utilization rate, but it is not working correctly. This is because the function is using a newly initialized struct instead of the stored utilization rate, which is causing problems with the interest rates and increasing gas costs. The recommendation is to obtain the current rate info from storage before using it.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

In `FraxlendPairCore.addInterest()`, it obtains the current utilization rate:

```solidity
function addInterest(bool _returnAccounting)
        external
        nonReentrant
        returns (
            uint256 _interestEarned,
            uint256 _feesAmount,
            uint256 _feesShare,
            CurrentRateInfo memory _currentRateInfo,
            VaultAccount memory _totalAsset,
            VaultAccount memory _totalBorrow
        )
    {
        uint256 _currentUtilizationRate = _currentRateInfo.fullUtilizationRate;
```

The issue is that the `_currentRateInfo` struct has just been initialized and does not contain the stored utilization rate, which is stored in the `currentRateInfo` storage variable.

This causes the `_rateChange` to always be high enough to warrant an update to the interest rates, contrary to the protocol intention. This limits the arbitrage opportunities available and increases the gas costs.

## Recommendations

Obtain the current rate info from storage before using it:

```solidity
_currentRateInfo = currentRateInfo;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Peapods_2024-11-16 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

