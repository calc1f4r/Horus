---
# Core Classification
protocol: Trzn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37232
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN Finance.md
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

Use `SafeTransfer` Instead Of Transfer

### Overview


This bug report is about a medium severity issue that has been resolved. In a specific function called swapBforA, there is a transfer of a digital token (ERC20) happening at line 90. However, the return value of this transfer is not being checked. This means that the transfer could fail without anyone knowing, and the function would continue as if it had been successful. This could result in incorrect token balances and fees being updated. To fix this, the recommendation is to either use a safer transfer method or to check the return value of the transfer. 

### Original Finding Content

**Severity** - Medium

**Status** - Resolved

**Description**

In the swapBforA function (SwapOnetoOne_V2.sol) there is a ERC20 transfer taking place at L90 . The return value of the transfer is not checked so it is possible that the transfer fails silently (returning a false ) and the rest of the function executes normally . In that case token balances and fees would be updated without any transfer taking place.

**Recommendation**:

Use safeTransfer or check the return value of the transfer

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Trzn Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

