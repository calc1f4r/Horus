---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: message_handling
vulnerability_type: message_registration

# Attack Vector Details
attack_type: message_spoofing
affected_component: codec

# Technical Primitives
primitives:
  - RegisterCodec
  - RegisterInterfaces
  - LegacyAmino
  - GetSigners
  - cosmos.msg.v1.signer
  - protobuf
  - MsgServer

# Impact Classification
severity: medium_to_high
impact: functionality_broken
exploitability: 0.7
financial_impact: medium

# Context Tags
tags:
  - cosmos_sdk
  - message_registration
  - codec
  - amino
  - protobuf
  - GetSigners
  - MsgServer
  - indexer
  - sign_mode
  
language: go
version: all
---

## References
- [deprecated-getsigners-usage.md](../../reports/cosmos_cometbft_findings/deprecated-getsigners-usage.md)
- [m-05-amino-legacy-signing-method-broken-because-of-name-mismatch.md](../../reports/cosmos_cometbft_findings/m-05-amino-legacy-signing-method-broken-because-of-name-mismatch.md)
- [m-7-addremove-authorization-messages-are-not-usable-due-to-missing-registration.md](../../reports/cosmos_cometbft_findings/m-7-addremove-authorization-messages-are-not-usable-due-to-missing-registration.md)
- [h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md](../../reports/cosmos_cometbft_findings/h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md)

## Vulnerability Title

**Cosmos SDK Message Registration and Handling Vulnerabilities**

### Overview

Cosmos SDK modules rely on proper message registration with Amino codec, Protobuf interface registry, and correct signer annotations for messages to be usable. Missing or misconfigured message registrations result in transactions failing to decode, route, or validate. Additionally, newer SDK versions deprecate GetSigners() in favor of cosmos.msg.v1.signer protobuf annotations, causing incompatibility issues. Message type confusion can also allow disguising Cosmos SDK messages as EVM transactions, breaking indexer functionality.

### Root Cause

1. **Missing message registration**: Messages not registered in RegisterCodec/RegisterInterfaces are unusable
2. **Amino name mismatch**: RegisterConcrete names must match amino.name protobuf options exactly
3. **Deprecated GetSigners**: Older messages using GetSigners() break on newer SDK versions
4. **Missing cosmos.msg.v1.signer annotation**: Required for SDK message validation
5. **Sign mode confusion**: Using SignMode_SIGN_MODE_ETHEREUM with non-EVM messages breaks indexers

### Impact Analysis

#### Technical Impact
- Transactions fail to decode or route
- Messages completely unusable via CLI, gRPC, or transactions
- Block indexing fails on type URL mismatch
- Legacy signing methods break
- Incompatibility with newer SDK versions

#### Business Impact
- Critical functionality unavailable
- User transactions rejected
- Upgrade path blocked
- Governance/authority actions impossible

### Audit Checklist
- All module messages registered in RegisterCodec and RegisterInterfaces
- RegisterConcrete names match amino.name protobuf options exactly
- cosmos.msg.v1.signer annotation present for all messages
- GetSigners() deprecated usage replaced with protobuf annotations
- MsgServer handlers exist for all registered message types
- Sign modes validated to prevent message type confusion

### Real-World Examples

| Protocol | Audit Firm | Severity | Issue |
|----------|------------|----------|-------|
| Ethos Cosmos | OtterSec | HIGH | Deprecated GetSigners usage |
| Initia | Code4rena | MEDIUM | Amino name mismatch breaks signing |
| ZetaChain | Sherlock | MEDIUM | Missing message registration |
| Initia MiniEVM | Code4rena | HIGH | Cosmos SDK message disguised as EVM tx |

### Keywords

message_registration, RegisterCodec, RegisterInterfaces, LegacyAmino, GetSigners, cosmos.msg.v1.signer, protobuf, MsgServer, amino.name, codec, SignMode_SIGN_MODE_ETHEREUM, type_url, message_spoofing, indexer
