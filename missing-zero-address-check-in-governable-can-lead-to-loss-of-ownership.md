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
solodit_id: 45743
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

Missing zero address check in Governable can lead to loss of Ownership

### Overview


This bug report discusses a problem with the transferGovernor() function in the Governable.sol file. The issue is that there is no check for a zero address, which can result in the admin losing ownership and access to important functions. The report recommends adding a zero address check for both the transferGovernor() function and the initialize() function in Receivable.sol. This bug has been marked as resolved.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**: 

In Governable.sol’s transferGovernor() function, there is missing zero address check. This can lead to accidentally losing ownership if a zero address is passed as a parameter to this function. This will lead to the admin losing access to the onlyGovernor() functions forever and make it unusable.

```solidity
   function transferGovernor(address newGovernor) external virtual override onlyGovernor {
       // Effects: update the governor.
       governor = newGovernor;


       // Log the transfer of the governor.
       emit IGovernable.TransferGovernor({ oldGovernor: msg.sender, newGovernor: newGovernor });
   }
```
In addition to this, the Receivable.sol’s initialize() function is missing zero address check for initialGovernor_ parameter, which can also make onlyGovernor functions uncallable and make transferGovernor unusable too.


**Recommendation**: 

It is advised to do the following changes:

Introduce a zero address check in the Governable.sol’s transferGovernor() function for the newGovernor parameter
Introduce a zero address check for Receivable.sol’s initialize() function for the initialGovernor_ parameter

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

