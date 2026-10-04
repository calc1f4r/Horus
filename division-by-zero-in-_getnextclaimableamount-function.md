---
# Core Classification
protocol: Narwhal Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37289
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal Finance.md
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

Division by Zero in `_getNextClaimableAmount` Function

### Overview


The VestingSchedule contract has a vulnerability that causes a division by zero error, potentially leading to a panic error and locking funds. This can happen if a group's vesting duration is not set or mistakenly set to zero, and the account tries to claim vested tokens. To fix this, input validation should be implemented to prevent setting a zero vesting duration, and a safe division should be used in the _getNextClaimableAmount function to handle the scenario of a zero vesting duration. This will prevent the contract from failing and locking funds.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**:

The `VestingSchedule` contract, particularly in its `_getNextClaimableAmount` function, is vulnerable to a division by zero error. This issue occurs when `groupVestingDuration[addressGroup[_account]]` is zero, a scenario that might not be uncommon, especially if vesting durations for certain groups are not set correctly or are inadvertently set to zero. The division by zero can lead to a panic error, causing contract execution to fail and potentially locking funds.
**Scenario:**
An account is added to the vesting schedule with a specific group.
The group's vesting duration is either not set or mistakenly set to zero.
The account tries to claim vested tokens.
The contract attempts to calculate the claimable amount using groupVestingDuration[addressGroup[_account]] which is zero, leading to a division by zero error.
This scenario can occur during regular operation, particularly in cases where new vesting groups are added without proper validation of input parameters.

**Recommendation:**

Implement the following changes to mitigate this vulnerability:
Input Validation: Ensure that groupVestingDuration is never set to zero in the addGroupCliff function. Add checks to prevent setting a zero vesting duration.
Safe Division: In _getNextClaimableAmount, before performing the division, check if groupVestingDuration[addressGroup[_account]] is zero. If it is, handle this case by either returning zero or reverting with a clear error message.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Narwhal Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

