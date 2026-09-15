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
solodit_id: 762
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/128

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - wrong_math

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

[H-01] Controller.setCap sets wrong vault balance

### Overview


This bug report is about a vulnerability in the `Controller.setCap` function. This function sets a cap for a strategy and withdraws any excess amounts, but the vault balance is decreased by the entire strategy balance instead of by this excess amount. This bug can lead to users losing money as they can redeem fewer tokens than they should, and an attacker can deposit and withdraw more tokens than they should, leading to the vault losing tokens. The recommended mitigation step is to sub the `_diff` instead of the `balance`.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `Controller.setCap` function sets a cap for a strategy and withdraws any excess amounts (`_diff`).
The vault balance is decreased by the entire strategy balance instead of by this `_diff`:

```
// @audit why not sub _diff?
_vaultDetails[_vault].balance = _vaultDetails[_vault].balance.sub(_balance);
```

## Impact
The `_vaultDetails[_vault].balance` variable does not correctly track the actual vault balances anymore, it will usually **underestimate** the vault balance.
This variable is used in `Controller.balanceOf()`, which in turn is used in `Vault.balance()`, which in turn is used to determine how many shares to mint / amount to receive when redeeming shares.
If the value is less, users will lose money as they can redeem fewer tokens.
Also, an attacker can `deposit` and will receive more shares than they should receive. They can then wait until the balance is correctly updated again and withdraw their shares for a higher amount than they deposited. This leads to the vault losing tokens.

## Recommended Mitigation Steps
Sub the `_diff` instead of the `balance`: `_vaultDetails[_vault].balance = _vaultDetails[_vault].balance.sub(_diff);`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/128
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`Wrong Math`

