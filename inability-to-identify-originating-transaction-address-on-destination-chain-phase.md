---
# Core Classification
protocol: Avalanche Interchain Token Transfer Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34382
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/avalanche-interchain-token-transfer-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Inability to Identify Originating Transaction Address on Destination Chain - Phase 1

### Overview


The Teleporter Token Bridge contracts allow for the transfer of tokens between different subnets. However, the current implementation does not provide enough information about the sender of the original transaction, which may limit its applications. To address this, a field should be added to the message received by the targeted smart contract that represents the origin sender's address. This was partially resolved in a recent update, but it is suggested to also include the source bridge address for added security. This issue has now been fully resolved in another update.

### Original Finding Content

The Teleporter Token Bridge contracts enable the transfer of tokens between different subnets by specifying a recipient on the destination chain using the [\_send](https://github.com/ava-labs/teleporter-token-bridge/blob/f18d6f34b94708deab31cddd4eb84fd7d9a8670d/contracts/src/TeleporterTokenSource.sol#L87) method. In addition, they also support token transfers using a function call with the [\_sendAndCall](https://github.com/ava-labs/teleporter-token-bridge/blob/f18d6f34b94708deab31cddd4eb84fd7d9a8670d/contracts/src/TeleporterTokenSource.sol#L124) method. However, the context provided as input when executing these methods may not be sufficient for users as it does [not specify](https://github.com/ava-labs/teleporter-token-bridge/blob/f18d6f34b94708deab31cddd4eb84fd7d9a8670d/contracts/src/TeleporterTokenSource.sol#L151) the sender of the originating transaction.


This could impact the user experience and may limit the bridge's applications. Consider a scenario where a user wants to authenticate the original sender to restrict calls. They might configure the contract to be callable only by the bridge contract but may also need to identify who initiated the transaction on the source chain. This could be critical, especially if the contract handles value, as they would not want to receive calls from just any origin sender.


Consider including a field in the message received by the targeted smart contract that represents the origin sender's address.


***Update:** Partially resolved in [pull request #101](https://github.com/ava-labs/teleporter-token-bridge/pull/101). The Ava Labs team stated:*



> *We added the verified `sourceBlockchainID` and `originSenderAddress` values to the `receiveTokens` interfaces for both ERC-20 tokens and the native token to allow for `sendAndCall` use cases that require authenticating the caller. In a multi-hop case, these values are passed through the source chain on their intended destination. This required adding the fields to the `SingleHopCallMessage` payload. The `MultiHopCallMessage` only needs to include the `originSenderAddress` because the `sourceBlockchainID` is the source blockchain ID of the Teleporter message itself.*


*The new implementation properly passes the original caller and source blockchain ID to the recipients of the `sendAndCall` feature. This enables use cases that require authenticating the caller on the source blockchain who initiated the transaction. On top of passing the caller and the source blockchain ID, consider adding the source bridge address. This allows the recipient of the `sendAndCall` feature to ensure the `sendAndCall` was handled by a trusted source bridge contract.*


***Update 2:** Resolved in [pull request #136](https://github.com/ava-labs/teleporter-token-bridge/pull/136). The new implementation now also passes the `originBridgeAddress` to the `receiveTokens` interface in both the [`IERC20SendAndCallReceiver`](https://github.com/ava-labs/teleporter-token-bridge/blob/fe35bee8aeb6ca83a002cfca9cd9ac0772609123/contracts/src/interfaces/IERC20SendAndCallReceiver.sol#L29) and [`INativeSendAndCallReceiver`](https://github.com/ava-labs/teleporter-token-bridge/blob/fe35bee8aeb6ca83a002cfca9cd9ac0772609123/contracts/src/interfaces/INativeSendAndCallReceiver.sol#L29). This allows the recipient contracts of the `sendAndCall` feature to verify that the `sendAndCall` was handled by a trusted source bridge contract.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Avalanche Interchain Token Transfer Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/avalanche-interchain-token-transfer-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

