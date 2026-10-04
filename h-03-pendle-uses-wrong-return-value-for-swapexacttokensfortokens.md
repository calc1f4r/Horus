---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25271
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/94

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-03] Pendle Uses Wrong Return Value For `swapExactTokensForTokens()`

### Overview


A bug has been identified in the function `swapExactTokensForTokens()` of the Pendle Protocol. This function returns an array with the 0 index being the input amount and the following indexes being the output amounts. The 0 index is incorrectly used in the `lend()` function of Pendle as the output amount. As a result, the value of `returned` will be the invalid input amount rather than the output amount. This could lead to the sender of the transaction receiving an incorrect number of PT tokens, either over or understated, depending on the exchange rate.

To resolve this issue, the amount of `principal` returned should be index 1 of the array returned by `swapExactTokensForTokens()`. The bug has been confirmed by Illuminate's Sourabhmarathe.

### Original Finding Content

_Submitted by kirk-baird, also found by 0x52, cccz, csanuragjain, kenzo, and WatchPug_

The function `swapExactTokensForTokens()` will return and array with the 0 index being the input amount follow by each output amount. The 0 index is incorrectly used in Pendle `lend()` function as the output amount. As a result the value of `returned` will be the invalid (i.e. the input rather than the output).

Since this impacts how many PTs will be minted to the `msg.sender`, the value will very likely be significantly over or under stated depending on the exchange rate. Hence the `msg.sender` will receive an invalid number of PT tokens.

### Proof of Concept

```solidity
            address[] memory path = new address[](2);
            path[0] = u;
            path[1] = principal;

            returned = IPendle(pendleAddr).swapExactTokensForTokens(a - fee, r, path, address(this), d)[0];
```

### Recommended Mitigation Steps

The amount of `principal` returned should be index 1 of the array returned by `swapExactTokensForTokens()`.

**[sourabhmarathe (Illuminate) confirmed](https://github.com/code-423n4/2022-06-illuminate-findings/issues/94)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-illuminate
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/94
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

