---
# Core Classification
protocol: Smoothly
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26461
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-08-01-Smoothly.md
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
  - business_logic

protocol_categories:
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[C-02] Operator can still claim rewards after being removed from governance

### Overview


A bug has been identified in the `deleteOperators` method, which is used when operators must be slashed. This bug leaves the `operatorRewards` mapping untouched when an operator is removed, meaning they can still claim their accrued rewards, even if they are acting maliciously or are inactive. This has a high impact on the PoolGovernance, as rewards shouldn't be claimable for operators that were removed. The likelihood of this happening is also high, as this will occur every time the functionality is used and an operator has unclaimed rewards. To fix this, it is recommended that the operator rewards are transferred to a chosen account, such as the `SmoothlyPool`, when an operator is removed.

### Original Finding Content

**Severity**

**Impact:**
High, as rewards shouldn't be claimable for operators that were removed from governance

**Likelihood:**
High, as this will happen every time this functionality is used and an operator has unclaimed rewards

**Description**

The `deleteOperators` method removes an operator account from the `PoolGovernance` but it still leaves the `operatorRewards` mapping untouched, meaning even if an operator is acting maliciously and is removed he can still claim his accrued rewards. This shouldn't be the case, as this functionality is used when operators must be slashed. Also if an operator becomes inactive, even if he is removed, his unclaimed rewards will be stuck in the contract with the current implementation.

**Recommendations**

On operator removal transfer the operator rewards to a chosen account, for example the `SmoothlyPool`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Smoothly |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-08-01-Smoothly.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Business Logic`

