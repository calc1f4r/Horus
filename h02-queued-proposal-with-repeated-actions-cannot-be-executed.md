---
# Core Classification
protocol: Compound Alpha Governance System Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11543
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-alpha-governance-system-audit/
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
  - yield
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H02] Queued proposal with repeated actions cannot be executed

### Overview


The GovernorAlpha contract in the Compound Protocol Alpha allows users to propose and queue proposals with repeated actions. If a proposal with repeated actions is approved, each action in the proposal will be queued individually in the Timelock contract via subsequent calls to its queueTransaction function. All queued actions are kept in the queuedTransactions mapping of the Timelock contract. Each action is identified by the keccak256 hash of its target, value, signature, data and eta values, however all actions in the same proposal share the same eta. This can cause a problem when the time lock expires, as the whole set of actions in a proposal must be aborted if one of its actions fails. 

To fix this issue, a change was introduced to explicitly disallow proposals with repeated actions to be queued in the Timelock contract. This change ensures that each action in a proposal is identified uniquely and allows the Compound's governance system to execute queued proposals that contain repeated actions.

### Original Finding Content

The [`GovernorAlpha` contract](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Governance/GovernorAlpha.sol) allows to propose and queue proposals with repeated actions. That is, two or more actions in a proposal can have the same set of `target`, `value`, `signature` and `data` values.


Assuming a proposal with repeated actions is approved by the governance system, then [each action in the proposal will be queued individually](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Governance/GovernorAlpha.sol#L190-L192) in the `Timelock` contract via subsequent calls to its [`queueTransaction` function](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Timelock.sol#L60). All queued actions are kept in the [`queuedTransactions` mapping](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Timelock.sol#L23) of the `Timelock` contract for future execution. While each action is [identified by the `keccak256` hash](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Timelock.sol#L64-L65) of its `target`, `value`, `signature`, `data` and `eta` values, it must be noted that all actions in the same proposal share the same `eta`. As a consequence, repeated actions always produce the same identifier hash. So a single entry will be created for them in the `queuedTransactions` mapping.


When the time lock expires, the whole set of actions in a proposal can be executed atomically. In other words, the entire proposal must be aborted should one of its actions fail. To execute a proposal anyone can call the [`execute` function](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Governance/GovernorAlpha.sol#L196) of the `GovernorAlpha` contract. This will in turn call, [for each action in the proposal](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Governance/GovernorAlpha.sol#L200-L202), the [`executeTransaction` function](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Timelock.sol#L80) of the `Timelock` contract. Considering a proposal with duplicated actions, the first of them will be executed normally and [its entry in the `queuedTransactions` mapping will be set to `false`](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Timelock.sol#L88). However, the second repeated action will share the same identifier hash as the first action. As a result, its execution will inevitably fail due to the [`require` statement in line 84 of `Timelock.sol`](https://github.com/compound-finance/compound-protocol-alpha/blob/6858417c91921208c0b3ff342b11065c09665b1b/contracts/Timelock.sol#L84), thus reverting the execution of the entire proposal.


Consider modifying how each action in a proposal is identified so as to avoid clashes in their identifiers. This should allow for each action in a proposal to be identified uniquely, therefore enabling Compound’s governance system to execute queued proposals that contain repeated actions.


**Update**: *Fixed in the follow-up commit [`f5976a8a1dcf4e14e435e5581bade8ef6b5d38ea`](https://github.com/compound-finance/compound-protocol-alpha/blob/f5976a8a1dcf4e14e435e5581bade8ef6b5d38ea/contracts/Governance) which introduced a change to explicitly disallow proposals with repeated actions to be queued in the `Timelock` contract.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Alpha Governance System Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-alpha-governance-system-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

