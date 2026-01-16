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
solodit_id: 768
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/132

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
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-07] Vault.balance() mixes normalized and standard amounts

### Overview


This bug report is about the `Vault.balance` function in the code. The function uses the `balanceOfThis` function which normalizes all balances to 18 decimals. However, the second term `IController(manager.controllers(address(this))).balanceOf()` is not normalized, which means that the `balance()` will be under-reported. This leads to receiving wrong shares when `deposit`ing tokens, and a wrong amount when redeeming `tokens`. The recommended mitigation steps are to normalize the second term before adding it, and to use `_vaultDetails[msg.sender].balance` which directly uses the raw token amounts which are not normalized.

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

Note that `balance()`'s second term `IController(manager.controllers(address(this))).balanceOf()` is not normalized.
The code is adding a non-normalized amount (for example 6 decimals only for USDC) to a normalized (18 decimals).

## Impact
The result is that the `balance()` will be under-reported.
This leads to receiving wrong shares when `deposit`ing tokens, and a wrong amount when redeeming `tokens`.

## Recommended Mitigation Steps
The second term `IController(manager.controllers(address(this))).balanceOf()` must also be normalized before adding it.
`IController(manager.controllers(address(this))).balanceOf()` uses `_vaultDetails[msg.sender].balance` which directly uses the raw token amounts which are not normalized.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/132
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`Wrong Math, Decimals`

