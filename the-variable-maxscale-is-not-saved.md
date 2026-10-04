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
solodit_id: 6791
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

The Variable maxscale Is Not Saved

### Overview


This bug report is about a high-risk issue in the function _collect() of Divider.sol. In this function, the value maxscale is updated in a temporary variable, but not written back to its origin. This means the value of maxscale is not kept over time.

To address this issue, two solutions have been suggested. The first one is to replace memory with storage. This way, any access to _series will translate to sload/sstore. The second one is to add a line of code at the end of function _collect() to "save" the value of _series.maxscale. This is assuming maxscale is the only part that has to be saved.

The issue has been addressed in #163 and acknowledged by the spearbit.

### Original Finding Content

## Security Advisory

## Severity
**High Risk**

## Context
*File*: Divider.sol  
*Lines*: 334-382

## Situation
In the function `_collect()` of `Divider.sol`, the value `maxscale` is updated in a temporary variable. However, this temporary variable is not written back to its origin. This means the value of `maxscale` is not kept over time.

```solidity
function _collect(...) internal returns (uint256 collected) {
    ...
    Series memory _series = series[adapter][maturity];
    ...
    // If this is larger than the largest scale we've seen for this Series, use it!
    if (cscale > _series.maxscale) {
        // _series is a local variable
        _series.maxscale = cscale;
        lscales[adapter][maturity][usr] = cscale;
    } else {
        // If not, use the previously noted max scale value
        lscales[adapter][maturity][usr] = _series.maxscale;
    }
} // _series is not saved to series[adapter][maturity]
```

## Recommendation
Do one of the following:
- Replace memory with storage. This way, any access to `_series` translates to sload/sstore:
  ```solidity
  Series storage _series = series[adapter][maturity];
  ```
- At the end of the function `_collect()`, add the following to "save" the value of `_series.maxscale`. This is assuming `maxscale` is the only part that has to be saved:
  ```solidity
  series[adapter][maturity].maxscale = _series.maxscale;
  ```

## Sense
Addressed in #163.

## Spearbit
Acknowledged.

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

