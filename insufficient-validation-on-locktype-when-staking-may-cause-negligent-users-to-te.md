---
# Core Classification
protocol: Devve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37621
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Devve.md
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

Insufficient Validation On `lockType` When Staking May Cause Negligent Users To Temporarily Lose Their Stakes Until Admin Recovery

### Overview


This bug report discusses a problem where users are able to stake their tokens into a contract using a lock type that may not exist. This can prevent them from accessing the "unStake" function and may require admin intervention to retrieve their tokens. The severity of this issue is considered medium. The report recommends enforcing a limit on the number of time locks that can exist and checking for the existence of a lock type before allowing staking. This will prevent users from encountering this issue in the future. The bug has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

When users stake into the staking contract they are able to supply an arbitrary `lockType` which may or may not exist, users who supply a lock type which does not exist may not have access to the `unStake` function due to the check of `locktype` existence. As a result, admins may have to rescue their tokens in order for them to gain their funds back hence, the medium in severity reasoning.

**Recommendation**: 

It’s recommended that the `setTimeLocks` has it’s length enforced to ensure that only a certain amount of time locks exist. When users attempt to stake in the contract, ensure that the lock time first exists, if the lock type is non existent, revert.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Devve |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Devve.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

