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
solodit_id: 45996
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

[M-02] Pairs cannot be deposited when the externalAssetVault has not been set

### Overview


The bug report discusses an issue with the `FraxlendPairCore._deposit()` function. This function does not have a check before making external calls to the `externalAssetVault` which can cause the deposit to always fail if the `externalAssetVault` has not been set. This means that lending pairs cannot function properly without the `externalAssetVault` being set. The report recommends adding a check in the `_deposit()` function to ensure that the `externalAssetVault` is not equal to 0 before making the external call.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `FraxlendPairCore._repayAsset()` function has this check before making external calls to the external vault:

```solidity
        if (address(externalAssetVault) != address(0)) {
```

However, this check is not included in `FraxlendPairCore._deposit()` before it makes an external call to the `externalAssetVault`.

This means that depositing will always revert when the `externalAssetVault` has not been set, so lending pairs cannot function independently of the lending asset vault.

## Recommendations

In `_deposit()`, ensure that `externalAssetVault != address(0)` before calling it.

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

