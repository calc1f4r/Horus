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
solodit_id: 10706
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

[H01] Concurrent relays deplete reserves

### Overview


This bug report is about the `relayDeposit` function of the `BridgePool` contract. This function ensures that the contract has sufficient funds to execute the transfer, but it does not account for the pending reserves. This means that multiple simultaneous relays may rely on the same funds, and they may not all be settleable immediately. To solve this issue, it was suggested that the system should prevent relays that would cause the pending reserves to exceed the liquid reserves. 

The bug has been fixed as of commit `6290f3facbca8d878605a1d390ed59d4b6b6db02` in Pull Request 3501.

### Original Finding Content

The `relayDeposit` function of the `BridgePool` contract [ensures the contract has sufficient funds](https://github.com/UMAprotocol/protocol/blob/4cbb0986d80dfbb351caaadf203d74f0c50b4db8/packages/core/contracts/insured-bridge/BridgePool.sol#L423-L426) to execute the transfer. However, it does not account for [the pending reserves](https://github.com/UMAprotocol/protocol/blob/f24ad501c8e813cf685f72217e7f13c8f3c366df/packages/core/contracts/insured-bridge/BridgePool.sol#L51), which tracks funds that are earmarked for active relays. Therefore, multiple simultaneous relays may rely on the same funds, and they may not all be settleable immediately. In particular, with a steady stream of transfers, instant relayer returns may be delayed indefinitely.


Consider preventing relays that would cause the pending reserves to exceed the liquid reserves.


**Update:** *Fixed as of commit [`6290f3facbca8d878605a1d390ed59d4b6b6db02`](https://github.com/UMAprotocol/protocol/pull/3501/commits/6290f3facbca8d878605a1d390ed59d4b6b6db02) in [PR3501](https://github.com/UMAprotocol/protocol/pull/3501).*

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

