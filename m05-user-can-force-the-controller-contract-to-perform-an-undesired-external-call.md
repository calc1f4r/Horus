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
solodit_id: 11231
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/opyn-gamma-protocol-audit/
github_link: none

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

[M05] User can force the Controller contract to perform an undesired external call

### Overview


The Controller contract is a gateway that allows users to interact with the GammaProtocol. It enables users to open new vaults, deposit collateral, or redeem their oTokens. In addition, it enables a general transaction to be used as a flash loan in other projects. This is done by formatting the call with the CallArgs struct format. 

When the user submits the action in the operate function, the call jumps into the _call function and performs an external call to the callFunction payable function in the callee address. However, if the callee address is not a CalleeInterface based contract, and it has either a fallback or payable fallback function in it, and it is not restricted, the call coming from the Controller contract will end up executing any code under the fallback function on behalf of the Controller contract’s address. This other address could be either an asset that may be part of the whitelisted assets in the protocol or a future contract of the project that allows the execution of sensitive actions by the Controller contract. 

Therefore, it is recommended to prevent an external call on behalf of the Controller contract when the destination address is not a CalleeInterface type of contract and it is not a whitelisted address.

### Original Finding Content

The [`Controller` contract](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L27) is the users’ front gate. With it, they can interact with the protocol to either open a new vault, deposit collateral or redeem their oTokens.


Besides those actions, the contract allows the execution of a more general transaction to be used as a [flash loan](https://blog.openzeppelin.com/flash-loans-and-the-advent-of-episodic-finance/) in other projects by formatting the call with the [`CallArgs` struct format](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/libs/Actions.sol#L137).


By doing this, if the user submits that action in the [`operate` function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L331), the call would jump into the [`_call` function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L763) to then perform an external call to the [`callFunction` payable function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L770) in the [`callee` address](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/libs/Actions.sol#L141).


However, if the `callee` address is not a [`CalleeInterface` based contract](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/interfaces/CalleeInterface.sol#L9) but it has either a fallback or payable fallback function in it, and [it is not restricted](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L54) the whitelisted addresses, the call coming from the `Controller` contract will end up executing any code under the fallback function on behalf of the `Controller` contract’s address. This other address could be either an asset that may be part of the whitelisted assets in the protocol or a future contract of the project that allows the execution of sensitive actions by the `Controller` contract.


Consider preventing an external call on behalf of the `Controller` contract when the destination address is not a `CalleeInterface` type of contract and it is not a whitelisted address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

