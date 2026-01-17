---
# Core Classification
protocol: UMA Across V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10604
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-across-v2-audit/
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
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Slow relays on multiple chains

### Overview


This bug report is about the Across Protocol's root bundle. In Across Protocol, the root bundle consists of two parts: the slowRelayRoot and the poolRebalanceRoot. The slowRelayRoot represents all the slow relays in a batch, which could involve multiple tokens and spoke pools. The poolRebalanceRoot ensures that there is a leaf for every spoke chain. When the rebalance leaf is processed, the slowRelayRoot is sent to the corresponding spoke pool. 

The bug is that every spoke pool receives the same slowRelayRoot, which represents all slow relays in the batch across the whole system. When the slow relay is executed, the Spoke Pool does not filter on the destination chain id, which means that any slow relay can be executed on any spoke chain where the Spoke Pool has sufficient funds in the destinationToken. The bug was fixed in pull request #79, as of commit 2a41086f0d61caf0be8c2f3d1cdaf96e4f67f718. This fix included including the destination chain ID in the slow relay details so the Spoke Pool can filter out relays that are intended for other chains.

### Original Finding Content

In each root bundle, the [slowRelayRoot](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/HubPool.sol#L63) represents all the slow relays in a batch, which could involve multiple tokens and spoke pools. A valid root bundle would ensure [the `poolRebalanceRoot`](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/HubPool.sol#L59) has a leaf for every spoke chain. When this rebalance leaf is processed, the `slowRelayRoot` will also be [sent to the corresponding spoke pool](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/HubPool.sol#L566).


Notably, every spoke pool receives the same `slowRelayRoot`, which represents all slow relays in the batch across the whole system. When [the slow relay is executed](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/SpokePool.sol#L477), the Spoke Pool does not filter on the destination chain id, which means that any slow relay can be executed on any spoke chain where the Spoke Pool has sufficient funds in the `destinationToken`. Consider including the destination chain ID in the slow relay details so the Spoke Pool can filter out relays that are intended for other chains.


**Update**: *Fixed in [pull request #79](https://github.com/across-protocol/contracts-v2/pull/79) as of commit [`2a41086f0d61caf0be8c2f3d1cdaf96e4f67f718`](https://github.com/across-protocol/contracts-v2/pull/79/commits/2a41086f0d61caf0be8c2f3d1cdaf96e4f67f718).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA Across V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-across-v2-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

