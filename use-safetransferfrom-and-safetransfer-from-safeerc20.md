---
# Core Classification
protocol: Tigris
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44963
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-19-Tigris.md
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

Use `safeTransferFrom` and `safeTransfer` from SafeERC20

### Overview


This bug report discusses a medium severity issue that has already been resolved. The issue was found in the Trading.sol contract, where the IERC20 interface was used to interact with different tokens. However, there were also instances where the function's result was not checked, specifically in the 'transfer' function on line 804. This could lead to unexpected results as some ERC20 tokens may not behave as expected. The recommendation is to use the SafeERC20 library to ensure safe token transfers, following best practices.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In contract Trading.sol, there are multiple places where the IERC20 interface is used for the interaction with several tokens. However, there are also cases where the result of functions is not checked, for example ‘transfer’ function at line 804 which can result in weird edge cases as there are a lot of ERC20 tokens who do not behaves as developers usually expect. 

**Recommendation**

Add the usage of SafeERC20 library to ensure safe token transfers, in line with best practices.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tigris |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-19-Tigris.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

