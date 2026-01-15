---
# Core Classification
protocol: Augur Core v2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11507
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/augur-core-v2-audit/
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
  - prediction_market
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H01] Implementation of EIP 777 does not fully match the specification

### Overview


This bug report is regarding the implementation of EIP 777, a standard for tokens on the Ethereum network, and the related contracts. Specifically, the report identifies mismatches between the EIP 777 specification and the related implementation contracts. These include missing functions, incorrect parameter types, return values that are not specified in the EIP 777 standard, and functions that do not follow the EIP 777 specification. Augur developers acknowledge some of these mismatches in an inline comment.

In addition, the report states that a critical regression error was introduced when an attempt was made to fix the issue, where the mint function of the VariableSupplyToken was modified to call the ERC777 tokensReceived hook. This allowed malicious token holders to prevent the migration from finishing, potentially never allowing the isMigratingFromLegacy flag to be set to false.

In order to fix this issue, it is recommended to either avoid calling the implemented token ERC777 altogether, or to follow OpenZeppelin’s ERC777 implementation which is released in the 2.3.0 version.

### Original Finding Content

The following mismatches between the [EIP 777 specification](https://eips.ethereum.org/EIPS/eip-777) and the related implementation contracts (*i.e.* [`ERC777Token`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777Token.sol), [`ERC777BaseToken`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777BaseToken.sol), [`ERC777TokensRecipient`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777TokensRecipient.sol) and [`ERC777TokensSender`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777TokensSender.sol)) were identified.


* In [`ERC777Token`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777Token.sol), the following functions are missing from the ERC777 interface: `name()`, `symbol()`, `totalSupply()`, `balanceOf(address)`, `granularity()`, `burn(uint256,bytes)` and `operatorBurn(address,uint256,bytes,bytes)`. It is worth highlighting that `burn(uint256,bytes)` and `operatorBurn(address,uint256,bytes,bytes)` are the only functions never implemented in child contracts.
* In [`ERC777Token`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777Token.sol), [`ERC777TokensSender`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777TokensSender.sol) and [`ERC777TokensRecipient`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777TokensRecipient.sol), all function and event parameters defined as type `bytes32` should be defined as `bytes`.
* In [`ERC777Token`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777Token.sol), the `authorizeOperator(address)`, `revokeOperator(address)`, `send(address,uint256,bytes)` and `operatorSend(address,address,uint256,bytes,bytes)` functions return a success `bool` while the EIP 777 standard does not specify a return value for any of those functions.
* The [`ERC777BaseToken`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777BaseToken.sol) [contract](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777BaseToken.sol) does not implement the `burn(uint256,bytes)` and `operatorBurn(address,uint256,bytes,bytes)` functions, which as mentioned, are missing from the [`ERC777Token`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777Token.sol) interface. Augur developers acknowledge this situation in [an inline comment](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777Token.sol#L17).
* The [`ERC777BaseToken`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777BaseToken.sol) [contract](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777BaseToken.sol) implements a public [`sendNoHooks`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777BaseToken.sol#L49) [function](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777BaseToken.sol#L49) that allows the caller to transfer tokens bypassing the `tokensReceived` and `tokensToSend` hooks of the sender and receiver, a feature [completely opposite to the EIP 777 specification](https://eips.ethereum.org/EIPS/eip-777#sending-tokens).
* The [`mint`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/VariableSupplyToken.sol#L13) [function](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/VariableSupplyToken.sol#L13) of `VariableSupplyToken` does not call the [`callRecipient`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777BaseToken.sol#L122) function of `ERC777BaseToken`, thus never calling the receiver’s `tokensReceived` hook. According to [the EIP 777 spec](https://eips.ethereum.org/EIPS/eip-777#minting-tokens), calling such hook is a MUST when minting tokens.
* The [`Minted`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777Token.sol#L29) [event](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/ERC777Token.sol#L29) defined in `ERC777Token` is never emitted when minting tokens in the [`mint`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/VariableSupplyToken.sol#L13) [function](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/VariableSupplyToken.sol#L13) of `VariableSupplyToken`. According to [the EIP 777 spec](https://eips.ethereum.org/EIPS/eip-777#minting-tokens), emitting such event is a MUST when minting tokens.
* According to the spec, the `tokensToSend` hook MUST be called *before* the token’s state is updated. Similarly, the `tokensReceived` hook MUST be called *after* the token’s state is updated. However, the function [`transferFrom`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/StandardToken.sol#L26) of the `StandardToken` contract [modifies the token’s state](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/token/StandardToken.sol#L31) (*i.e.* the allowances) before the `tokensToSend` hook is called.


Many of these particular noncompliances seem to be known by Augur’s development team, who still decided to move forward with their custom implementation of EIP 777. This kind of decisions come with trade-offs. While the deviations from the spec may be more suitable for the Augur protocol, they might potentially cause errors in clients interacting with Augur that expect a fully-compliant implementation of the EIP 777. Therefore, it is advisable to either avoid calling the implemented token ERC777 altogether (its similarities and differences with the standard spec could be described in end-user documentation), or instead fully comply with the EIP’s specification by following [OpenZeppelin’s ERC777 implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/v2.3.0/contracts/token/ERC777), released in the 2.3.0 version.


***Update:*** *in an* [*attempt to fix*](https://github.com/AugurProject/augur/pull/2510) *this issue, where the* *`mint`* *function of the* *`VariableSupplyToken`* *was modified to call the ERC777* *`tokensReceived`* *hook, a critical regression error has been introduced. The* *`migrateBalanceFromLegacyRep`* *function of the* *`OldLegacyRepToken`* *contract must be called for every token holder to complete the migration, and as* *`mint`* *now calls the* *`tokensReceived`* *hook, any holder can revert attempts to mint new tokens for them. As a result, malicious tokens holders can prevent the migration from finishing (i.e. potentially never allowing the* *`isMigratingFromLegacy`* *flag to be set to* *`false`**).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Augur Core v2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/augur-core-v2-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

