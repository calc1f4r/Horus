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
solodit_id: 64178
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

[M-03] Missing slippage protection in sell functions

### Overview


The bug report states that there is a problem with the `sellSharesByLots` and `sellSharesByUnits` functions, which can result in users receiving less ETH than expected when selling shares. This is because the payout is calculated based on the current supply at the time of execution, and if the supply decreases before execution, the user will receive less than expected. This is a high severity issue, but the likelihood of it occurring is low. The report recommends adding a `minNetPayout` parameter to both sell functions to prevent this issue from happening. This is important because in active markets, the share supply and prices can change quickly, leaving users vulnerable to receiving less than expected. Additionally, there is currently no protection for users selling large amounts of shares, making them vulnerable to malicious actors who could perform "sandwich attacks" to extract value from them. The report suggests implementing a protection similar to the `msg.value` sending amount for buy functions to prevent this. 

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The `sellSharesByLots` and `sellSharesByUnits` functions lack slippage protection, exposing users to receiving significantly less ETH than expected when selling shares. 

When a user submits a sell transaction, the payout is calculated based on the current supply at execution time. If other transactions execute first (either from natural market activity or frontrunning), the payout can change. If the supply decreases before execution, the user receives less than expected. This is particularly problematic because:
- In active markets with frequent trading, the share supply and prices can change substantially between transaction submission and execution.
- Users selling significant positions have no way to protect against unfavorable execution prices.
- Malicious actors could perform sandwich attacks (sell first and buy back after victim) to extract value from users if the gain > sell fees.

In contrast, buy functions are protected by max input through `msg.value` sending amount. Sell functions have no equivalent protection.

## Recommendations

Add a `minNetPayout` parameter to both sell entrypoints and revert when `netPayout < minNetPayout`.





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

