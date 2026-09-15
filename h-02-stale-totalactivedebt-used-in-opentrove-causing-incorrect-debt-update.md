---
# Core Classification
protocol: Roots_2025-02-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55112
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] Stale `totalActiveDebt` used in `openTrove` causing incorrect debt update

### Overview


This bug report discusses a medium severity issue in the `TroveManager::openTrove` function. The function caches the `totalActiveDebt` value before calling the `_accrueActiveInterests` function, which updates the `totalActiveDebt` to reflect accrued interest. However, the function then uses the cached value instead of the updated value, leading to an underestimation of the actual debt in the system. To fix this, the `totalActiveDebt` should be updated with the most recent value after the interest accrual. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

In the `TroveManager::openTrove` function, the `totalActiveDebt` is cached into a local variable `supply` before the `_accrueActiveInterests` function is called. The `_accrueActiveInterests` function itself updates the `totalActiveDebt` to reflect accrued interest. However, the `openTrove` function subsequently updates `totalActiveDebt` using the cached `supply` value instead of the potentially updated `totalActiveDebt`.

Specifically, the code caches `totalActiveDebt` in line 754:

```solidity
File: TroveManager.sol
754:    uint256 supply = totalActiveDebt;
```

Then, interest is accrued, potentially updating `totalActiveDebt` in line 761 by calling `_accrueActiveInterests()`:

```solidity
File: TroveManager.sol
761:    uint256 currentInterestIndex = _accrueActiveInterests();
```

Inside `_accrueActiveInterests`, `totalActiveDebt` is updated:

```solidity
File: TroveManager.sol
1183:           totalActiveDebt = currentDebt + activeInterests;
```

Finally, in line 776, `totalActiveDebt` is updated using the _cached_ `supply` value:

```solidity
File: TroveManager.sol
774:@>       uint256 _newTotalDebt = supply + _compositeDebt;
775:         require(_newTotalDebt + defaultedDebt <= maxSystemDebt, "Collateral debt limit reached");
776:@>       totalActiveDebt = _newTotalDebt;
```

Because `supply` is the value of `totalActiveDebt` before interest accrual in `_accrueActiveInterests`, the update in line 776 does not incorporate the interest accrued within the same `openTrove` transaction. This means the `totalActiveDebt` may be incorrectly updated, potentially underestimating the actual debt in the system.

Consider the next scenario:

1.  Initial state:

    - `totalActiveDebt = 1000`
    - Interest rate is such that `_accrueActiveInterests()` will increase `totalActiveDebt` by 100.

2.  `openTrove` call:

    - User calls `openTrove` with `_compositeDebt = 500`.
    - Line 754: `supply = totalActiveDebt;` => `supply = 1000` (cached value).
    - Line 761: `_accrueActiveInterests()` is called. Inside `_accrueActiveInterests()` (line 1183): `totalActiveDebt` is updated to `1000 + 100 = 1100`.
    - Line 776: `totalActiveDebt = _newTotalDebt;` where `_newTotalDebt = supply + _compositeDebt = 1000 + 500 = 1500`.
    - `totalActiveDebt` is set to `1500`.

3.  Expected vs. actual `totalActiveDebt`:
    - Expected `totalActiveDebt`: Initial debt (1000) + accrued interest (100) + new debt (500) = `1600`.
    - Actual `totalActiveDebt` after `openTrove`: `1500`.

The `totalActiveDebt` is underestimated by `100` (the accrued interest within the same transaction).

## Recommendations

To correct this issue, ensure that the `totalActiveDebt` is updated with the most recent value _after_ the interest accrual. Instead of caching `totalActiveDebt` at the beginning of the function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Roots_2025-02-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

