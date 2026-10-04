---
# Core Classification
protocol: Wormhole
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40683
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0591640a-e6f1-460c-8553-caa681ea5551
source_link: https://cdn.cantina.xyz/reports/cantina_competition_wormhole_mar2024.pdf
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - J4X98
  - pks271
---

## Vulnerability Title

Cross-chain transactions can be replayed when the chain undergoes a hard fork 

### Overview


The bug report discusses a potential issue with the NttManager.sol code, specifically in the function "completeInboundQueuedTransfer". During a hard fork, if there are still pending transactions in the InboundQueued, they can be replayed on another chain. This is due to the lack of a checkFork(evmChainId) validation, which is present in the executeMsg function. This could potentially lead to malicious users exploiting the system and causing significant damage. The report recommends adding the checkFork(evmChainId) validation to the completeInboundQueuedTransfer function to prevent this issue.

### Original Finding Content

## Vulnerability Report

## Context
**File:** NttManager.sol  
**Lines:** 234-251  

## Description
During a hard fork, if `InboundQueued` has pending transactions, these can be replayed on another chain. The root cause is that the `NttManager.completeInboundQueuedTransfer` function lacks `checkFork(evmChainId)` validation, similar to the `executeMsg` function. 

Although the chances of exploitation are low, the impact can be significant, as malicious users could extract substantial profits. This risk is highlighted by the Omni bridge vulnerability that occurred during Ethereum's transition to a proof-of-stake consensus mechanism.

## Recommendation
Add `checkFork(evmChainId)` check to the `completeInboundQueuedTransfer` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Wormhole |
| Report Date | N/A |
| Finders | J4X98, pks271 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_wormhole_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0591640a-e6f1-460c-8553-caa681ea5551

### Keywords for Search

`vulnerability`

