---
# Core Classification
protocol: AdapterFinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58084
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
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

[M-01] Multiple strategies sharing the same asset

### Overview


The report discusses a bug in the AdapterVault design which assumes that each strategy has a unique asset. This can lead to overinflated values in key accounting functions. The bug occurs when two strategies share the same underlying asset, causing the same token to be counted twice and resulting in incorrect calculations. To fix this, the \_addAdapter() function should be updated to check that the asset is not already being used in current strategies.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

AdapterVault design assumes that each strategy has a unique asset (e.g. PT token). Otherwise, key accounting functions would return overinflated values.

E.g. \_totalAssetsNoCache() which goes through each strategy and calls `balanceOf()` for their related underlying and sums them up.

```python
@internal
@view
def _totalAssetsNoCache() -> uint256:
    assetqty : uint256 = ERC20(asset).balanceOf(self)
    for adapter in self.adapters:
        assetqty += IAdapter(adapter).totalAssets()

    return assetqty
```

`IAdapter(adapter).totalAssets()` checks the balance of the related underlying on `AdapterVault` and multiply by its oracle price (according to `PendleAdapter`).

But if two strategies share the same underlying, it will double count the same token twice, because `AdapterVault` cannot identify how this balance is split between two strategies.

As a result, it leads to overinflated `totalAssets()` and broken calculations between shares and assets. Transient cache values will also hold the wrong balances.

## Recommendations

\_addAdapter() should check that `adapter.asset` is not used in current strategies.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AdapterFinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

