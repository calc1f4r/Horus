---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 763
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/1

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
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xsanson
  - jonah1005
---

## Vulnerability Title

[H-02]  set cap breaks vault’s Balance

### Overview


This bug report is about an issue with the `setCap` function in the `Controller.sol` file. This function incorrectly handles `_vaultDetails[_vault].balance`, subtracting the remaining balance of the strategy instead of the difference of the strategies balance. This would result in `vaultDetails[_vault].balance` being far smaller than the strategy's value, causing an assertion error and locking the fund in the strategy. The bug is considered to be of high severity since the `setCap` function is a permission function that only the operator can call.

The bug can be triggered by setting the cap 1 wei smaller than the strategy's balance. The recommended mitigation steps include ensuring that `_vaultDetails[_vault].balance` is a public variable and subtracting the difference of the balance instead of the remaining balance of the strategy.

### Original Finding Content

## Handle

jonah1005


## Vulnerability details

## Impact
In controller.sol's function `setCap`, the contract wrongly handles `_vaultDetails[_vault].balance`. While the balance should be decreased by the difference of strategies balance, it subtracts the remaining balance of the strategy.
[Controller.sol#L262-L278](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/controllers/Controller.sol#L262-L278)
 `_vaultDetails[_vault].balance = _vaultDetails[_vault].balance.sub(_balance);`

This would result in `vaultDetails[_vault].balance` being far smaller than the strategy's value. A user would trigger the assertion at [Contreller.sol#475](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/controllers/Controller.sol#L475) and the fund would be locked in the strategy.

Though `setCap` is a permission function that only the operator can call, it's likely to be called and the fund would be locked in the contract. I consider this a high severity issue.

## Proof of Concept
We can trigger the issue by setting the cap 1 wei smaller than the strategy's balance.


```python
strategy_balance = strategy.functions.balanceOf().call()
controller.functions.setCap(vault.address, strategy.address, strategy_balance - 1, dai.address).transact()

## this would be reverted
vault.functions.withdrawAll(dai.address).transact()
```


[Controller.sol#L262-L278](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/controllers/Controller.sol#L262-L278)

## Tools Used
Hardhat

## Recommended Mitigation Steps

I believe the dev would spot the issue in the test if `_vaultDetails[_vault].balance` is a public variable.

One possile fix is to subtract the difference of the balance.
```solidity
uint previousBalance = IStrategy(_strategy).balanceOf();
_vaultDetails[_vault].balance.sub(previousBalance.sub(_amount));
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | 0xsanson, jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/1
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`vulnerability`

