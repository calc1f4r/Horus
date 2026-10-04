---
# Core Classification
protocol: Roots_2025-02-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55119
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
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

[M-03] Users can prevent absorbing bad debt by sandwiching liquidations

### Overview


The report discusses a problem where a trove's bad debt is redistributed among other troves when a liquidation occurs and the stability pool does not have enough funds. This allows trove owners to withdraw their collateral just before the liquidation and open it again after, avoiding the redistribution of bad debt and increasing the debt of other troves. The report recommends implementing a two-step mechanism for closing troves to prevent this issue. This would involve separating the request and execution of closing a trove by a time delay.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

When a liquidation occurs and the stability pool does not have enough funds to absorb the bad debt, this debt is distributed among all active troves.

Before a big liquidation that will cause a redistribution of bad debt, trove owners can withdraw their collateral just before the liquidation happens and open the trove again just after the liquidation, thus avoiding the redistribution of bad debt and increasing the bad debt of other troves.

## Recommendations

Implement a two-step mechanism for closing troves such that the request and the execution of the closing are separated by a time delay.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Roots_2025-02-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

