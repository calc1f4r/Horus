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
solodit_id: 767
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/9

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
finders_count: 1
finders:
  - jonah1005
---

## Vulnerability Title

[H-06] earn results in decreasing share price

### Overview


This bug report is about a vulnerability in a dai vault that pairs with NativeStrategyCurve3Crv. Every time the `earn()` function is called, shareholders would lose money (about 2%). This is due to two issues with the Vault contract and the controller contract not properly handling the price difference between the want token and other tokens. The bug was triggered with a web3.py script and the recommended mitigation steps are to decide what the balance sheet in each contract stands for and make it consistent in all cases. This is considered a high-risk issue.

### Original Finding Content

## Handle

jonah1005


## Vulnerability details

## Impact
For a dai vault that pairs with NativeStrategyCurve3Crv, every time `earn()` is called, shareholders would lose money. (about 2%)

There're two issues involved. The Vault contract and the controller contract doesn't handle the price difference between the want token and other tokens. 

[Vault.sol#L293](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/Vault.sol#L293-L303) When a vault calculates its value, it sums up all tokens balance. [Controller.sol#L410-L436](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/controllers/Controller.sol#L410-L436) However, when the controller calculates vaults' value, it only adds the amount of `strategy.want` it received. (in this case, it's t3crv). 

Under the current design, users who deposit dai to the vault would not get yield. Instead, they would keep losing money. I consider this a high-risk issue



## Proof of Concept
I trigger the bug with the following web3.py script:
```python
previous_price = vault.functions.getPricePerFullShare().call()
vault.functions.available(dai.address).call()
vault.functions.earn(dai.address, strategy.address).transact()
current_price = vault.functions.getPricePerFullShare().call()
print(previous_price)
print(current_price)
```


## Tools Used
Hardhat

## Recommended Mitigation Steps

The protocol should decide what the balance sheet in each contract stands for and make it consistent in all cases. Take, for example, if `_vaultDetails[_vault].balance;` stands for the amount of 'want' token the vault owns, there shouldn't exist two different want in all the strategies the vault has. Also, when the vault queries controllers `function balanceOf()`, they should always multiply it by the price.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/9
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`vulnerability`

