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
solodit_id: 6807
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
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

Do collect() First In GClaimManager

### Overview


This bug report is about the function join() of GClaimManager.sol. The function pulls target to backfill for previous collect()s, however if collect() hasn’t been called for a long time or not at all, the user might not have enough target for the backfill. The recommendation is to call Divider.collect() at the beginning of the join() function. It is noted that GClaimManager will most likely be deprecated, but this issue is included for completeness.

### Original Finding Content

## Security Analysis Report

## Severity
**Medium Risk**

## Context
`GClaimManager.sol#L36-75`

## Situation
The function `join()` of `GClaimManager.sol` pulls target to backfill for previous `collect()` calls. However, if `collect()` hasn’t been called for a long time (or not called at all), the user might not have enough target for the backfill.

### Code Snippet
```solidity
function join(address adapter, uint48 maturity, uint256 uBal) external {
    ...
    /* Pull the amount of `Target` needed to
    backfill the `excess` back to issuance,
    retrieves previously `collect()`'ed `target`
    */
    ERC20(Adapter(adapter).target()).safeTransferFrom(msg.sender, address(this), tBal);
    ...
    // Pull Collect Claims to GClaimManager.sol
    ERC20(claim).safeTransferFrom(msg.sender, address(this), uBal);
    /* This will call `Divider.collect()`
    and send target to the `msg.sender`
    */
    ...
}
```

## Recommendation
If the Sense Team agrees this is an issue, then call `Divider.collect()` at the beginning of function `join()`.

## Note
`GClaimManager` will most likely be deprecated. This issue is included for completeness.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

