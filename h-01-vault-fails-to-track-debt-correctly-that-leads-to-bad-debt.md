---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 922
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/72

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
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - jonah1005
---

## Vulnerability Title

[H-01] Vault fails to track debt correctly that leads to bad debt

### Overview


A bug report has been filed by jonah1005, which details a vulnerability in a contract that leads to an exploit pattern with varying severity. The issue is similar to the issue "misuse amount as increasing debt in the vault contract". When users borrow usdm from a vault, the debt increases by the amount multiplied by 1.005. However, when the contract records the total debt, it uses the original amount instead of the increased amount. This inconsistency leads to an inaccuracy in the accounting of the debt, which could lead to serious issues.

A proof of concept has been provided in the form of a web3.py script, which demonstrates how a liquidation could fail. No tools are used in this report.

The recommended mitigation steps are to check the contract to make sure the increased debt amount is used consistently.

### Original Finding Content

_Submitted by jonah1005, also found by WatchPug_

#### Impact
It's similar to the issue "misuse amount as increasing debt in the vault contract".
Similar issue in a different place that leads to different exploit patterns and severity.

When users borrow usdm from a vault, the debt increases by the amount \* 1.005.

```solidity
    uint256 increasingDebt = (_amount * 1005) / 1000;
```

However, when the contract records the total debt it uses `_amount` instead of `increasingDebt`.

```solidity
details[_id].debtIndex =
    (details[_id].debtIndex * (totalDebt)) /
    (details[_id].debt + _amount);
details[_id].debt = totalDebt;
details[_id].status = Status.Active;
debts += _amount;
```

[MochiVault.sol L242-L249](https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/vault/MochiVault.sol#L242-L249)

The contract's debt is inconsistent with the total sum of all users' debt. The bias increases overtime and would break the vault at the end.

For simplicity, we assume there's only one user in the vault.
Example:

1.  User deposits 1.2 M worth of BTC and borrows 1M USDM.
2.  The user's debt (`details[_id].debt`) would be 1.005 M as there's a .5 percent fee.
3.  The contract's debt is 1M.
4.  BTC price decrease by 20 percent
5.  The liquidator tries to liquidate the position.
6.  The liquidator repays 1.005 M and the contract tries to sub the debt by 1.005 M
7.  The transaction is reverted as `details[_id].debt -= _usdm;` would raise exception.

inaccurate accounting would lead to serious issues. I consider this a high-risk issue.

#### Proof of Concept
This is a web3.py script that a liquidation may fail.

```python
deposit_amount = 10**18
big_deposit = deposit_amount * 100000
minter.functions.mint(user, big_deposit).transact()

dai.functions.approve(vault.address, big_deposit + deposit_amount).transact()



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | WatchPug, jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/72
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`vulnerability`

