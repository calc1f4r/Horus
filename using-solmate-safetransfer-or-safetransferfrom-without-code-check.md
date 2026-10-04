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
solodit_id: 44589
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-19-Umami.md
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

Using solmate safeTransfer OR safeTransferFrom without code check

### Overview


This bug report discusses a problem with the use of a library called solmate in contracts. The issue is that the library may not accurately track the transfer of funds, which could result in miscalculation and potential loss of funds. The report recommends using a different library or implementing a code size check to avoid this issue. It is important to note that this problem only affects tokens trading in GLP. The bug has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

All the contracts are making heavy use of solmate’s library (e.g. function transferAsset from AggregateVault contract ) the main usecase of this collection is to optimize the gas usage as much as possible, for that to be achieved there have been some compromised made by the library developers. ​​This is a known issue while using solmate's libraries. Hence this may lead to miscalculation of funds and may lead to loss of funds, because if safetransfer() and safetransferfrom() are called on a token address that doesn't have a contract in it, it will always return success, bypassing the return value check. Due to this, the protocol will think that funds have been transferred successfully, and records will be accordingly calculated, but in reality, funds were never transferred. So this will lead to miscalculation and possibly loss of funds

**Recommendation**: 

Use openzeppelin's safeERC20 or implement a code size check

**Note**: All tokens that will be transferred using solmates transfer libs will only be well-defined tokens trading in GLP.

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

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-19-Umami.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

