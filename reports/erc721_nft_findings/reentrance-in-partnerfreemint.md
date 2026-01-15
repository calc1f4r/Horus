---
# Core Classification
protocol: Heurist
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37689
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-07-01-Heurist.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Reentrance in `partnerFreeMint`

### Overview


This bug report discusses a high severity issue that has been resolved. The `partnerFreeMint` function is not following the proper checks-effects-interactions pattern, which could lead to reentrancy attacks. This means that a contract could call back into the function and bypass the 24 hours limit before it is updated. The recommendation is to update the `lastMinted` mapping before calling the `_safeMint` function to prevent these attacks. The client has addressed the issue by adhering to the checks-effects-interactions pattern and has also added an extra layer of security by using the reentrancy guard modifier.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

The `partnerFreeMint` function doesn’t implement the checks-effects-interactions pattern. The `_safeMint` function call occurs before updating the `lastMinted` mapping. If the to address is a contract, it could call back into the `partnerFreeMint` function, allowing re-entrance before `lastMinted` is updated and bypassing the 24 hours limit.

**Recommendation**: 

To prevent reentrancy attacks, update the `lastMinted` mapping before calling the `_safeMint` function.

**Fix**: Client addressed the issue in commit a27af000 by adhering to the checks-effects-interactions pattern. It is recommended though to add an extra layer of security by applying the reentrancy guard modifier to the function since the code base utilizes it already in other places of the codebase. 

**Update**: The client added the reentrancy guard modifier.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Heurist |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-07-01-Heurist.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

