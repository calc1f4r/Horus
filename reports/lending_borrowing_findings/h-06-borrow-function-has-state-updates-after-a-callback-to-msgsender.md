---
# Core Classification
protocol: Timeswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25636
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-timeswap
source_link: https://code4rena.com/reports/2022-01-timeswap
github_link: https://github.com/code-423n4/2022-01-timeswap-findings/issues/6

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
  - yield
  - services
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-06] borrow() function has state updates after a callback to msg.sender

### Overview


A bug was reported in TimeswapPair.sol, a Solidity smart contract. The `borrow()` function had a callback to the msg.sender in the middle of the function while there were still updates to state that take place after the callback. This could lead to cross function reentrancy, a type of attack where malicious actors can exploit a contract’s vulnerability to gain access to its resources. The callback also violated the Checks Effects Interactions best practices, which further widened the attack surface.

The recommended mitigation step was to move the callback to the end of the borrow() function after all state updates have taken place. This was confirmed and resolved by Timeswap (Mathepreneur).

### Original Finding Content

_Submitted by jayjonah8_

In TimeswapPair.sol, the `borrow()` function has a callback to the msg.sender in the middle of the function while there are still updates to state that take place after the callback.  The lock modifier guards against reentrancy but not against cross function reentrancy.  Since the protocol implements Uniswap like functionality,  this can be extremely dangerous especially with regard to composability/interacting with other protocols and contracts.  The callback before important state changes (updates to collateral, totalDebtCreated and reserves assets) also violates the Checks Effects Interactions best practices further widening the attack surface.

#### Proof of Concept

- <https://github.com/code-423n4/2022-01-timeswap/blob/main/Timeswap/Timeswap-V1-Core/contracts/TimeswapPair.sol#L322>

- <https://fravoll.github.io/solidity-patterns/checks_effects_interactions.html>

- cross function reentrancy
<https://medium.com/coinmonks/protect-your-solidity-smart-contracts-from-reentrancy-attacks-9972c3af7c21>

#### Recommended Mitigation Steps

The callback Callback.borrow(collateral, dueOut.collateral, data); should be placed at the end of the borrow() function after all state updates have taken place.

**[Mathepreneur (Timeswap) confirmed and resolved](https://github.com/code-423n4/2022-01-timeswap-findings/issues/6):**
 > https://github.com/Timeswap-Labs/Timeswap-V1-Core/pull/105





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Timeswap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-timeswap
- **GitHub**: https://github.com/code-423n4/2022-01-timeswap-findings/issues/6
- **Contest**: https://code4rena.com/reports/2022-01-timeswap

### Keywords for Search

`vulnerability`

