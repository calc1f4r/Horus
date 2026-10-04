---
# Core Classification
protocol: YuzuUSD_2025-08-28
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62759
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/YuzuUSD-security-review_2025-08-28.md
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

[M-01] Missing slippage protection allows unexpected asset amounts

### Overview


The report states that there is a bug in the `ERC4626` interaction functions in three different contracts: `StakedYuzuUSD`, `YuzuUSD`, and `YuzuILP`. This bug does not have a high impact, but it can still cause problems for users. When users call functions like `initiateRedeem()`, they may not receive the expected amount of assets due to changes in fees or pool size. This is because there is no protection in place to account for these changes. The report recommends adding a slippage tolerance feature or a deadline parameter to prevent unexpected outcomes for users.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `ERC4626` interaction functions in `StakedYuzuUSD`, `YuzuUSD`, and `YuzuILP` lack slippage protection mechanisms. Users call functions like `initiateRedeem()` expecting to receive a specific amount of assets based on the current preview, but the actual amount received can differ due to state changes between transaction submission and execution.

- In `StakedYuzuUSD` and `YuzuUSD` contracts, users may suffer from changes in redemption fees. 

- In `YuzuILP` contract, users may suffer from both changes in fees and changes in pool size, as this pool is expected to also bear risk for `YuzuUSD`.

The lack of slippage protection means users cannot specify a minimum acceptable amount of assets they're willing to receive, potentially leading to unexpected outcomes.

## Recommendation

Allow users to specify their slippage tolerance when interacting with `StakedYuzuUSD`, `YuzuUSD`, and `YuzuILP` contracts.

An additional approach is to implement a deadline parameter that ensures transactions are only executed within a specific time window, reducing the likelihood of significant parameter changes between submission and execution.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | YuzuUSD_2025-08-28 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/YuzuUSD-security-review_2025-08-28.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

