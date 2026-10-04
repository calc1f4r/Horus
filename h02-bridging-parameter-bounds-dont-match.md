---
# Core Classification
protocol: UMA Audit – L2 Bridges
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10707
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-audit-l2-bridges/
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
  - bridge
  - cdp
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H02] Bridging parameter bounds don’t match

### Overview


The bug report is about the `deposit` function of the `BridgeDepositBox` contract, which is used to bridge funds between the layer 2 (L2) and layer 1 (L1) chains. The `deposit` function uses inclusive bounds to restrict the relay fees, while the associated L1 `BridgePool` uses exclusive bounds. This means that some deposits (with 25% relay fees) cannot be relayed, and the funds will be inaccessible on both layers.

To fix this issue, the validations on both layers were synchronized to ensure all valid deposits can be relayed. This was done in commit `2345966b3a2ace0159379b3a13256cc1a4c5d52f` of pull request 3494. Initially, the severity of the bug was classified as ‘critical’, but it was downgraded when the UMA team pointed out that the funds would not be strictly trapped and could be released if the DVM (Decentralized Virtual Machine) voters agreed to accept a modified relay description for affected deposits.

### Original Finding Content

The [`deposit` function](https://github.com/UMAprotocol/protocol/blob/f24ad501c8e813cf685f72217e7f13c8f3c366df/packages/core/contracts-ovm/insured-bridge/implementation/BridgeDepositBox.sol#L169) of the `BridgeDepositBox` contract, deployed on layer 2 chains, is used to bridge funds between the L2 and L1. In particular, relayers are incentivized to [relay](https://github.com/UMAprotocol/protocol/blob/f24ad501c8e813cf685f72217e7f13c8f3c366df/packages/core/contracts/insured-bridge/BridgePool.sol#L238) the transaction details on the associated L1 `BridgePool`. However, the deposit box uses [inclusive bounds](https://github.com/UMAprotocol/protocol/blob/f24ad501c8e813cf685f72217e7f13c8f3c366df/packages/core/contracts-ovm/insured-bridge/implementation/BridgeDepositBox.sol#L181) to restrict the relay fees, while the bridge pool uses [exclusive bounds](https://github.com/UMAprotocol/protocol/blob/f24ad501c8e813cf685f72217e7f13c8f3c366df/packages/core/contracts/insured-bridge/BridgePool.sol#L244-L248). This means that some deposits (with 25% relay fees) cannot be relayed, and the funds will be inaccessible on both layers.


Consider synchronizing the validations on both layers to ensure all valid deposits can be relayed.


**Update:** *Fixed in commit [`2345966b3a2ace0159379b3a13256cc1a4c5d52f`](https://github.com/UMAprotocol/protocol/pull/3494/commits/2345966b3a2ace0159379b3a13256cc1a4c5d52f) of [PR3494](https://github.com/UMAprotocol/protocol/pull/3494). This was originally classified as Critical severity but was downgraded when the UMA team pointed out the funds would not be strictly trapped and could be released if the DVM voters agreed to accept a modified relay description for affected deposits.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA Audit – L2 Bridges |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-audit-l2-bridges/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

