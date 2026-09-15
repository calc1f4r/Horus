---
# Core Classification
protocol: Compound III Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10554
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-iii-audit/
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
  - bridge
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

The protocol may end up holding collateral assets in an unwanted manner

### Overview


The Comet contract contains an immutable value, which defines the target amount of reserves of the base token. This value is closely related to the buyCollateral function, which cannot be called successful if the protocol reserves are greater than or equal to this target. If this target is set to a small value, the contract could easily reach the level. This would mean that the protocol would be unable to sell the collateral, potentially resulting in the loss of value over time. In the opposite case, where the target is set to a large value, the chance of reaching this level would be much lower, making it a useless constraint.

It is recommended to set the target to a large value, and if it is too high to have a useful purpose, consider redesigning the system to not make use of it. The team has acknowledged this and is conducting research around liquidation auction strategies to identify the best strategy for the protocol to build up reserves.

### Original Finding Content

The Comet contract has an [immutable value](https://github.com/compound-finance/comet/blob/0f1221967149115f50a09681eea9580879ee7720/contracts/Comet.sol#L110) that defines the target amount of reserves of the base token. This value is closely related to the [buyCollateral](https://github.com/compound-finance/comet/blob/0f1221967149115f50a09681eea9580879ee7720/contracts/Comet.sol#L1232) function. This function cannot be called successful if the protocol reserves are greater than or equal to this target.


If `targetReserves` is set to a small value, the contract could easily reach the level. The problem is that the [absorptions](https://github.com/compound-finance/comet/blob/0f1221967149115f50a09681eea9580879ee7720/contracts/Comet.sol#L1153) can continue but the protocol will not be able to sell the collateral because the `buyCollateral` function cannot be used and the protocol could be in a situation where it would hold assets that may lose value over time.


In the opposite case, where `targetReserves` is set to a large value, the chance of reaching this level would be much lower so it could be a useless constraint.


Keeping in mind that setting this variable to a small value is more of a problem, be sure to set it to a large value. Also if the value of the target is too high to not have a useful or practical use, consider re-design the system to not make use of it.


**Update**: *Acknowledged. In the words of the team: “We intend for `targetReserves` to be a pretty large value so the protocol can use liquidations to build up a sizable reserve. Once reserves have reached `targetReserves`, we believe it may be advantageous for the protocol to start HODLing the collateral assets. We’ve run backtesting simulations to identify this as the best strategy for the protocol to build up reserves, but this strategy can definitely change as we conduct more research around liquidation auction strategies.”*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound III Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-iii-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

