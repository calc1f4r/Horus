---
# Core Classification
protocol: Klaster
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36334
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Klaster-security-review.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-08] Missing check for non-zero `msg.value`

### Overview

See description below for full details.

### Original Finding Content

The `KlasterPaymaster` contract has three functions that accept Ether: `handleOps`, `simulateHandleOp`, and `simulateValidation`. However, these functions do not check whether the received `msg.value` is greater than zero before depositing the funds to the `entryPoint` contract using `entryPoint.depositTo{value: msg.value}(address(this))`.

If the `msg.value` is zero, the deposit operation will still be executed, but it will not have any effect on the contract's balance.

To ensure that the `msg.value` is greater than zero before depositing funds, add a check at the beginning of each affected function. If the `msg.value` is zero, the function should revert with an appropriate error message.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Klaster |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Klaster-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

