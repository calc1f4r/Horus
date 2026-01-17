---
# Core Classification
protocol: Starter
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35711
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-starter.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Inadequate Input Validation in `setStakingConfig` Function

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Location**: PoolBase.sol

**Description**

The `setStakingConfig` function in the `PoolBase.sol` contract lacks proper input validation for the `_index` parameter. The `_index` parameter is used to update the values of `feeCycle` and `burnFees` arrays. Given that `feeCycle` is of length 4 and `burnFees` is of length 5, inadequate checks on the `_index` value can lead to out-of-bounds errors or unexpected behavior. This discrepancy in array lengths and the absence of checks for valid `_index` values could result in setting configurations that are not intended or are erroneous. It might as well be necessary to validate that `minStakeTime`, `_cycle` and `_fee` are within acceptable bounds.

**Recommendation**: 

Add appropriate input validation for the `_index` parameter within the `setStakingConfig` function. The validation should ensure `_index` falls within the valid range for both the `feeCycle` and `burnFees` arrays. By doing this, you ensure that `_index` is checked against the lengths of both arrays, thereby preventing potential errors and maintaining the integrity of the staking configuration process. Additionally, consider discussing with the project owners if the restriction on changing the burn fee after the last cycle is an intentional strategic decision to ensure it aligns with the project’s goals. 

**Fix** - The client made an attempt to address the issue in commit e935e74.  Mean while the issue in itself is addressed the change proposed introduced significant bugs that undermines the functionality of the codebase.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Starter |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-starter.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

