---
# Core Classification
protocol: Superform
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54334
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9
source_link: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
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
finders_count: 4
finders:
  - cccz
  - rvierdiiev
  - elhaj
  - bronzepickaxe
---

## Vulnerability Title

Increasing quorum requirements will prevent messages from being processed 

### Overview


The report discusses a bug in the code related to cross-chain messaging. The problem occurs when the `setRequiredMessagingQuorum` function is called to increase the required quorum between the initiation and processing of a cross-chain message. This results in the message not being processed due to insufficient `messageQuorum`. The recommendation is to cache the current quorum requirements in the payload when a cross-chain message is initiated and use it instead of the latest quorum requirements for the checks. This will prevent the message from being rejected due to insufficient `messageQuorum`. 

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
The admin can call `setRequiredMessagingQuorum` to set `requiredQuorum`:

```solidity
function setRequiredMessagingQuorum(uint64 srcChainId_, uint256 quorum_) external override onlyProtocolAdmin {
    requiredQuorum[srcChainId_] = quorum_;
    emit QuorumSet(srcChainId_, quorum_);
}
```

The message can only be processed if the number of proof messages received is greater than the `requiredQuorum`:

```solidity
if (messageQuorum[payloadProof] < _getQuorum(srcChainId)) {
    revert Error.INSUFFICIENT_QUORUM();
}
```

The problem here is that when a cross-chain message is initiated, the length of its `ambIds` is fixed, i.e. the number of messages sent is fixed, which also means that the number of received proof messages, i.e. `messageQuorum`, will not exceed it.

If `setRequiredMessagingQuorum` is called to increase the `requiredQuorum` between the initiation and processing of a cross-chain message, then when the cross-chain message is processed, it will not be processed due to insufficient `messageQuorum`:

1. Consider chain A with `requiredQuorum` 3; a user initiates a cross-chain deposit with `ambIds` length 4.
2. When the message is successfully dispatched, the admin calls `setRequiredMessagingQuorum` to increase the `requiredQuorum` to 5.
3. When the destination chain processes the message, the message will not be processed because the `messageQuorum` is at most 4 and less than 5.

## Recommendation
Consider caching the current quorum requirements in the payload when a cross-chain message is initiated, and using it instead of the latest quorum requirements for the checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | cccz, rvierdiiev, elhaj, bronzepickaxe |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9

### Keywords for Search

`vulnerability`

