---
# Core Classification
protocol: Bunni-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43548
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Bunni-security-review-August.md
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

[H-03] Share price increases can lead to sandwiching attacks when using only one vault

### Overview


This bug report discusses an issue with the surge fee mechanism in a project called Bunni. The surge fee is used to prevent sandwiching attacks during certain types of changes to the project. However, the `beforeSwap` function in `BunniHookLogic` does not properly check for changes in rehypothecation yields, which can lead to a sandwiching attack. The report recommends applying a check for surge from vaults even when only one of the vaults is being used and ensuring that all changes are also implemented in `BunniQuoter` for accurate quotes. This issue has a high impact and medium likelihood of occurring.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The surge fee is a mechanism to avoid sandwiching attacks during autonomous liquidity modifications, which can happen due to LDF updates, rehypothecation yields, or autonomous rebalances.

The `beforeSwap` function in `BunniHookLogic` checks for these changes in liquidity and the check for changes in rehypothecation yields is done in the `_shouldSurgeFromVaults` function. This function performs the check only when both vaults are being used, assuming that when using only one vault, the total liquidity will not change. However, in case the tokens in the pool are unbalanced and only the token with less liquidity uses a vault, an increase in the share price of its vault will increase the total liquidity, which can lead to a sandwiching attack.

## Recommendations

Apply a check for surge from vaults also when only one of the vaults is being used. All changes done in `BunniHookLogic` should also be done in `BunniQuoter` to offer accurate quotes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bunni-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Bunni-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

