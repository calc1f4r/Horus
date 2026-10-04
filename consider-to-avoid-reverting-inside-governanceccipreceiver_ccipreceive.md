---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52942
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/cc661600-b854-49ec-8d9a-90d164b65f28
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_february2025.pdf
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Anurag Jain
  - StErMi
---

## Vulnerability Title

Consider to avoid reverting inside GovernanceCCIPReceiver._ccipReceive 

### Overview

See description below for full details.

### Original Finding Content

## GovernanceCCIPReceiver._ccipReceive Reversion Issues

## Context
(No context files were provided by the reviewer)

## Description
When `GovernanceCCIPReceiver._ccipReceive` is executed by the CCIP framework and the logic reverts in any way, the message could be "manually executed" (retried) in a permissionless way by interacting directly with Chainlink CCIP (see the Chainlink Manual Execution documentation). This could create edge cases, problems, and unexpected behaviors depending on the client's needs and expectations.

The suggestion in this case is to always prevent any possible revert by using `try/catch` and providing the correct amount of `gasLimit` (as part of the message's `extraArgs` configuration) when the message is sent from the relay contract. At this point, the client has two options:

1. Save locally the failed messages and implement a custom logic to retry them eventually.
2. Ignore the failed message and re-execute the whole process by triggering again `GovernanceCCIPRelay.relayMessage`.

In any case, the client should monitor these failures by emitting a corresponding event inside the catch clause of the `try/catch` statement:

```solidity
event MessageExecuted(
    bytes32 messageId,
    uint64 sourceChainSelector,
    address messageSender,
    address target,
    bytes payload,
    bytes memory error
);
```

## Recommendation
Cryptex should consider avoiding any possible reverts inside the execution of `GovernanceCCIPReceiver._ccipReceive` and implement a custom behavior, if needed, to manage the retry of the execution of such failed messages.

## Cryptex
Implemented in PR 173. Following changes have been made:
- Does not revert when target call fails.
- Emits `MessageExecutionFailed(messageId, target, payload, _error)` when target call fails.
- Emits `MessageExecutedSuccessfully(messageId, target, payload)` when message call succeeds.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | Anurag Jain, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/cc661600-b854-49ec-8d9a-90d164b65f28

### Keywords for Search

`vulnerability`

