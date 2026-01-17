---
# Core Classification
protocol: Peapods
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52753
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/749
source_link: none
github_link: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/41

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
finders_count: 5
finders:
  - RampageAudit
  - X77
  - Honour
  - super\_jack
  - future2\_22
---

## Vulnerability Title

M-1: MEV bots will steal from users due to an incorrectly manipulated value

### Overview


This bug report discusses an issue with MEV bots stealing from users due to a manipulated value. The root cause is a code that decreases the minimum amount of tokens a user will receive when calling `_swapV3Single()`. This can lead to users receiving less than what they originally provided. The impact of this bug is the theft of funds from innocent users. The report suggests not manipulating the value for users who provide a specific minimum amount of tokens. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/41 

## Found by 
Honour, RampageAudit, X77, future2\_22, super\_jack

### Summary

MEV bots will steal from users due to an incorrectly manipulated value

### Root Cause

Upon calling `Zapper::_zap()` to handle a transfer of a different token, we have the following code which is for a direct swap in a Uniswap V3 pool:
```solidity
else {
        _amountOut = _swapV3Single(_in, _getPoolFee(_poolInfo.pool1), _out, _amountIn, _amountOutMin);

}
```
The `_amountOutMin` is provided by the user as slippage. The issue is that upon calling `_swapV3Single()`, we have the following code:
```solidity
uint256 _finalSlip = _slippage[_v3Pool] > 0 ? _slippage[_v3Pool] : _defaultSlippage;
...
DEX_ADAPTER.swapV3Single(_in, _out, _fee, _amountIn, (_amountOutMin * (1000 - _finalSlip)) / 1000, address(this));
```
As seen, the provided minimum amount is manipulated and decreased further.

### Internal Pre-conditions

_No response_

### External Pre-conditions

_No response_

### Attack Path

1. User provides 100 tokens to swap and wants at least 90 in return
2. The 90 minimum tokens input is decreased by `_finalSlip` percentage, resulting in the user receiving less than what he provided

### Impact

Theft of funds from innocent users who have done nothing wrong

### PoC

_No response_

### Mitigation

Do not manipulate the value for users who provided a specific amount of minimum tokens to receive

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Peapods |
| Report Date | N/A |
| Finders | RampageAudit, X77, Honour, super\_jack, future2\_22 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/41
- **Contest**: https://app.sherlock.xyz/audits/contests/749

### Keywords for Search

`vulnerability`

