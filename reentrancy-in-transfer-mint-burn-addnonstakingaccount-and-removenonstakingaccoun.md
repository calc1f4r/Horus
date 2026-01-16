---
# Core Classification
protocol: Unity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44520
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-02-21-Unity.md
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

Reentrancy in transfer(), mint(), burn(), addNonStakingAccount() and removeNonStakingAccount functions

### Overview


This bug report describes a critical issue where certain functions in the code are vulnerable to reentrancy. This means that an external call can be made to a different part of the code, which can cause unexpected behavior and potentially lead to security risks. The recommended solution is to move the function calls that are causing the issue to the end of the functions, in order to follow a checks-effects-interaction pattern and prevent reentrancy. This will ensure that the code is more secure and less susceptible to potential attacks. 

### Original Finding Content

**Severity**: Critical

**Status**: Acknowledged

**Description**

The functions _transfer(), _mint(), _burn(), addNonStakingAccount() and removeNonStakingAccount() are susceptible to reentrancy because an external call to YieldTracker contract(out of scope of this audit) is made via the updateRewards() function. 

Although addNonStakingAccount() and removeNonStakingAccount() is an onlyAdmin function, and mint() and burn() is an onlyMinter function, it is expected that the function follows a checks-effects-interaction pattern to avoid any kind of reentrancy as a security best practice.

**Recommendation**: 

It is advised to move the _updateRewards() function call on line: 192 and 193 in _transfer to the end of the function instead. Also, it is advised to move the _updateRewards() function call on line: 157 to the end of the _mint() function instead in order to mitigate this issue. Similarly, it is advised to move the _updateRewards() function call on line: 172 to the end of the _burn() function instead, in order to mitigate this issue. The same is advised for the addNonStakingAccount() and removeNonStakingAccount() functions. This will ensure checks-effects interactions pattern to be followed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Unity |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-02-21-Unity.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

