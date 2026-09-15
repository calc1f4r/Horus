---
# Core Classification
protocol: Zerodex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55794
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-04-22-ZeroDex.md
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

Use safeTransfer() and safeTransferFrom().

### Overview


This bug report is about a problem with the code in a file called BaseDexManager.sol. The issue is specifically on lines 96, 150, 130, and 120 in this file, as well as line 143 in a different file called EthDexManager.sol. The recommendation to fix this problem is to use a specific function from a library called SafeERC20.

### Original Finding Content

**Description**

BaseDexManager.sol - line 96
BaseDexManager.sol - line 150
EthDexManager.sol - line 143
BaseDexManager.sol - line 130
EthDexManager.sol - line 120

**Recommendation**:

Use the safeTransfer and safeTransferFrom from SafeERC20 library.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zerodex |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-04-22-ZeroDex.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

