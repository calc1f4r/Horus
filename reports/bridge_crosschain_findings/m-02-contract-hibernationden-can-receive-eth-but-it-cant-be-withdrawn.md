---
# Core Classification
protocol: Bearcave
chain: everychain
category: uncategorized
vulnerability_type: fund_lock

# Attack Vector Details
attack_type: fund_lock
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20613
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-BearCave.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - fund_lock

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[M-02] Contract `HibernationDen` can receive ETH but it can't be withdrawn

### Overview


This bug report is about a contract called `HibernationDen` and its `receive` method. This method is mostly expected to be used for `LayerZero` refunds. The problem is that when there is a refund from a cross-chain call, the gas refunds ETH won't be withdrawable as there is no method for ETH withdraw in the contract. Additionally, anyone can mistakenly send ETH to `HibernationDen` and it will be stuck there. The impact of this bug is medium, as it will result in stuck funds, but they will just have the value of gas refunded. The likelihood of this bug is also medium.

The recommendation to fix this bug is to add a method that can withdraw ETH from the `HibernationDen` contract.

### Original Finding Content

**Impact:**
Medium, as it will result in stuck funds, but they will just have the value of gas refunded

**Likelihood:**
Medium, as it will happen when there is a refund from a cross-chain call

**Description**

The `HibernationDen` contract has a `receive` method. This is mostly expected to be used for `LayerZero` refunds as the comment above the method says. The problem is that this gas refunds ETH won't be withdrawable as there is no method for ETH withdraw in the contract. Another issue is that anyone can mistakenly send ETH to `HibernationDen` and it will be stuck there.

**Recommendations**

Add a method that can withdraw ETH from the `HibernationDen` contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bearcave |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-BearCave.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Fund Lock`

