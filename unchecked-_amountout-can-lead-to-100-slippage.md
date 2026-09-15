---
# Core Classification
protocol: Umami
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44769
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-16-Umami.md
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
  - Zokyo
---

## Vulnerability Title

Unchecked _amountOut can lead to 100% slippage

### Overview


This bug report is about a medium severity issue that has been resolved. The issue was found in a contract called AaveUtilsl, where a function called `_tokenSwapOutAmount` was returning a value of 0 when a small amount of tokens was used. This could lead to a swap with 100% slippage, making it easy for a MEV bot to exploit and make a profit. The recommendation is to add a check to prevent the output of `_tokenSwapOutAmount` and the minimum output (_minOut) from ever being 0. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In contract AaveUtilsl, function `_tokenSwapOutAmount` will return in 0 when the token amount is a small value, resulting in an swap with a _minOut of 0 which on it’s on with lead to a swap with 100% slippage which can be easily sandwich by a MEV bot for profit.

**Recommendation**: 

Add a sanity check for the to ensure the output of `_tokenSwapOutAmount` and _minOut can never be 0.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Umami |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-16-Umami.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

