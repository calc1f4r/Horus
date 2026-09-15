---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25473
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-pooltogether
source_link: https://code4rena.com/reports/2021-06-pooltogether
github_link: https://github.com/code-423n4/2021-06-pooltogether-findings/issues/84

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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-03] `BadgerYieldSource` `balanceOfToken` share calculation seems wrong

### Overview


A bug report has been submitted by cmichel, which is related to the `BadgerYieldSource` contract. When supplying to the `BadgerYieldSource`, some `amount` of `badger` is deposited to `badgerSett` and one receives `badgerSett` share tokens in return which are stored in the `balances` mapping of the user. The `balanceOfToken` function should then return the redeemable balance in `badger` for the user's `badgerSett` balance.

However, `badger.balanceOf(address(badgerSett))` is only a small amount of badger that is deployed in the vault ("Sett") due to most of the capital being deployed to the _strategies_. Therefore, it under-reports the actual balance. Any contract or user calling the `balanceOf` function will receive a value that is far lower than the actual balance.

It is recommended to use `badgerSett.balance()` instead of `badger.balanceOf(address(badgerSett))` to also account for "the balance in the Sett, the Controller, and the Strategy". This has been confirmed by asselstine (PoolTogether).

### Original Finding Content

_Submitted by cmichel_

When suppling to the `BadgerYieldSource`, some `amount` of `badger` is deposited to `badgerSett` and one receives `badgerSett` share tokens in return which are stored in the `balances` mapping of the user. So far this is correct.

The `balanceOfToken` function should then return the redeemable balance in `badger` for the user's `badgerSett` balance.
It computes it as the pro-rata share of the user balance (compared to the total-supply of `badgerSett`) on the `badger` in the vault:

```solidity
balances[addr].mul(
  badger.balanceOf(address(badgerSett))
).div(
  badgerSett.totalSupply()
)
```

However, `badger.balanceOf(address(badgerSett))` is only a small amount of badger that is deployed in the vault ("Sett") due to most of the capital being deployed to the _strategies_. Therefore, it under-reports the actual balance:

> Typically, a Sett will keep a small portion of deposited funds in reserve to handle small withdrawals cheaply. [Badger Docs](https://badger-finance.gitbook.io/badger-finance/technical/setts/sett-contract)

Any contract or user calling the `balanceOf` function will receive a value that is far lower than the actual balance.
Using this value as a basis for computations will lead to further errors in the integrations.

Recommend using [`badgerSett.balance()`](https://github.com/Badger-Finance/badger-system/blob/2b0ee9bd77a2cc6f875b9b984ae4dfe713bbc55c/contracts/badger-sett/Sett.sol#L126) instead of `badger.balanceOf(address(badgerSett))` to also account for "the balance in the Sett, the Controller, and the Strategy".

**[asselstine (PoolTogether) confirmed](https://github.com/code-423n4/2021-06-pooltogether-findings/issues/84)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-pooltogether
- **GitHub**: https://github.com/code-423n4/2021-06-pooltogether-findings/issues/84
- **Contest**: https://code4rena.com/reports/2021-06-pooltogether

### Keywords for Search

`vulnerability`

