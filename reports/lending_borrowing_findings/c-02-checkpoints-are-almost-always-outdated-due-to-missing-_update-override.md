---
# Core Classification
protocol: StakeDAO_2025-07-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63599
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
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

[C-02] Checkpoints are almost always outdated due to missing `_update` override

### Overview


The report discusses a bug in the Morpho Blue markets where the `_update` function is not properly overridden in the strategy wrapper. This results in outdated checkpoints and has several impacts, including the inability for liquidators to redeem LP tokens and the breaking of fungibility for ERC20 tokens. The report recommends overriding the `_update` function to update checkpoints and fix the bug.

### Original Finding Content


_Acknowledged_

## Severity

**Impact:** High

**Likelihood:** High

## Description

Strategy tokens are used as collateral token in Morpho Blue markets. It's crucial to update checkpoints in case of transfers because checkpoints are always handled with `msg.sender`. Currently, `_update` function is not overridden in strategy wrapper, which means checkpoints will be outdated almost always. 

There are many impacts of this situation:

1. Liquidator can't redeem LP tokens because he doesn't have any checkpoints for those tokens. It means it has no value for liquidators.

```solidity
        UserCheckpoint storage checkpoint = userCheckpoints[msg.sender];
        checkpoint.balance -= amount; // revert here due to underflow
```

2. Even if the borrower is liquidated in the market, he can claim rewards because his checkpoint still exists. Checkpoints are updated only while `deposit` and `withdraw` calls are made.

3. It breaks the fungibility feature of ERC20. It behaves like non-fungible tokens.

## Recommendations

Override `_update` function and update checkpoints in there.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StakeDAO_2025-07-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

