---
# Core Classification
protocol: Nabla
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36533
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nabla-security-review.md
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

[M-03] Inability to remove swap pools from the backstop pool

### Overview


A bug has been found in the backstop pool feature of the Pyth network. This bug can have a high impact and a low likelihood of occurring. The issue is that once a swap pool is added to the list of covered pools, it cannot be removed. This means that if the price feed for one of the covered pools is deprecated or returns bad data, it can cause problems with depositing or withdrawing funds from the backstop pool. This can result in the funds of the LPs in the covered pool being locked. To fix this issue, it is recommended to give the owner of the backstop pool the ability to remove swap pools from the list of covered pools.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

In the backstop pool, once a swap pool is added to the list of covered pools, it cannot be removed.

If the Pyth network deprecated the price feed for the asset of one of the covered pools, or it began returning bad data, the execution of `_getAllTokenPrices` would revert, making it impossible to deposit or withdraw from the backstop pool and, consequently, locking the funds of the LPs in the covered pool.

**Recommendations**

Give to the owner of the backstop pool the ability to remove swap pools from the list of covered swap pools.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nabla |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nabla-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

