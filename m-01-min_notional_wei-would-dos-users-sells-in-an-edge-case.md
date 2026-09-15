---
# Core Classification
protocol: TopStrike_2025-12-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64176
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/TopStrike-security-review_2025-12-18.md
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

[M-01] `MIN_NOTIONAL_WEI` would DOS users sells in an edge case

### Overview


This bug report discusses an issue with `_sellSharesUnits()` function, where it overlooks a case when the `MIN_NOTIONAL_WEI` check is enabled. This can cause problems for users who have bought shares of a player at the border of the `MIN_NOTIONAL_WEI` value. If a big whale sells their shares, the share price can decrease, making it impossible for other users to sell their shares because they are now worth less than the `MIN_NOTIONAL_WEI` value. This issue also applies to the functions `transferSharesByUnits()` and `awardSharePrizeByUnits()`. The recommendation is to turn off `MIN_NOTIONAL_WEI` for sells, as implementing it for each player curve would be too complex.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In `_sellSharesUnits()`, there is a check for `MIN_NOTIONAL_WEI` if enabled, the check is made on buy and sell operations, but it overlook a case where the following can happen:
1. A big whale buy a very large amounts of `player x`, increasing its price.
2. Some users buys `player x` shares at the border of `MIN_NOTIONAL_WEI` value.
3. The big whale sells his shares making the share price go lower.
4. Other users can't sell now cause their shares are worth less than `MIN_NOTIONAL_WEI` users will have to buy more `player x` shares to then sell their initial shares.

Same scenario applied for `transferSharesByUnits()` and `awardSharePrizeByUnits()`

## Recommendations

Efficiently implementing `MIN_NOTIONAL_WEI` per every player curve will bring more complexity, so it would be better to turn off `MIN_NOTIONAL_WEI` for sells.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | TopStrike_2025-12-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/TopStrike-security-review_2025-12-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

