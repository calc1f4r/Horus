---
# Core Classification
protocol: Opyn Gamma Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11225
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/opyn-gamma-protocol-audit/
github_link: none

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
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H01][Fixed] ETH could get trapped in the protocol

### Overview


This bug report is about the `Controller` contract, which is part of the GammaProtocol. This contract allows users to send arbitrary actions, such as flash loans, through the `_call` internal function. It also allows sending ETH with the action to then perform a call to a `CalleeInterface` type of contract. The `Controller` contract saves the original `msg.value` sent with the `operate` function call and updates the remaining ETH left after each one of those calls.

However, if the user sends more ETH than necessary for the batch of actions, the remaining ETH (stored in the `ethLeft` variable after the last iteration) will not be returned to the user and will be locked in the contract due to the lack of a `withdrawEth` function. The bug report suggests either returning all the remaining ETH to the user or creating a function that allows the user to collect the remaining ETH after performing a `Call` action type, taking into account that sending ETH with a push method may trigger the fallback function on the caller’s address.

The bug has since been fixed in PR#304, where the `payable` property has been removed from the `operate` function. However, this change also means it is impossible to do outbound calls which require ETH through the `operate` function.

### Original Finding Content

The [`Controller` contract](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L27) allows users to send arbitrary actions such as possible [flash loans](https://blog.openzeppelin.com/flash-loans-and-the-advent-of-episodic-finance/) through the [`_call` internal function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L763).


Among other features, it allows sending ETH with the action to then perform a call to a [`CalleeInterface` type of contract](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/interfaces/CalleeInterface.sol#L9).


To do so, it saves the original `msg.value` sent with the [`operate` function call](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L331) in the [`ethLeft` variable](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L460) and it [updates the remaining ETH left](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L769) after each one of those calls to revert in case that it is not enough.


Nevertheless, if the user sends more than the necessary ETH for the batch of actions, the remaining ETH (stored in the `ethLeft` variable after the last iteration) will not be returned to the user and will be locked in the contract due to the lack of a `withdrawEth` function.


Consider either returning all the remaining ETH to the user or creating a function that allows the user to collect the remaining ETH after performing a `Call` action type, taking into account that sending ETH with a push method may trigger the fallback function on the caller’s address.


**Update:** *Fixed in [PR#304](https://github.com/opynfinance/GammaProtocol/pull/304) where the `payable` property is removed from the `operate` function. However this change also means it is impossible to do outbound calls which require ETH through the `operate` function.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Opyn Gamma Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/opyn-gamma-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

