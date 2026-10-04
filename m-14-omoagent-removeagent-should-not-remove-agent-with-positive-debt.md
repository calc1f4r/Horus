---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53344
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-14] OmoAgent `removeAgent` should not remove agent with positive debt

### Overview


This bug report discusses a problem with the `removeAgent()` function in a contract. Currently, this function allows for the removal of an agent even if they have a positive debt. This can cause the contract to be in an inconsistent or incorrect state. The severity and likelihood of this bug are both considered medium. The recommendation is to check the agent's debt before removing them to avoid any issues.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `removeAgent()` function currently allows the removal of an agent even if the agent has a positive debt. This could lead to an inconsistent or incorrect state in contract:

```solidity
    function removeAgent(uint256 _id) external onlyManager {
        delete OmoAgentStorage.data().agents[_id];
    }
```

## Recommendations

Check `agentDebts` before removing an agent.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

