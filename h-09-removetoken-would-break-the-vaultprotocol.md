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
solodit_id: 770
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/4

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

[H-09] removeToken would break the vault/protocol.

### Overview


This bug report is about a vulnerability in Manager.sol, which is part of the code-423n4/2021-09-yaxis project. The vulnerability is that the removeToken function does not have any safety checks. This would lead to the token being locked in the original vault, the Controller's balanceOf no longer reflecting the real value, and the share price in the vault decreasing drastically. The bug was tested using Hardhat and a web3.py script, which confirmed the bug.

The recommended mitigation steps involve withdrawing all tokenA from all strategies and the vault, converting it to tokenB, and transferring the tokenB to the vault. This should be thoroughly tested to ensure that all components' states are correctly handled.

### Original Finding Content

## Handle

jonah1005


## Vulnerability details

## removeToken would break the vault.


## Impact
There's no safety check in Manager.sol's removeToken. [Manager.sol#L454-L487](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/Manager.sol#L454-L487)
1. The token would be locked in the original vault. Given the current design, the vault would keep a ratio of total amount to save the gas. Once the token is removed at manager contract, these token would lost.
2. Controller's balanceOf would no longer reflects the real value. [Controller.sol#L488-L495](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/controllers/Controller.sol#L488-L495) While `_vaultDetails[msg.sender].balance;` remains the same, user can nolonger withdraw those amount.
3. Share price in the vault would decrease drastically. The share price is calculated as `totalValue / totalSupply` [Vault.sol#L217](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/Vault.sol#L217). While the `totalSupply` of the share remains the same, the total balance has drastically decreased.

Calling removeToken way would almost break the whole protocol if the vault has already started. I consider this is a high-risk issue.


## Proof of Concept

We can see how the vault would be affected with below web3.py script.
```python
print(vault.functions.balanceOfThis().call())
print(vault.functions.totalSupply().call())
manager.functions.removeToken(vault.address, dai.address).transact()
print(vault.functions.balanceOfThis().call())
print(vault.functions.totalSupply().call())
```

output
```
100000000000000000000000
100000000000000000000000
0
100000000000000000000000
```
## Tools Used
Hardhat

## Recommended Mitigation Steps
Remove tokens from a vault would be a really critical job. I recommend the team cover all possible cases and check all components' states (all vault/ strategy/ controller's state) in the test.

 Some steps that I try to come up with that is required to remove TokenA from a vault.
 1. Withdraw all tokenA from all strategies (and handle it correctly in the controller).
 2. Withdraw all tokenA from the vault.
 3. Convert all tokenA that's collected in the previous step into tokenB.
 4. Transfer tokenB to the vault and compensate the transaction fee/slippage cost to the vault.

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
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/4
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`vulnerability`

