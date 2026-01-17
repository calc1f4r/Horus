---
# Core Classification
protocol: Project Pi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35692
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-24-Project Pi.md
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

Incorrect Check To Verify startTime

### Overview


This bug report discusses a problem with the start time for staking in a function called `recordStakingStart()`. The issue is that the current check for the start time only verifies if it is a valid timestamp, but it does not account for the possibility that the start time could be less than the current timestamp. This could cause problems with staking if the start time is in the next block. The recommendation is to change the check to also include the condition that the start time must be greater than the current timestamp.

### Original Finding Content

**Severity** - High

**Status** - Resolved

**Description**

The start time for staking is assigned in the function `recordStakingStart()` , to verify if the `startTime` is a valid timestamp the following check is performed →
```solidity
if (startTime > block.timestamp) {
        revert("InvalidStartTime");
    }
```
But this would be incorrect in a general sense since startTime can be higher than the current timestamp but it should not be less than the current timestamp which would be problematic. If the staking begins in the next block it should be fine since the end timestamp would be calculated accordingly.

**Recommendation**

Change the check to
```solidity
if (startTime < block.timestamp) {
        revert("InvalidStartTime");
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Project Pi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-24-Project Pi.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

