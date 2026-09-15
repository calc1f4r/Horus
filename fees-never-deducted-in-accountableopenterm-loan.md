---
# Core Classification
protocol: Accountable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62980
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
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

protocol_categories:
  - options_vault
  - liquidity_manager
  - insurance
  - uncollateralized_lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Immeas
  - Chinmay
  - Alexzoid
---

## Vulnerability Title

Fees never deducted in `AccountableOpenTerm` loan

### Overview


This report describes a bug in the `AccountableOpenTerm` code. The `interestData()` function returns non-zero `performanceFee` and `establishmentFee`, but these fees are never charged. As a result, fees are effectively never taken by the protocol/manager. To fix this, the fees should be charged in the `supply()` and `repay()` functions, before any other state changes. This bug has been fixed in the commits `fce6961` and `8e53eba` by the `Accountable-Protocol` team. The bug has been verified and the fees are now correctly deducted for open term loans.

### Original Finding Content

**Description:** In `AccountableOpenTerm`, `interestData()` returns non-zero `performanceFee` and `establishmentFee`, but no path ever charges these fees. `_accrueInterest()` only updates `_scaleFactor` for base interest and none of `supply` or `repay` calls `FeeManager` (unlike FixedTerm’s `collect`). As a result, fees are never charged.

**Impact:** Protocol/manager fees are effectively never taken.

**Recommended Mitigation:** Consider charge the fee in `supply()`/`repay()`, before any other state changes. Compute fees for the elapsed period and transfer to `FeeManager`, then proceed.

**Accountable:** Fixed in commits [`fce6961`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/fce6961c71269739ec35da60131eaf63e66e1726) and [`8e53eba`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/8e53eba7340f223f86c9c392f50b8b2d885fdd39)

**Cyfrin:** Verified. `performanceFee` and `establishmentFee` are now deducted for open term loans.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Accountable |
| Report Date | N/A |
| Finders | Immeas, Chinmay, Alexzoid |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

