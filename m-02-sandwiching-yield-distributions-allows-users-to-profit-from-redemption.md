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
solodit_id: 62760
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

[M-02] Sandwiching yield distributions allows users to profit from redemption

### Overview


The bug report discusses an issue with the `StakedYuzuUSD` contract that allows users to benefit from larger yields by sandwiching the reward distribution with deposit and redeem requests. This results in a net positive outcome for the users, even after accounting for redemption fees. The report recommends implementing a cooldown period between deposit and redemption requests to prevent this exploit.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `StakedYuzuUSD` allows users to deposit and initiate redeem requests immediately after the reward distribution. When rewards are distributed to the `StakedYuzuUSD` contract, the `totalAssets()` increases while `totalSupply()` remains constant, which improve the exchange rate for all shareholders. 

However, users can sandwich the reward distribution with the deposit and redeem requests to initiate redemption requests. They can then benefit from the yields that larger than the fee they pay, potentially resulting in a net positive outcome even after accounting for redemption fees.

**Proof of Concept:**: [test_fuzz_audit_sandwichYieldDistribution](https://gist.github.com/merlinboii/b125979b081266de2491e883712713fc#file-stakedyuzuusd-t-sol-L54)

## Recommendation

Implement a cooldown period between when users deposit and when users can initiate redemption requests.





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

