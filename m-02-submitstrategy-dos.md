---
# Core Classification
protocol: AdapterFinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58085
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
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

[M-02] `submitStrategy()` DOS

### Overview


The function `Governance.submitStrategy()` has a bug where it only allows for one pending strategy per vault and does not accept any new strategies for voting. This function is also public, which means anyone can submit a strategy. This makes it vulnerable to spam attacks, where an attacker can continuously submit new strategies and delay the voting process. The bug can also be used to block legitimate submissions by frontrunning transactions. To fix this, it is recommended to either allow for multiple pending strategies or limit submissions to trusted addresses.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

`Governance.submitStrategy()` is strict to have only one pending strategy per vault. Moreover, no new strategy can be accepted for voting. It can only be accepted either after accepting or rejecting a pending strategy or after 6 hours after submission.

In addition, this function is public, so anyone can submit.

As a result, the simplest attack vector is spamming any new strategy as soon as submission is available. New submissions will have to wait 6 hours or governance step in. But after that the same spam attack is possible.
It can also be frontrun transactions before submissions to block them.

## Recommendations

Consider allowing multiple pending strategies so that the attacker's submissions could be just ignored.
Or allow submitting only for trusted addresses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AdapterFinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

