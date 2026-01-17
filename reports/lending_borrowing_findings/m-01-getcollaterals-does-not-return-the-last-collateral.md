---
# Core Classification
protocol: GainsNetwork-February
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37798
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
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

[M-01] `getCollaterals()` does not return the last collateral

### Overview


This bug report is about a function called `getCollaterals()` which is used to retrieve all the existing collaterals in a protocol. The severity of this bug is low, but the likelihood of it happening is high. The problem is that the function is not retrieving the collaterals correctly. Instead of starting from the first collateral, it starts from the second one and also fails to retrieve the last collateral. The report includes a code snippet that shows where the issue is and a recommendation on how to fix it. The recommendation suggests changing one line of code to make the function work properly. 

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

The `getCollaterals()` function is used to retrieve all the existing collaterals in the protocol. And as evident in `addCollateral()`, the `collateralIndex` for existing collateral starts from 1, while 0 is not used for any collateral.

However, `getCollateral()` accesses the `Collateral[]` incorrectly and retrieves the collaterals from index 0. This will cause it to return the empty collateral at index 0 and also fail to return the last collateral.

```Solidity
    function getCollaterals() internal view returns (ITradingStorage.Collateral[] memory) {
        ITradingStorage.TradingStorage storage s = _getStorage();

        ITradingStorage.Collateral[] memory collaterals = new ITradingStorage.Collateral[](s.lastCollateralIndex);


         //@audit it should be  for (uint8 i = 1; i < s.lastCollateralIndex +1; ++i) { instead
        for (uint8 i; i < s.lastCollateralIndex; ++i) {
            collaterals[i] = s.collaterals[i];
        }

        return collaterals;
    }
```

## Recommendations

Change from

```Solidity
for (uint8 i; i < s.lastCollateralIndex; ++i) {
```

to

```Solidity
for (uint8 i = 1; i < s.lastCollateralIndex + 1; ++i) {
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GainsNetwork-February |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

