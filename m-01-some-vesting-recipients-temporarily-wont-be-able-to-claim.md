---
# Core Classification
protocol: Protectorate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20629
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-Protectorate.md
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
  - Pashov
---

## Vulnerability Title

[M-01] Some vesting recipients temporarily won't be able to claim

### Overview


This bug report is about the `SLICE_PERIOD` constant in the `Vesting` code. This constant is set to 30 days and if the `timeFromStart` is less than 30 days it will round down to zero. This means the amount to claim until 30 days have passed will always be zero, which is especially true for vesting schedules with no `cliff` (it is 0). This bug has a medium impact as funds will be locked for 30 days and a medium likelihood as it will only happen when the cliff is < 30 days. 

To fix this issue, it is recommended to either make the `SLICE_PERIOD` smaller or implement another design for handling no cliff vesting schedules that won't be using this calculation. This will help ensure funds are not locked for 30 days.

### Original Finding Content

**Impact:**
Medium, as funds will be locked for 30 days

**Likelihood:**
Medium, because it will only happen when the cliff is < 30 day

**Description**

The `SLICE_PERIOD` constant in `Vesting` is set to 30 days. Due to the following math in `_computeReleasableAmount`

```solidity
uint256 vestedSeconds = (timeFromStart / SLICE_PERIOD) * SLICE_PERIOD;
```

If `timeFromStart` is less than 30 days this will round down to zero, which means the amount to claim until 30 days have passed will always be zero. This applies especially for vesting schedules that have no `cliff` (it is 0), which is expected for `Investors` and `Treasury`.

**Recommendations**

Make the `SLICE_PERIOD` smaller, or implement another design for handling no cliff vesting schedules that won't be using this calculation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Protectorate |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-Protectorate.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

