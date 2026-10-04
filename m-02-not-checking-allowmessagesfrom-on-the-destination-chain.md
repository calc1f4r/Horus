---
# Core Classification
protocol: Ionprotocol July
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36520
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review-July.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Not checking `allowMessagesFrom` on the destination chain

### Overview


This bug report discusses a problem with the Cross-chain Teller contract. The contract has different configurations for each supported chain, which allow it to send and receive messages. However, when receiving a cross-chain message, the contract does not consider the configuration for receiving messages from the other chain. This can lead to potential issues, such as allowing malicious activity from a chain that is not supposed to be receiving messages. The report recommends checking the configuration for receiving messages from the other chain to prevent these issues.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

The Cross-chain Teller contract has configurations for each supported chain. They can separately configure whether to only receive messages (`allowMessagesFrom`), only send messages (`allowMessagesTo`), or have both configured as true or false.

```solidity
    function addChain(
        uint32 chainSelector,
        bool allowMessagesFrom,
        bool allowMessagesTo,
        address targetTeller,
        uint64 messageGasLimit
    ) external requiresAuth {
        if (allowMessagesTo && messageGasLimit == 0) {
            revert CrossChainTellerBase_ZeroMessageGasLimit();
        }
        selectorToChains[chainSelector] = Chain(allowMessagesFrom, allowMessagesTo, targetTeller, messageGasLimit);

        emit ChainAdded(chainSelector, allowMessagesFrom, allowMessagesTo, targetTeller, messageGasLimit);
    }
```

However, when receiving cross-chain message, it doesn't consider the `allowMessagesFrom` flag.

```solidity
    function _lzReceive(
        Origin calldata _origin,
        bytes32 _guid,
        bytes calldata payload,
        address,  // Executor address as specified by the OApp.
        bytes calldata  // Any extra data or options to trigger on receipt.
    ) internal override {
        // @audit - not checking "allowMessagesFrom"
        // Decode the payload to get the message
        (uint256 shareAmount, address receiver) = abi.decode(payload, (uint256,address));
        vault.enter(address(0), ERC20(address(0)), 0, receiver, shareAmount);
    }
```

```solidity
    function receiveBridgeMessage(address receiver, uint256 shareMintAmount) external{
        // @audit - not checking receive chain from?
        if(msg.sender != address(messenger)){
            revert CrossChainOPTellerWithMultiAssetSupport_OnlyMessenger();
        }

        if(messenger.xDomainMessageSender() != peer){
            revert CrossChainOPTellerWithMultiAssetSupport_OnlyPeerAsSender();
        }

        vault.enter(address(0), ERC20(address(0)), 0, receiver, shareMintAmount);
    }
```

This can potentially cause issues. For instance, if the supported chain configuration only allows sending messages to the destination chain (`allowMessagesTo` is true) but does not allow receiving messages from that chain (`allowMessagesFrom` is set to false). Another scenario is in the case of an emergency where the other chain has a malicious activity that needs to prevent receiving messages from that chain.

**Recommendations**

Check `allowMessagesFrom` when receiving a message from the other chain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ionprotocol July |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review-July.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

