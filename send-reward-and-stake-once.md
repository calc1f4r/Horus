---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6795
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Denis Milicevic
  - Gerard Persoon
---

## Vulnerability Title

Send Reward And Stake Once

### Overview


This bug report describes a high-risk situation in the Divider.sol file. The issue is that the reward and stake can be sent multiple times from the settleSeries() and backfillScale() functions. This could cause the reward and stake to be sent multiple times, which should only happen once. To fix this issue, a flag should be set to prevent the reward and stake from being sent a second time. This has been addressed in #155, and the reward is now set to 0 so it won't be sent twice. There may still be a risk with stakeSize, so it should be monitored.

### Original Finding Content

## High Risk Report

**Severity:** High Risk  
**Context:** `Divider.sol#L157-180`, `Divider.sol#L511-547`  

## Situation
A reward and stake can be sent from `settleSeries()` or `backfillScale()`. However, this should only be done once. Luckily, `settleSeries()` can’t be run twice as this is prevented by `_canBeSettled()`. However, `backfillScale()` might be called multiple times. This could result in the function trying to send the reward and the stake multiple times.

### Code Snippet: `settleSeries()`
```solidity
function settleSeries(address adapter, uint48 maturity) external nonReentrant whenNotPaused {
    ...
    // prevents calling this function twice
    require(_canBeSettled(adapter, maturity), Errors.OutOfWindowBoundaries);
    ...
    ERC20(target).safeTransferFrom(adapter, msg.sender, series[adapter][maturity].reward);
    ...
    ERC20(stake).safeTransferFrom(adapter, msg.sender, stakeSize);
    ...
}
```

### Code Snippet: `backfillScale()`
```solidity
function backfillScale(...) external requiresTrust {
    ...
    uint256 reward = series[adapter][maturity].reward;
    ERC20(target).safeTransferFrom(adapter, cup, reward);
    ERC20(stake).safeTransferFrom(adapter, stakeDst, stakeSize);
    ...
}
```

## Recommendation
After sending the reward and the stake, set a flag to prevent sending it a second time.

## Sense
Addressed in #155.

## Spearbit
The reward is set to 0 now so won’t be transferred twice. There may still, however, be a risk with `stakeSize`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sense |
| Report Date | N/A |
| Finders | Max Goodman, Denis Milicevic, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

