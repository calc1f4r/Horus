---
# Core Classification
protocol: Tradable onchain v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37964
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tradable-Spearbit-Security-Review-July2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tradable-Spearbit-Security-Review-July2024.pdf
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
finders_count: 4
finders:
  - Cergyk 
  - Christoph Michel 
  - 0xIcingdeath 
  - Akshay Srivastav 
---

## Vulnerability Title

payoutPeriodStartTime skips 1 second for payouts

### Overview


This bug report discusses a medium risk bug in the PayoutManager contract, specifically in the function that distributes yield to investors. The bug occurs when a new investor joins the deal and is minted deal tokens, entitling them to yield for a specific period. However, due to a flaw in the code, this period is not calculated accurately, leading to unfair distributions and potential loss of yield for investors. The bug has been fixed in the latest update.

### Original Finding Content

## Medium Risk Issue in PayoutManager.sol

## Severity: Medium Risk

### Context
`PayoutManager.sol#L120`

### Description
When yield is being distributed via `PayoutManager._initiateInterestPayout`, the deal admin specifies a period end time. The period start time is taken as the last end time + 1 in `payoutPeriodStartTime`.

```solidity
function payoutPeriodStartTime() public view returns (uint48) {
    PMStorage storage $ = _pmStorage();
    // If there are no interest payouts yet, return the yield generation start.
    if ($.latestInterestPeriodEnd > 0) {
        return $.latestInterestPeriodEnd + 1;
    }
    // ...
}
```

The idea is that the timeline is perfectly subdivided into consecutive periods so no period can be missed. However, the new periods start at `latestInterestPeriodEnd + 1`, skipping the 1-second period from `[latestInterestPeriodEnd, latestInterestPeriodEnd + 1]` each time when a yield distribution is made. This leads to unfair distributions and in the worst case, a yield recipient may not receive their yield.

### Example 1
Assume holders are entitled to yield from time `t + 0` to `t + 200` which hasn't been distributed yet. At `t + 101`, a new investor joins the deal and is minted deal tokens, entitling them to yield for the period `[t + 101, t + 200]`.

- First, yield is distributed up to `t + 100`.
- Afterwards, yield is distributed up to `t + 200`, note that this period is starting at `payoutPeriodStartTime = t + 101` instead of `t + 100`.
- The new investor will receive the same yield for the second distribution for the `[t + 100, t + 200]` period as an existing investor with the same balance. The existing investor should have received more yield for the second distribution as they held their deal token balance for 1 second longer (the period of `[t + 100, t + 101]`).

### Example 2
The contracts are intended to be deployed on zkSync. The block time on zkSync is 1 second: an L2 block is generated every 1 second, encompassing all transactions received within that timeframe. 

An investor joins the deal and is minted deal tokens at time `t + 0`. They exit the deal one second later at time `t + 1` (force transfer, principal payout, etc.). If the previous yield distribution ended at `t + 0`, they won't receive any yield.

### Recommendation
Consider changing the `payoutPeriodStartTime` to start exactly when the old period ended.

```solidity
function payoutPeriodStartTime() public view returns (uint48) {
    PMStorage storage $ = _pmStorage();
    // If there are no interest payouts yet, return the yield generation start.
    if ($.latestInterestPeriodEnd > 0) {
        - return $.latestInterestPeriodEnd + 1;
        + return $.latestInterestPeriodEnd;
    }
    return deal().yieldGenerationStart();
}
```

### Tradable
Fixed in PR 19.

### Spearbit
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Tradable onchain v2 |
| Report Date | N/A |
| Finders | Cergyk , Christoph Michel , 0xIcingdeath , Akshay Srivastav  |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tradable-Spearbit-Security-Review-July2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tradable-Spearbit-Security-Review-July2024.pdf

### Keywords for Search

`vulnerability`

