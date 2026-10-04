---
# Core Classification
protocol: Yieldfi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55536
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
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
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Immeas
  - Jorge
---

## Vulnerability Title

Missing source validation in CCIP message handling

### Overview


The YieldFi platform uses Chainlink CCIP to transfer its yield tokens between different blockchains. However, there is a bug in the `BridgeCCIP` contract that allows an attacker to send a message from an untrusted source chain and potentially drain tokens from the bridge or create an unlimited amount of tokens on another blockchain. To prevent this, the report recommends implementing validation to only accept messages from trusted sources. This bug has been fixed in the latest update and has been verified by Cyfrin.

### Original Finding Content

**Description:** YieldFi integrates with Chainlink CCIP to facilitate cross-chain transfers of its yield tokens (`YToken`). This functionality is handled by the `BridgeCCIP` contract, which manages token accounting for these transfers.

However, in the [`BridgeCCIP::_ccipReceive`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L160-L181) function, there is no validation of the message sender from the source chain:
```solidity
/// handle a received message
function _ccipReceive(Client.Any2EVMMessage memory any2EvmMessage) internal override {
    bytes memory message = abi.decode(any2EvmMessage.data, (bytes)); // abi-decoding of the sent text
    BridgeSendPayload memory payload = Codec.decodeBridgeSendPayload(message);
    bytes32 _hash = keccak256(abi.encode(message, any2EvmMessage.messageId));
    require(!processedMessages[_hash], "processed");

    processedMessages[_hash] = true;

    require(payload.amount > 0, "!amount");

    ...
}
```

As a result, an attacker could craft a malicious `Any2EVMMessage` containing valid data and trigger the minting or unlocking of arbitrary tokens by sending it through CCIP to the `BridgeCCIP` contract.


**Impact:** An attacker could drain the bridge of tokens on L1 or mint an unlimited amount of tokens on L2. While a two-step redeem process offers some mitigation, such an exploit would still severely disrupt the protocol’s accounting and could be abused when claiming yield for example.

**Recommended Mitigation:** Consider implementing validation to ensure that messages are only accepted from trusted peers on the source chain:
```solidity
mapping(uint64 sourceChain => mapping(address peer => bool allowed)) public allowedPeers;
...
function _ccipReceive(
    Client.Any2EVMMessage memory any2EvmMessage
) internal override {
    address sender = abi.decode(any2EvmMessage.sender, (address));
    require(allowedPeers[any2EvmMessage.sourceChainSelector][sender],"allowed");
    ...
```

**YieldFi:** Fixed in commit [`a03341d`](https://github.com/YieldFiLabs/contracts/commit/a03341d8103ba08473ea1cd39e64192608692aca)

**Cyfrin:** Verified. `sender` is now verified to be a trusted sender.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Yieldfi |
| Report Date | N/A |
| Finders | Immeas, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

