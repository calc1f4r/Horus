---
# Core Classification
protocol: Satin.Exchange
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18952
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-02-24-Satin.Exchange.md
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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-9 Anybody can withdraw the admin fees in the 4pool for themselves

### Overview


This bug report is about the admin-only function `withdrawAdminFees()` and the public function `skim()` which both have the same purpose of collecting the 4pool admin fees. The bug is that `skim()` is public meaning anyone can withdraw the admin fees to an arbitrary address. The recommended mitigation is to restrict access to the `skim()` function only to the team and/or trusted addresses. The team response is that the issue has been fixed and a modifier `onlyOwnerOrRebaseHandler()` has been applied to both the `withdrawAdminFees()` and `skim()` functions. This modifier allows calls only from the owner and the rebase handler contract, thus solving the issue.

### Original Finding Content

**Description:**
The admin-only function `withdrawAdminFees()` is responsible for collecting the 4pool admin 
fees, the way this is done is by withdrawing the excess amount of tokens in the contract 
relative to the variables tracking the token balances. The function `skim()` does the same 
thing as `withdrawAdminFees()` but it’s a public function, meaning anybody can withdraw the 
admin fees to an arbitrary address.

**Recommended Mitigation:**
Because skim() is supposed to be called by the team and/or a trusted address to collect 
$CASH rebase restricting access to the skim() function only to the team and/or trusted 
addresses solves the issue. 
Important to note that when collecting the $CASH rebase the function withdrawAdminFees() 
should be called first, then the rebase should be distributed, and then `skim()` should be 
followed. If the order is not followed the rebase might be collected as admin fees or the 
admin fees might be collected as rebase.

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, a modifier `onlyOwnerOrRebaseHandler()` which 
allows calls only from the owner and the rebase handler contract has been applied to both 
the `withdrawAdminFees()` and `skim()` functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Satin.Exchange |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-02-24-Satin.Exchange.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

