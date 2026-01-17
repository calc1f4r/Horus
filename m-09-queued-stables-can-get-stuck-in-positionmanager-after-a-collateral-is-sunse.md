---
# Core Classification
protocol: Ouroboros_2024-12-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45957
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
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

[M-09] Queued stables can get stuck in `PositionManager` after a collateral is sunset

### Overview


This bug report is about a high-impact issue that can affect users who have queued redemptions for a collateral that has been sunset. When this happens, the users' stables can get stuck in the `PositionManager` contract because there is no collateral left to redeem. To fix this, the report recommends setting the `redemptionCooldownPeriod` to 0 when the collateral is sunset, so that users can still recover their stables.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

After a collateral is sunset, all the orphaned collateral tokens can be withdrawn by the guardian. If users have queued redemptions, their queued stables will get stuck in the `PositionManager` contract, as there will not be any collateral to redeem.
One way of allowing users to redeem their stables it setting `redemptionCooldownPeriod` to 0, as this will trigger `_dequeueEscrow()` when `redeemCollateral()` is called. However, this value cannot be set on sunset collaterals.

## Recommendations

Set `redemptionCooldownPeriod` to 0 on `activeToSunset()` to allow users to recover their escrowed stables after the collateral is sunset.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ouroboros_2024-12-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

