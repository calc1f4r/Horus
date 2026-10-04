---
# Core Classification
protocol: Coinflip_2025-02-19
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55506
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-19.md
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

[M-03] Locked tokens when token is removed during `depositDelay` period

### Overview


The report discusses a bug in the `Staking.finalizeStake()` function that allows users to complete the staking process even if the intended token is removed from the `acceptedTokens` list during the `depositDelay` period. This can result in the user's tokens being locked for at least 49 hours until they can withdraw their non-accepted tokens. Additionally, if the contract does not have enough liquidity, the user's stake could remain locked for even longer. The recommendation is to update the `finalizeStake()` function to handle this scenario and refund non-accepted tokens to the user, ensuring that they are not locked out of their tokens for an extended period.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description:

The `Staking.finalizeStake()` function allows staking to be completed even if the intended token is removed from the `acceptedTokens` list **during the `depositDelay`** (if between a `requestStake()` and `finalizeStake()` calls, the intended token is removed).
This results in locking the user's tokens for at least the duration of `depositDelay` + `unstakeDelay` (currently locking for at least a total of **49 hours**) until the user can withdraw their non-accepted tokens.
Furthermore, if the contract’s liquidity is insufficient to complete `finalizeUnstake()`, the user’s stake could remain locked for an even longer period.
This scenario is a possible due to the lack of a check on whether the token has been removed from the `acceptedTokens` when the user calls `Staking.finalizeStake()` function.

## Recommendation:

Update the `finalizeStake()` function to handle the case where the token has been removed from the `acceptedTokens` list, where the non-accepted tokens is refunded to the user , ensuring that users are not locked out of their tokens for an extended period if the token is no longer accepted.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Coinflip_2025-02-19 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-19.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

