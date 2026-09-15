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
solodit_id: 7021
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

Shares distributed to operators suffer from rounding error

### Overview


A bug has been identified in the River.1.sol#L238 code, which is used to distribute a portion of the overall shares to operators based on the number of active and funded validators. The code calculates the number of shares distributed to a validator by dividing the reward by the total number of active validators, then multiplying it by the validator count. This calculation is subject to a rounding error, which can favor the users/depositors. 

The recommendation is to rewrite the code to reduce the rounding error, but this would add an additional DIVgas cost of 5gas per iteration. Alternatively, the whole operator rewarding system has been removed in SPEARBIT/8. This has been acknowledged.

### Original Finding Content

## Severity: Medium Risk

## Context: 
River.1.sol#L238

## Description: 
*rewardOperators* distribute a portion of the overall shares distributed to operators based on the number of active and funded validators that each operator has.

The current number of shares distributed to a validator is calculated by the following code:

```solidity
_mintRawShares(operators[idx].feeRecipient, validatorCounts[idx] * rewardsPerActiveValidator);
```

where *rewardsPerActiveValidator* is calculated as:

```solidity
uint256 rewardsPerActiveValidator = _reward / totalActiveValidators;
```

This means that in reality each operator receives:

*validatorCounts[idx] * (_reward / totalActiveValidators)* shares. Such share calculation suffers from a rounding error caused by division before multiplication.

## Recommendation: 
Consider re-writing the number of shares distributed to each operator:

```solidity
// removed --- > uint256 rewardsPerActiveValidator = _reward / totalActiveValidators;
for (uint256 idx = 0; idx < validatorCounts.length;) {
    _mintRawShares(
        operators[idx].feeRecipient,
        (validatorCounts[idx] * _reward) / totalActiveValidators
    );
    ...
}
```

Note that this will reduce the rounding error, but it adds 1 DIVgas cost (5 gas) per iteration. Also, the rounding errors favor the users/depositors.

## Alluvial: 
The whole operator rewarding system has been removed in SPEARBIT/8.

## Spearbit: 
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

