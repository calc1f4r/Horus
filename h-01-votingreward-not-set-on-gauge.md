---
# Core Classification
protocol: KittenSwap_2025-06-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58068
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-06-12.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] `votingReward` not set on `Gauge`

### Overview


The report states that there is a bug in the `Gauge` contract, which can have a medium impact and a high likelihood of occurring. The bug is related to the `votingReward` not being set during initialization and not having a setter function. This results in the `notifyRewardAmount()` function reverting when fees are claimed from the pair. This bug will prevent the distribution of fees and may cause unfair distribution of rewards among depositors once a new version of the `Gauge` is deployed. The recommendation is to set the `votingReward` during initialization to fix this bug.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `Gauge` contract does not set the `votingReward` during its initialization and does not have a setter function for it.

As a result, when `notifyRewardAmount()` is called and fees are claimed from the pair, the transaction will revert.

```solidity
        (claimed0, claimed1) = IPair(address(lpToken)).claimFees();
        (address _token0, address _token1) = IPair(address(lpToken)).tokens();
        if (claimed0 > 0) {
            IERC20(_token0).approve(address(votingReward), claimed0);
    @>      votingReward.notifyRewardAmount(_token0, claimed0);
```

Until a new version of the `Gauge` is deployed, the fees will not be distributed and the `notifyRewardAmount()` function will always revert, potentially causing an unfair distribution of rewards once the new `Gauge` implementation is deployed, as the distribution among depositors might have changed.

## Recommendations

Set `votingReward` on `Gauge` initialization.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | KittenSwap_2025-06-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-06-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

