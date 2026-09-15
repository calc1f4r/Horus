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
solodit_id: 6794
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

Return value missing in wrapUnderlying() WstETHAdapter

### Overview


This bug report is about an issue in three contracts: WstETHAdapter, CAdapter, and Periphery. The function wrapUnderlying() of WstETHAdapter does not return any value, while the same function in CAdapter returns the amount of tokens sent (tBal). This causes an issue in the contract Periphery, which calls wrapUnderlying() and expects a return value, and bases its following actions on this return value. The recommendation is to add the following to the end of the function wrapUnderlying() in WstETHAdapter: return wstETH, and add unit tests for WstETHAdapter to detect these types of errors. It was not fixed in the first commit, but seems to have been fixed in a different commit, though still no test coverage was added to this issue on the dev branch.

### Original Finding Content

## High Risk Severity Report

## Context
1. `WstETHAdapter.sol#L136-142`
2. `CAdapter.sol#L130-154`
3. `Periphery.sol#L253-272`

## Situation
The function `wrapUnderlying()` of `WstETHAdapter` does not return any value, which means it returns 0. On the contrary, the function `wrapUnderlying()` of `CAdapter` returns the amount of tokens sent: `tBal`. The `CAdapter` version returns the amount of tokens sent (`tBal`), while the `WstETHAdapter` returns 0.

The contract `Periphery`, which calls `wrapUnderlying()`, expects a return value. It also bases its following actions on this return value.

```solidity
contract WstETHAdapter is BaseAdapter {
    ...
    function wrapUnderlying(uint256 amount) external override returns (uint256) {
        ...
        ERC20(WSTETH).safeTransfer(msg.sender, wstETH); // transfer wstETH to msg.sender // no return value
    }
}
```

```solidity
contract CAdapter is CropAdapter {
    ...
    function wrapUnderlying(uint256 uBal) external override returns (uint256) {
        ...
        ERC20(target).safeTransfer(msg.sender, tBal);
        return tBal;
    }
}
```

```solidity
contract Periphery is Trust {
    ...
    function addLiquidityFromUnderlying(...) {
        ...
        uint256 tBal = Adapter(adapter).wrapUnderlying(uBal);
        return _addLiquidity(adapter, maturity, tBal, mode); // tBal being used here
    }
}
```

## Recommendation
In the function `wrapUnderlying()` of `WstETHAdapter()`, at the end, add the following:
```solidity
return wstETH;
```
Add unit tests for `WstETHAdapter` to detect these types of errors.

## Sense
Fixed here.

## Spearbit
It was not fixed in the above commit. There is still a stack variable declared that will shadow the return variable. This seems to have been fixed in a different commit, but still, no test coverage was added to this issue on the dev branch.

## Spearbit Acknowledgment
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

