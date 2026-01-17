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
solodit_id: 11348
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

[M01] Fees cannot be collected

### Overview


This bug report is about the `exercise` function of the `Option` contract. It charges a fee every time a user exercises option tokens or takes a flash loan of underlying tokens. This fee is calculated as a portion of the underlying tokens and is expected to be paid by the caller in strike tokens. However, the logic does not keep track of the added fees, so they will be lost without any possibility of collecting them.

The issue was initially solved by considering modifying the way in which fees are tracked so that they can be effectively collected. However, the concept of fee was eventually removed from the system altogether, as seen in Pull Request #16. The docstrings above the `exercise` function must be updated to reflect this.

### Original Finding Content

The [`exercise` function](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L179) of the `Option` contract charges a fee every time a user exercises option tokens or takes a flash loan of underlying tokens. This fee is calculated [as a portion of the underlying tokens](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L225) sent out by the contract, and is expected to [be paid by the caller in strike tokens](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L216).


Before finishing execution of the `exercise` function, the cached balances of strike and underlying tokens [are updated](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L250) to the latest balance [queried during the transaction](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L208-L213). However, the logic does not keep track of the added fees. Thus they will be lost without any possibility of collecting them.


Consider modifying the way in which fees are tracked so that they can be effectively collected. Related issue **“[H01] Fragile internal accounting mechanism may cause loss of funds”** should be taken into account to solve this particular issue. Alternatively, if fees do not have a clear purpose in the Primitive protocol, consider removing them from the system altogether.


**Update:** *Fixed in [PR #16](https://github.com/primitivefinance/primitive-protocol/pull/16). The concept of fee has been removed from the system altogether. The docstrings [above the `exercise` function](https://github.com/primitivefinance/primitive-protocol/blob/hotfix/audit-fixes/packages/primitive-contracts/contracts/option/primitives/Option.sol#L173) must be updated to reflect this.*

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

