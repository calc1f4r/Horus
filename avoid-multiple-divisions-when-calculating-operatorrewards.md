---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: arithmetic
vulnerability_type: rounding

# Attack Vector Details
attack_type: rounding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7020
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - rounding

protocol_categories:
  - staking_pool
  - liquid_staking
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Optimum
  - Matt Eccentricexit
  - Danyal Ellahi
  - Saw-mon and Natalie
  - Emanuele Ricci
---

## Vulnerability Title

Avoid multiple divisions when calculating operatorRewards

### Overview


This bug report is about a medium risk issue that has been identified in the River.1.sol#L277 code. The code has two divisions which can be reduced to one and delegated to the _rewardOperators function. This will help to avoid any rounding errors that may be caused by the division in the EVM. The code needs to be changed slightly to account for the two new values, numerator and denominator, which should be passed to the _rewardOperators function. This will ensure that any rounding errors are in favor of the general users/stakers and the treasury of the River protocol. It should also be noted that the whole operator rewarding system has been removed in SPEARBIT/8.

### Original Finding Content

## Severity: Medium Risk

## Context
River.1.sol#L277

## Description/Recommendation
In `_onEarnings`, we calculate the `sharesToMint` and `operatorRewards` by dividing two numbers. We can reduce the number of divisions to one and also delegate this division to `_rewardOperators`. This would further avoid the rounding errors that we get when we divide two numbers in EVM. 

Here is the original code:

```solidity
uint256 globalFee = GlobalFee.get();
uint256 numerator = _amount * currentTotalSupply * globalFee;
uint256 denominator = (_assetBalance() * BASE) - (_amount * globalFee);
uint256 sharesToMint = denominator == 0 ? 0 : (numerator / denominator);
uint256 operatorRewards = (sharesToMint * OperatorRewardsShare.get()) / BASE;
uint256 mintedRewards = _rewardOperators(operatorRewards);
```

Instead of passing `operatorRewards`, we can pass two values: one for the numerator and one for the denominator. This way, we can avoid extra rounding errors introduced in `_rewardOperators`. `_rewardOperators` also needs to be changed slightly to account for these two new values.

Here’s the updated code:

```solidity
uint256 globalFee = GlobalFee.get();
uint256 numerator = _amount * currentTotalSupply * globalFee * OperatorRewardsShare.get();
uint256 denominator = ((_assetBalance() * BASE) - (_amount * globalFee)) * BASE;
uint256 mintedRewards;

if (denominator != 0) { // note: this was added to avoid calling `_rewardOperators` if `denominator == 0`
    mintedRewards = _rewardOperators(numerator, denominator);
}
```

Without this correction, the rounding errors are in favor of the general users/stakers and the treasury of the River protocol (not the operators).

## Alluvial
The whole operator rewarding system has been removed in SPEARBIT/8.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Optimum, Matt Eccentricexit, Danyal Ellahi, Saw-mon and Natalie, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf

### Keywords for Search

`Rounding`

