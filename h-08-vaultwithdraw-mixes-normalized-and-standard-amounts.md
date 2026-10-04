---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 769
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/131

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
  - wrong_math
  - decimals

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - hickuphh3  jonah1005
---

## Vulnerability Title

[H-08] Vault.withdraw mixes normalized and standard amounts

### Overview


This bug report is about the `Vault.balance` function in a smart contract. This function uses the `balanceOfThis` function which normalizes all balances to 18 decimals. However, the second term `IController(manager.controllers(address(this))).balanceOf()` is not normalized, leading to issues in the contracts that use `balance` but don't treat these values as normalized values. This can lead to an attacker stealing tokens by withdrawing a tiny amount of shares and receiving an inflated amount of a token with less than 18 decimals.

The recommended mitigation steps for this issue are to make sure any derived token amount is denormalized again before using them.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `Vault.balance` function uses the `balanceOfThis` function which scales ("normalizes") all balances to 18 decimals.

```
for (uint8 i; i < _tokens.length; i++) {
    address _token = _tokens[i];
    // everything is padded to 18 decimals
    _balance = _balance.add(_normalizeDecimals(_token, IERC20(_token).balanceOf(address(this))));
}
```

Note that `balance()`'s second term `IController(manager.controllers(address(this))).balanceOf()` is not normalized, but it must be.

This leads to many issues through the contracts that use `balance` but don't treat these values as normalized values.
For example, in `Vault.withdraw`, the computed `_amount` value is normalized (in 18 decimals).
But the `uint256 _balance = IERC20(_output).balanceOf(address(this));` value is not normalized but compared to the normalized `_amount` and even subtracted:

```solidity
// @audit compares unnormalzied output to normalized output
if (_balance < _amount) {
    IController _controller = IController(manager.controllers(address(this)));
    // @audit cannot directly subtract unnormalized
    uint256 _toWithdraw = _amount.sub(_balance);
    if (_controller.strategies() > 0) {
        _controller.withdraw(_output, _toWithdraw);
    }
    uint256 _after = IERC20(_output).balanceOf(address(this));
    uint256 _diff = _after.sub(_balance);
    if (_diff < _toWithdraw) {
        _amount = _balance.add(_diff);
    }
}
```

## Impact
Imagine in `withdraw`, the `output` is USDC with 6 decimals, then the normalized `_toWithdraw` with 18 decimals (due to using `_amount`) will be a huge number and attempt to withdraw an inflated amount.
An attacker can steal tokens this way by withdrawing a tiny amount of shares and receive an inflated USDC or USDT amount (or any `_output` token with less than 18 decimals).

## Recommended Mitigation Steps
Whenever using anything involving `vault.balanceOfThis()` or `vault.balance()` one needs to be sure that any derived token amount needs to be denormalized again before using them.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | cmichel, hickuphh3  jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/131
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`Wrong Math, Decimals`

