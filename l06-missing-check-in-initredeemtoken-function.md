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
solodit_id: 11362
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/primitive-audit/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L06] Missing check in initRedeemToken function

### Overview

See description below for full details.

### Original Finding Content

The Primitive protocol intends to have a single redeem token associated with each `Option` contract. This redeem token can only be set once. Only the owner of the [`OptionFactory` contract](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/applications/factories/OptionFactory.sol#L19) can call the [`initialize` function](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/applications/factories/OptionFactory.sol#L64-L70) which in turns calls the [`initRedeemToken` function](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L78-L81) in the [`Option` contract](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L28). The owner of the `OptionFactory` contract is the [`Registry` contract](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/applications/Registry.sol#L23) which deploys the factory contract by calling the [`deployOption` function](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/applications/Registry.sol#L56-L90).


In summary, `Option` contracts are deployed via the factory, and the factory is owned by the registry, and there does not seem to be a way of setting the redeem token for an option twice. However, future changes to the code base might introduce viable ways of doing it.


Since setting the redeem token is an important functionality of the Primitive protocol, in order to reduce the attack surface, consider adding an explicit check in the [`initRedeemToken` function](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L78) that verifies that the address of `redeemToken` is zero [before setting it to the passed `_redeemToken` address](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L80).


**Update:** *Fixed in [PR #29](https://github.com/primitivefinance/primitive-protocol/pull/29).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

