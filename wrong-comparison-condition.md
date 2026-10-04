---
# Core Classification
protocol: Radiant Capital
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56435
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant Capital.md
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

Wrong comparison condition.

### Overview


This report is about a bug in the MultiFee Distribution.sol contract. The issue is with the "if" statement in the _withdrawExpiredLocksFor() function on line 1147. The contract compares the variable 'isRelockAction' to "false" instead of "true", which doesn't match the contract's logic. This means that when the function is called, the funds should be transferred to the user, but they are instead being restaked. This is a critical issue because users are currently unable to withdraw their expired locks. The recommendation is to either fix the comparison logic or compare 'isRelockAction' to true instead. The post-audit shows that the condition was not changed, but a new function was added to perform the withdrawal without restaking.

### Original Finding Content

**Description**

MultiFee Distribution.sol: _withdraw Expired LocksFor(), line 1147. 
The "if " statement validates that in case relock is not disabled by the user during the relock action transaction, withdrawn funds should be restaked. However, the contract compares variable 'isRelockAction' to "false" instead of "true", which doesn't correspond to the logic of the contract. For example, if_withdrawExpired LocksFor() is called within function withdrawExpiredLocks For(), it will have parameter 'isRelockAction' set to "false" which means that funds should be transferred to the user, not restaked. However, due to the wrong condition, funds will be restaked. The issue is marked as critical since it is currently impossible for users to withdraw expired locks to their balances. 

**Recommendation**: 

Verify the comparison logic OR compare 'isRelockAction' to true instead. 

**Post-audit**. 
Comparison condition wasn't changed. Thus, function withdraw ExpiredLocksFor() still performs a relock action, however another function was added to perform withdrawing without relock.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Radiant Capital |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant Capital.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

