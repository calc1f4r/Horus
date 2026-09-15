---
# Core Classification
protocol: YieldBasis_2025-03-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61979
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/YieldBasis-security-review_2025-03-26.md
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

[M-03] Token rebase miscalculation during position losses

### Overview


This bug report discusses an issue where the token reduction is not correctly calculated when the position is at a loss. This can result in an unfair distribution of value between staked and unstaked liquidity providers. The report suggests setting the token reduction to 0 when this occurs.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Low

**Likelihood:** High

## Description

When the position is at a loss (dv_use < 0), the token reduction should theoretically be zero:

```python
@internal
@view
def _calculate_values(p_o: uint256) -> LiquidityValuesOut:
    ...
    token_reduction: int256 = unsafe_div(staked * new_total_value - new_staked_value * supply, new_total_value - new_staked_value)
    ...
```
We have the numerator of the calculation should evaluate to zero:

```
  staked * new_total_value - new_staked_value * supply 
= staked * (prev_value + dv_use) - (v_st + dv_s) * supply
= staked * (prev_value + dv_use) - (v_st + dv_use * staked / supply) * supply
= staked * prev_value - v_st * supply
= staked * prev_value - (staked * prev_value / supply) * supply 
(because v_st / staked == prev_value / supply => v_st = staked *  prev_value / supply)
= 0
```

However, due to integer division rounding, the calculation may result in a non-zero value, causing an incorrect token reduction. It can lead to unfair distribution of value between staked and unstaked liquidity providers.

## Recommendations

When the position losses, set `token_reduction` = 0.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | YieldBasis_2025-03-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/YieldBasis-security-review_2025-03-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

