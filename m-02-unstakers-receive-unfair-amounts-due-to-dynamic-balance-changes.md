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
solodit_id: 55505
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

[M-02] Unstakers receive unfair amounts due to dynamic balance changes

### Overview


This bug report discusses an issue in the `Staking` contract where users may receive an unexpected amount of assets when finalizing their unstake. This is due to the dynamic changes in the contract's available balance caused by interactions with game contracts. This could also be exploited by users to reduce the amount owed to other unstakers. The recommendation is to add a `minAmountOut` parameter to the `finalizeUnstake()` function to ensure users receive an acceptable amount of assets and prevent unexpected reductions in the amount owed. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the `Staking` contract, users can finalize their unstake via the `finalizeUnstake()` function, where they will receive their `amountOwed` based on the available balance of the contract. However, the issue arises because the available balance dynamically changes when the game contracts interact with the contract to pay winners or transfer game losers' bits.
This results in an unexpected amount of assets being transferred to the user.
Additionally, this could be exploited by users who have passed their `unstakeDelay` and can frontrun the the `finalizeUnstake()` transaction to finalize their unstakes first, reducing the `amountOwed` for other unstakers.

```solidity
function finalizeUnstake(address token) external nonReentrant {
    //...
}
```

Similar issue with the `finalizeStake()` function:

```solidity
function finalizeStake(address token) external nonReentrant {
    //...
}
```

## Recommendation:

Add a `minAmountOut` parameter to the `finalizeUnstake()` function ( `minShare` for the `finalizeStake()` function) to ensure that the unstaker receives an acceptable amount of assets and avoids unexpected reductions in the amount they are owed due to the dynamic changes in the available contract's balance.

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

