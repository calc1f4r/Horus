---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bridge
vulnerability_type: hyperlane_integration

# Attack Vector Details (Required)
attack_type: ism_bypass|message_replay|handle_exploitation|mailbox_abuse
affected_component: Mailbox|ISM|Router|Warp

# Bridge-Specific Fields
bridge_provider: hyperlane
bridge_attack_vector: ism_validation|message_dispatch|handle_callback|interchain_security

# Technical Primitives (Required)
primitives:
  - Mailbox
  - dispatch
  - process
  - handle
  - ISM
  - interchainSecurityModule
  - enrollRemoteRouter
  - routers
  - TokenRouter
  - WarpRoute
  - quoteGasPayment
  - payForGas

# Impact Classification (Required)
severity: high|medium|low
impact: unlimited_minting|fund_loss|message_replay|state_corruption
exploitability: 0.75
financial_impact: critical

# Context Tags
tags:
  - defi
  - bridge
  - cross_chain
  - hyperlane
  - ism
  - mailbox
  - interchain

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### ISM (Interchain Security Module) Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing ISM Validation | `reports/bridge_crosschain_findings/m-02-missing-ism-validation.md` | MEDIUM | OtterSec |

### Message Replay Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Failed Message Replay | `reports/bridge_crosschain_findings/h-01-failed-message-can-be-replayed-to-mint-tokens-repeatedly.md` | HIGH | OtterSec |

### External Links
- [Hyperlane Documentation](https://docs.hyperlane.xyz/)
- [Hyperlane Security](https://docs.hyperlane.xyz/docs/protocol/security)
- [ISM Guide](https://docs.hyperlane.xyz/docs/reference/ISM)

---

# Hyperlane Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Hyperlane Cross-Chain Security Audits**

---

## Table of Contents

1. [ISM Validation Vulnerabilities](#1-ism-validation-vulnerabilities)
2. [Message Replay Attacks](#2-message-replay-attacks)
3. [Router Configuration Issues](#3-router-configuration-issues)
4. [Handle Function Vulnerabilities](#4-handle-function-vulnerabilities)
5. [Gas Payment Issues](#5-gas-payment-issues)

---

## 1. ISM Validation Vulnerabilities

### Overview

Hyperlane's Interchain Security Module (ISM) is the core security primitive. Each contract receiving cross-chain messages should verify messages through an ISM. Missing or incorrect ISM configuration allows attackers to forge messages and bypass security.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/m-02-missing-ism-validation.md` (OtterSec)

### Vulnerability Description

#### Root Cause

Contracts that receive Hyperlane messages fail to configure or validate the ISM properly, allowing arbitrary message acceptance without proper signature/proof verification.

#### Attack Scenario

1. Protocol deploys Hyperlane receiver without setting ISM
2. Default ISM may be permissive or not configured
3. Attacker calls `Mailbox.process()` with forged message
4. Without ISM validation, message is processed as legitimate
5. Attacker mints tokens or corrupts state

### Vulnerable Pattern Examples

**Example 1: Missing ISM Configuration** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/m-02-missing-ism-validation.md`
```solidity
// ❌ VULNERABLE: No ISM set
contract VulnerableReceiver is IMessageRecipient {
    // Missing: interchainSecurityModule not set!
    
    function handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) external override {
        // No verification that message came through ISM
        // Attacker can call Mailbox.process() with any message
        
        _processMessage(_origin, _sender, _message);
    }
}
```

**Example 2: Permissive ISM** [HIGH]
```solidity
// ❌ VULNERABLE: Always returns true
contract AlwaysTrueISM is IInterchainSecurityModule {
    function moduleType() external pure returns (uint8) {
        return 0; // NULL type
    }
    
    function verify(
        bytes calldata _metadata,
        bytes calldata _message
    ) external pure returns (bool) {
        return true;  // Always accepts!
    }
}
```

**Example 3: No Sender Validation** [HIGH]
```solidity
// ❌ VULNERABLE: Any sender accepted
contract WeakReceiverValidation is Router {
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override {
        // Missing: No check that _sender is enrolled router!
        // Attacker can send from any address on origin chain
        
        _processMessage(_message);
    }
}
```

### Impact Analysis

#### Technical Impact
- **Message Forgery**: Arbitrary messages processed as legitimate
- **Unlimited Minting**: Attacker can mint unlimited tokens
- **State Corruption**: Protocol state can be arbitrarily modified

#### Business Impact
- **Total Fund Loss**: Attacker drains all protocol value
- **Token Devaluation**: Unlimited minting destroys token value
- **Protocol Insolvency**: Unable to honor obligations

### Secure Implementation

**Fix 1: Proper ISM Configuration**
```solidity
// ✅ SECURE: ISM properly configured and validated
contract SecureReceiver is Router {
    using TypeCasts for bytes32;
    
    IInterchainSecurityModule public interchainSecurityModule;
    
    constructor(address _mailbox, address _ism) Router(_mailbox) {
        require(_ism != address(0), "ISM required");
        interchainSecurityModule = IInterchainSecurityModule(_ism);
    }
    
    function setInterchainSecurityModule(address _ism) external onlyOwner {
        require(_ism != address(0), "Zero address");
        interchainSecurityModule = IInterchainSecurityModule(_ism);
        emit ISMUpdated(_ism);
    }
    
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override {
        // Router base class already validates enrolled routers
        // Additional application-specific validation here
        
        _processMessage(_origin, _sender, _message);
    }
}
```

**Fix 2: Use MultisigISM**
```solidity
// ✅ SECURE: Deploy with MultisigISM for strong security
contract DeploySecureReceiver {
    function deploy(
        address mailbox,
        address[] memory validators,
        uint8 threshold
    ) external returns (address) {
        // Deploy MultisigISM with M-of-N validation
        MultisigISM ism = new MultisigISM(validators, threshold);
        
        SecureReceiver receiver = new SecureReceiver(
            mailbox,
            address(ism)
        );
        
        return address(receiver);
    }
}
```

---

## 2. Message Replay Attacks

### Overview

Failed Hyperlane messages that can be retried are a common attack vector. If the protocol doesn't properly track message processing state, attackers can replay failed messages multiple times for repeated effects (e.g., minting tokens).

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-01-failed-message-can-be-replayed-to-mint-tokens-repeatedly.md` (OtterSec)

### Vulnerability Description

#### Root Cause

When message processing fails (reverts), the protocol may not mark the message as consumed. Subsequent retries process the message again, causing double-spend or unlimited minting.

#### Attack Scenario

1. Attacker initiates cross-chain token transfer
2. On destination, message processing partially succeeds but then reverts
3. Message ID not marked as processed due to revert
4. Attacker retries message processing
5. Tokens are minted again
6. Repeat for unlimited minting

### Vulnerable Pattern Examples

**Example 1: No Message ID Tracking** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-01-failed-message-can-be-replayed-to-mint-tokens-repeatedly.md`
```solidity
// ❌ VULNERABLE: Message can be replayed on failure
contract VulnerableTokenBridge is Router {
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override {
        (address recipient, uint256 amount) = abi.decode(_message, (address, uint256));
        
        // If this reverts, message can be retried
        // and tokens minted again!
        _mintTokens(recipient, amount);
        
        // External call that might fail
        recipient.call{value: 0}("");  // If this reverts, replay possible
    }
}
```

**Example 2: Incomplete Failure Handling** [HIGH]
```solidity
// ❌ VULNERABLE: State changed before potential revert
contract IncompleteFailureHandling is Router {
    mapping(bytes32 => bool) public processedMessages;
    
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override {
        bytes32 messageId = keccak256(_message);
        
        // Tokens minted first
        (address recipient, uint256 amount) = abi.decode(_message, (address, uint256));
        token.mint(recipient, amount);  // State changed!
        
        // Then mark as processed
        // If revert happens between mint and this line,
        // message can be replayed
        processedMessages[messageId] = true;
        
        // External call that might revert
        _notifyRecipient(recipient, amount);
    }
}
```

### Secure Implementation

**Fix 1: Mark Message Before Processing**
```solidity
// ✅ SECURE: Mark processed before state changes
contract SecureTokenBridge is Router {
    mapping(bytes32 => bool) public processedMessages;
    
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override {
        // Generate unique message ID
        bytes32 messageId = keccak256(abi.encode(
            _origin,
            _sender,
            _message,
            block.chainid
        ));
        
        // Check and mark FIRST (before any state changes)
        require(!processedMessages[messageId], "Already processed");
        processedMessages[messageId] = true;
        
        // Now safe to process
        (address recipient, uint256 amount) = abi.decode(_message, (address, uint256));
        _mintTokens(recipient, amount);
    }
}
```

**Fix 2: Use Try-Catch with Proper Tracking**
```solidity
// ✅ SECURE: Track failures separately
contract SecureWithRetry is Router {
    mapping(bytes32 => MessageStatus) public messageStatus;
    
    enum MessageStatus { None, Pending, Completed, Failed }
    
    struct FailedMessage {
        uint32 origin;
        bytes32 sender;
        bytes message;
    }
    
    mapping(bytes32 => FailedMessage) public failedMessages;
    
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override {
        bytes32 messageId = _getMessageId(_origin, _sender, _message);
        
        require(
            messageStatus[messageId] == MessageStatus.None ||
            messageStatus[messageId] == MessageStatus.Failed,
            "Already processed or pending"
        );
        
        messageStatus[messageId] = MessageStatus.Pending;
        
        try this._processMessage(_message) {
            messageStatus[messageId] = MessageStatus.Completed;
        } catch {
            messageStatus[messageId] = MessageStatus.Failed;
            failedMessages[messageId] = FailedMessage(_origin, _sender, _message);
            emit MessageFailed(messageId);
        }
    }
    
    function retryFailedMessage(bytes32 messageId) external {
        require(messageStatus[messageId] == MessageStatus.Failed, "Not failed");
        
        FailedMessage memory fm = failedMessages[messageId];
        delete failedMessages[messageId];
        
        messageStatus[messageId] = MessageStatus.Pending;
        
        // Retry processing
        this._processMessage(fm.message);
        messageStatus[messageId] = MessageStatus.Completed;
    }
}
```

---

## 3. Router Configuration Issues

### Overview

Hyperlane Routers must be properly enrolled on each chain. Missing or incorrect router enrollment allows attackers to send messages from unauthorized sources.

### Vulnerable Pattern Examples

**Example 1: Missing Router Enrollment Check** [HIGH]
```solidity
// ❌ VULNERABLE: Any sender accepted
contract NoRouterCheck is IMessageRecipient {
    function handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) external override {
        // No check that sender is enrolled router!
        // Anyone on origin chain can send messages
        
        _processMessage(_message);
    }
}
```

**Example 2: Incorrect Router Address Format** [MEDIUM]
```solidity
// ❌ VULNERABLE: Wrong address format comparison
contract WrongAddressFormat is Router {
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override {
        // bytes32 sender compared to address directly
        // address(uint160(uint256(_sender))) conversion needed!
        require(_sender == bytes32(uint256(uint160(expectedSender))), "Wrong sender");
        // Above is wrong if expectedSender stored differently
        
        _processMessage(_message);
    }
}
```

### Secure Implementation

**Fix: Proper Router Enrollment**
```solidity
// ✅ SECURE: Proper router enrollment and validation
contract SecureRouter is Router {
    using TypeCasts for address;
    using TypeCasts for bytes32;
    
    constructor(address _mailbox) Router(_mailbox) {}
    
    function enrollRemoteRouters(
        uint32[] calldata _domains,
        bytes32[] calldata _routers
    ) external onlyOwner {
        require(_domains.length == _routers.length, "Length mismatch");
        
        for (uint256 i = 0; i < _domains.length; i++) {
            require(_routers[i] != bytes32(0), "Zero router");
            _enrollRemoteRouter(_domains[i], _routers[i]);
        }
    }
    
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override {
        // Router base class validates _sender against enrolled routers
        // Additional validation here if needed
        
        _processMessage(_origin, _sender, _message);
    }
}
```

---

## 4. Handle Function Vulnerabilities

### Overview

The `handle()` function is the entry point for cross-chain messages. Vulnerabilities in this function can lead to reentrancy, access control bypass, or state corruption.

### Vulnerable Pattern Examples

**Example 1: Reentrancy in Handle** [HIGH]
```solidity
// ❌ VULNERABLE: State change after external call
contract ReentrancyVulnerable is Router {
    mapping(address => uint256) public balances;
    
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override {
        (address recipient, uint256 amount) = abi.decode(_message, (address, uint256));
        
        // External call before state update
        (bool success,) = recipient.call{value: amount}("");
        require(success);
        
        // Attacker can reenter and drain funds
        balances[recipient] -= amount;  // Wrong order!
    }
}
```

**Example 2: Missing Access Control** [HIGH]
```solidity
// ❌ VULNERABLE: handle can be called by anyone
contract MissingAccessControl is IMessageRecipient {
    function handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) external override {
        // Missing: require(msg.sender == mailbox)
        // Anyone can call this directly!
        
        _mintTokens(_message);
    }
}
```

### Secure Implementation

**Fix: Secure Handle Implementation**
```solidity
// ✅ SECURE: Proper access control and reentrancy protection
contract SecureHandle is Router, ReentrancyGuard {
    using TypeCasts for bytes32;
    
    constructor(address _mailbox) Router(_mailbox) {}
    
    function _handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _message
    ) internal override nonReentrant {
        // Router ensures msg.sender == mailbox
        // Router ensures _sender is enrolled router
        
        (address recipient, uint256 amount) = abi.decode(_message, (address, uint256));
        
        // State changes first (CEI pattern)
        balances[recipient] += amount;
        
        // External call last
        _notifyRecipient(recipient, amount);
    }
}
```

---

## 5. Gas Payment Issues

### Overview

Hyperlane requires gas payment for cross-chain message delivery. Incorrect gas estimation or payment handling can lead to stuck messages or fund loss.

### Vulnerable Pattern Examples

**Example 1: Hardcoded Gas Amount** [MEDIUM]
```solidity
// ❌ VULNERABLE: Hardcoded gas may be insufficient
contract HardcodedGas is Router {
    uint256 constant GAS_AMOUNT = 200000;  // May not be enough!
    
    function sendMessage(uint32 _destination, bytes calldata _message) external payable {
        bytes32 messageId = _dispatch(_destination, _message);
        
        // Hardcoded gas - doesn't account for message complexity
        igp.payForGas{value: msg.value}(
            messageId,
            _destination,
            GAS_AMOUNT,  // Insufficient for complex operations!
            msg.sender
        );
    }
}
```

### Secure Implementation

**Fix: Dynamic Gas Estimation**
```solidity
// ✅ SECURE: Dynamic gas based on message
contract SecureGasPayment is Router {
    IInterchainGasPaymaster public igp;
    
    function sendMessage(
        uint32 _destination,
        bytes calldata _message
    ) external payable {
        // Estimate gas based on message size and operation
        uint256 gasAmount = _estimateGas(_destination, _message);
        
        // Get quote
        uint256 gasPayment = igp.quoteGasPayment(_destination, gasAmount);
        require(msg.value >= gasPayment, "Insufficient gas payment");
        
        bytes32 messageId = _dispatch(_destination, _message);
        
        igp.payForGas{value: gasPayment}(
            messageId,
            _destination,
            gasAmount,
            msg.sender
        );
        
        // Refund excess
        if (msg.value > gasPayment) {
            payable(msg.sender).transfer(msg.value - gasPayment);
        }
    }
    
    function _estimateGas(
        uint32 _destination,
        bytes calldata _message
    ) internal view returns (uint256) {
        uint256 baseGas = 100000;
        uint256 perByteGas = 16;
        return baseGas + (_message.length * perByteGas);
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: Missing interchainSecurityModule configuration
- Pattern 2: handle() without msg.sender == mailbox check
- Pattern 3: No replay protection (missing message ID tracking)
- Pattern 4: State changes before marking message as processed
- Pattern 5: Missing router enrollment validation
- Pattern 6: Hardcoded gas amounts
- Pattern 7: External calls before state updates in handle()
- Pattern 8: Permissive ISM (always returns true)
```

### Audit Checklist
- [ ] Verify ISM is properly configured (not null, not permissive)
- [ ] Check handle() access control (only Mailbox can call)
- [ ] Verify message ID tracking prevents replay
- [ ] Ensure state changes happen after replay check
- [ ] Validate router enrollment on all chains
- [ ] Check gas estimation is dynamic and sufficient
- [ ] Test reentrancy protection in handle()
- [ ] Verify sender address format conversions

---

## Keywords for Search

`hyperlane`, `mailbox`, `dispatch`, `process`, `handle`, `ISM`, `interchainSecurityModule`, `Router`, `enrollRemoteRouter`, `TokenRouter`, `WarpRoute`, `message_replay`, `unlimited_minting`, `cross_chain`, `bridge`, `interchain`, `quoteGasPayment`, `payForGas`

---

## Related Vulnerabilities

- [LayerZero Integration Issues](../layerzero/layerzero-integration-vulnerabilities.md)
- [Wormhole Integration Issues](../wormhole/wormhole-integration-vulnerabilities.md)
- [Cross-Chain Replay Attacks](../custom/cross-chain-replay-vulnerabilities.md)
