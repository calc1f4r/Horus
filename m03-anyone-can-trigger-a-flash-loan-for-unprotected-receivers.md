---
# Core Classification
protocol: Primitive Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11350
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/primitive-audit/
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
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M03] Anyone can trigger a flash loan for unprotected receivers

### Overview


This bug report is about an issue with the `exercise` function in the `Option` contract of the Primitive protocol. This function allows anyone to execute a flash loan of underlying tokens deposited in the contract. The caller can specify any contract address that implements the `IFlash` interface as the `receiver` parameter. If the receiver contract does not implement the necessary validations to identify who originally triggered the transaction, it may be possible for an attacker to force any `IFlash` contract to open arbitrary flash loans in the Primitive protocol, draining all tokens in balance from the vulnerable contract.

The bug has been partially fixed in PR#17, where the call to the receiver’s `primitiveFlash` function now passes the `msg.sender` address as argument, so as to inform the receiver who the caller of the `exercise` function is. However, the project is still lacking user-friendly documentation and examples to guide the development of secure implementations of receiver contracts. For this reason, it is advisable to modify the flash loan logic so that only the actual receiver of the loan can execute it. If opening flash loans on behalf of `IFlash` contracts is an intended feature, then consider adding user-friendly documentation to raise awareness, along with sample implementations showcasing how to defend from attackers.

### Original Finding Content

The [`exercise` function](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L179) of the `Option` contract allows anyone to execute a flash loan of underlying tokens deposited in the contract. The caller can specify in the [`receiver` parameter](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L180) any contract address [that implements the `IFlash` interface](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L205).


Should the receiver contract not implement the necessary validations to identify who originally triggered the transaction, it may be possible for an attacker to force any `IFlash` contract to open arbitrary flash loans in the Primitive protocol that would inevitably [pay the corresponding fees](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L225) (in strike tokens). This can potentially drain all tokens in balance from the vulnerable contract implementing the `IFlash` interface. It should be highlighted that the [`Flash` contract](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/test/Flash.sol) (used for testing purposes) is the only available example of an implementation of the `IFlash` interface, and it does not include any security measure, nor warning documentation, to prevent this issue.


To reduce the attack surface, it is advisable to modify the flash loan logic so that only the actual receiver of the loan can execute it. If opening flash loans on behalf of `IFlash` contracts is an intended feature, then consider adding user-friendly documentation to raise awareness, along with sample implementations showcasing how to defend from attackers that attempt to open flash loans on behalf of unprotected `IFlash` contracts. Finally, any solution for this issue should take into consideration what is described in related issue **“[M07] Convoluted implementation of exercise and flash loan features”**.


**Update**: *Partially fixed in [PR#17](https://github.com/primitivefinance/primitive-protocol/pull/17). The call to the receiver’s `primitiveFlash` function now passes the `msg.sender` address as argument, so as to inform the receiver who the caller of the `exercise` function is. However, the project is still lacking user-friendly documentation and examples to guide the development of secure implementations of receiver contracts.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Primitive Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/primitive-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

