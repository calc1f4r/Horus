---
# Core Classification
protocol: Isle Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45742
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
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

maxWithdraw() of ERC4626 Vaults must not revert

### Overview


This bug report is about a function called maxWithdraw() in a contract called Pool. The function is supposed to follow a standard called EIP-4626, which states that it should not "revert" when called. However, the function is currently causing the contract to revert when called. This goes against the EIP standard, which says that if withdrawals are disabled, the function should return 0 instead of reverting. The recommendation is to fix the function so that it returns 0 instead of reverting, in order to comply with the EIP standard. The bug has been resolved and is considered to be of low severity.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**: 

According to EIP-4626, maxWithdraw() must not revert. But the function maxWithdraw()  reverts when called in the Pool contract which uses the ERC-4626 standard.
According to the EIP, if withdrawals are entirely disabled (even temporarily) it MUST return 0.

**Recommendation**: 

It is advised to NOT revert the maxwithdraw() function but to instead return 0 in order to comply with the original EIP-4626 standard.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Isle Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

