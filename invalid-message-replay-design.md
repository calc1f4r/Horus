---
# Core Classification
protocol: Olympus DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48243
audit_firm: OtterSec
contest_link: https://www.olympusdao.finance/
source_link: https://www.olympusdao.finance/
github_link: https://github.com/OlympusDAO/bophades/tree/xchain/

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
  - liquid_staking
  - yield
  - cross_chain
  - leveraged_farming
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Youngjoo Lee
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Invalid Message Replay Design

### Overview


This bug report discusses a problem with a feature called "replay" in the CrossChainBridge smart contract. When this feature is used, there is a direct internal call to a function called _receiveMessage. However, there is a code error that causes an access control check to fail, which means that the feature does not work properly. This can result in the contract becoming permanently locked and causing issues with OHM tokens. The suggested solution is to mirror a different endpoint that will properly set the sender address. This issue has been fixed in a recent update.

### Original Finding Content

## Replay Messages and Access Control Issues

When messages are replayed, there’s a direct internal call to `_receiveMessage`.

### Source Code Reference
`src/policies/CrossChainBridge.sol` (SOLIDITY)

```solidity
// Execute the message. revert if it fails again
_receiveMessage(srcChainId_, srcAddress_, nonce_, payload_);
emit RetryMessageSuccess(srcChainId_, srcAddress_, nonce_, payloadHash);
```

However, this code performs an access control check on the sender, which will cause the invocation to abort.

### Source Code Reference
`src/policies/CrossChainBridge.sol` (SOLIDITY)

```solidity
// Needed to restrict access to low-level call from lzReceive
if (msg.sender != address(this)) revert Bridge_InvalidCaller();
```

As a result, the replay feature does not work. Messages that failed the initial invocation would lead to permanently locking up OHM tokens in the contract.

## Remediation

Consider mirroring the LayerZero endpoint, which performs an external call to properly set `msg.sender`.

### Source Code Reference
`Endpoint.sol` (SOLIDITY)

```solidity
ILayerZeroReceiver(dstAddress).lzReceive(_srcChainId, _srcAddress, nonce, _payload);
emit PayloadCleared(_srcChainId, _srcAddress, nonce, dstAddress);
```

## Patch

Fixed in #120.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Olympus DAO |
| Report Date | N/A |
| Finders | Youngjoo Lee, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.olympusdao.finance/
- **GitHub**: https://github.com/OlympusDAO/bophades/tree/xchain/
- **Contest**: https://www.olympusdao.finance/

### Keywords for Search

`vulnerability`

