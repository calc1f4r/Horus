---
# Core Classification
protocol: Parcel Payroll
chain: everychain
category: uncategorized
vulnerability_type: pause

# Attack Vector Details
attack_type: pause
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20513
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-Parcel Payroll.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 1

# Context Tags
tags:
  - pause
  - missing_check

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[M-03] Contract inherits from `Pausable` but does not expose pausing/unpausing functionality

### Overview


This bug report is about the `Organizer` smart contract, which inherits from the OpenZeppelin `Pausable` contract. However, the `_pause` and `_unpause` methods are not exposed externally and no methods use the `whenNotPaused` modifier. This creates a false sense of security, as the contract is not actually pausable.

To fix this issue, the developers have two options. They can either remove the `Pausable` contract from the code or add the `whenNotPaused` modifier to the methods that they want to be safer. Additionally, they should expose the `_pause` and `_unpause` methods externally with access control. 

The impact of this bug is low, as the methods do not have the `whenNotPaused` modifier. However, the likelihood of this bug is high, as it is certain that the contract cannot be paused at all.

### Original Finding Content

**Impact:**
Low, as methods do not have `whenNotPaused` modifier

**Likelihood:**
High, as it is certain that contract can't be paused at all

**Description**

The `Organizer` smart contract inherits from OpenZeppelin's `Pausable` contract, but the `_pause` and `_unpause` methods are not exposed externally to be callable and also no method actually uses the `whenNotPaused` modifier. This shows that `Pausable` was used incorrectly and is possible to give out a false sense of security when actually contract is not pausable at all.

**Recommendations**

Either remove `Pausable` from the contract or add `whenNotPaused` modifier to the methods that you want to be safer and also expose the `_pause` and `_unpause` methods externally with access control.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 1/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Parcel Payroll |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-Parcel Payroll.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Pause, Missing Check`

