---
# Core Classification
protocol: Hyperstable_2025-03-19
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57823
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] Losing voting power in rewards distribution

### Overview


The report discusses a bug in two contracts called `RewardsDistributor` and `TokenRewardsDistributor`. These contracts do not properly account for perpetual locks when calculating voting power and rewards. This means that users with perpetual locks are unable to claim their rewards, despite having an active and constant lock. The recommendation is to update the implementation to handle this issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

Both `RewardsDistributor` and `TokenRewardsDistributor` contracts lack of properly account for perpetual locks in their voting power and rewards calculations. The contracts calculate voting power using the linear decay formula (`bias - slope * time`), which incorrectly handle the perpetual locks as that perpetual locks should maintain constant voting power over time.

This issue affects the following functions in both contracts:

- `ve_for_at()`
- `_checkpoint_total_supply()`
- `_claim()`
- `_claimable()`

Since perpetual locks are initialized with `bias = 0` and `slope = 0`, the current reward logic calculates `zero` voting power for them.

As a result, users with perpetual locks unable to claim their rewards, despite having an active and constant lock. The only way for such users to receive rewards is to first convert their perpetual lock into a normal lock.

## Recommendation

Update the implementation to handle the case for perpetual locks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-03-19 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

