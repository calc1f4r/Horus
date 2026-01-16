---
# Core Classification (Required)
protocol: generic
chain: everychain
category: cross_chain
vulnerability_type: chainlink_ccip_integration

# Attack Vector Details (Required)
attack_type: message_manipulation|dos|fund_loss
affected_component: ccip_router|message_handling|token_transfer

# Oracle-Specific Fields
oracle_provider: chainlink
oracle_attack_vector: message_decode|router_config|gas_limit|source_validation

# Technical Primitives (Required)
primitives:
  - CCIP
  - ccipReceive
  - ccipSend
  - Client.EVM2AnyMessage
  - extraArgs
  - EVMExtraArgsV2
  - gasLimit
  - allowOutOfOrderExecution
  - router
  - chainSelector
  - sourceChain
  - sender

# Impact Classification (Required)
severity: high|medium|low
impact: fund_loss|dos|message_failure
exploitability: 0.70
financial_impact: high

# Context Tags
tags:
  - defi
  - cross_chain
  - bridge
  - messaging
  - token_transfer

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Message Decoding Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| All CCIP messages revert | `reports/chainlink_findings/all-ccip-messages-reverts-when-decoded.md` | HIGH | Cyfrin |

### Router Configuration Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Router cannot be updated | `reports/chainlink_findings/ccip-router-address-cannot-be-updated.md` | MEDIUM | Multiple |

### Extra Args Configuration
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Hardcoded extraArgs | `reports/chainlink_findings/hardcoded-extraargs-violates-ccip-best-practices.md` | LOW | Cyfrin |

### Source Validation Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing source validation | `reports/chainlink_findings/missing-source-validation-in-ccip-message-handling.md` | MEDIUM | Multiple |

### Exception Handling
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Unhandled exceptions | `reports/chainlink_findings/unhandled-exceptions-in-ccip-message-processing-can-lead-to-cross-chain-communic.md` | MEDIUM | Multiple |

### External Links
- [Chainlink CCIP Documentation](https://docs.chain.link/ccip)
- [CCIP Best Practices](https://docs.chain.link/ccip/best-practices)
- [CCIP Architecture](https://docs.chain.link/ccip/architecture)

---

# Chainlink CCIP Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Chainlink CCIP Security Audits**

---

## Table of Contents

1. [Message Decoding Vulnerabilities](#1-message-decoding-vulnerabilities)
2. [Router Configuration Issues](#2-router-configuration-issues)
3. [Extra Args Configuration](#3-extra-args-configuration)
4. [Source/Sender Validation](#4-sourcesender-validation)
5. [Callback/Receive Handling](#5-callbackreceive-handling)
6. [Gas Limit Configuration](#6-gas-limit-configuration)

---

## 1. Message Decoding Vulnerabilities

### Overview

CCIP messages carry encoded payloads that must be decoded correctly. Mismatches between encoding and decoding (especially with data types) cause all messages to fail.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/all-ccip-messages-reverts-when-decoded.md`

### Vulnerability Description

#### Root Cause

Chainlink CCIP uses `uint64` for chain selectors, but protocols often use smaller types like `uint32`. Type mismatches during ABI encoding/decoding cause silent failures or reverts.

#### Attack Scenario

1. Protocol encodes CCIP message with wrong type size
2. Message is sent cross-chain successfully
3. Receiving contract attempts to decode
4. ABI decode fails due to type mismatch (uint64 vs uint32)
5. All CCIP messages for this protocol fail permanently

### Vulnerable Pattern Examples

**Example 1: Wrong Chain ID Type** [HIGH]
> 📖 Reference: `reports/chainlink_findings/all-ccip-messages-reverts-when-decoded.md`
```solidity
// ❌ VULNERABLE: uint32 cannot hold Chainlink chain selectors
struct BridgePayload {
    uint32 dstId;     // WRONG: Chainlink uses uint64!
    address to;
    address token;
    uint256 amount;
}

function decodeBridgeSendPayload(bytes memory _data) external pure returns (...) {
    // Reverts! Chainlink's chain ID like 5009297550715157269 > uint32.max
    (uint32 dstId, address to, address token, uint256 amount) = 
        abi.decode(_data, (uint32, address, address, uint256));
}
```

**Example 2: Inconsistent Encoding/Decoding** [HIGH]
```solidity
// ❌ VULNERABLE: Encode and decode don't match
// Sender contract
function sendMessage(uint64 destChain) external {
    bytes memory payload = abi.encode(destChain, msg.sender);
    // Encoded as uint64
}

// Receiver contract
function receiveMessage(bytes memory payload) external {
    // Decodes as uint256 - works but wastes gas
    // Or decodes as uint32 - REVERTS!
    (uint32 destChain, address sender) = abi.decode(payload, (uint32, address));
}
```

### Impact Analysis

#### Technical Impact
- All CCIP messages fail to decode
- Cross-chain functionality completely broken
- Tokens may be burned/locked with no recovery

#### Business Impact
- Complete bridge failure
- Permanent fund loss (non-upgradeable contracts)
- User tokens stuck in transit

### Secure Implementation

**Fix 1: Use Correct Types (uint64)**
```solidity
// ✅ SECURE: Use uint64 for chain selectors
struct BridgePayload {
    uint64 dstId;     // Correct type for Chainlink chain selector
    address to;
    address token;
    uint256 amount;
}

function decodeBridgeSendPayload(bytes memory _data) external pure returns (
    uint64 dstId,
    address to,
    address token,
    uint256 amount
) {
    (dstId, to, token, amount) = abi.decode(_data, (uint64, address, address, uint256));
}
```

**Fix 2: Use Chainlink's Types Directly**
```solidity
// ✅ SECURE: Import and use Chainlink's exact types
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";

// Use Client.Any2EVMMessage directly
function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
    uint64 sourceChainSelector = message.sourceChainSelector; // Correct type
    // ...
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- uint32 for chain IDs/selectors in CCIP context
- Mismatched types between encode and decode
- Custom structs with non-uint64 chain identifiers
- Type casting of chain selectors
```

#### Audit Checklist
- [ ] Verify all chain selectors use uint64
- [ ] Check encoding/decoding types match exactly
- [ ] Review payload struct definitions
- [ ] Test with actual Chainlink chain selector values

---

## 2. Router Configuration Issues

### Overview

CCIP router addresses can change. Hardcoding or making them immutable prevents protocol from adapting to Chainlink router upgrades.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/ccip-router-address-cannot-be-updated.md`

### Vulnerability Description

#### Root Cause

Router address stored as immutable or constant without update mechanism. When Chainlink upgrades router, protocol becomes incompatible.

### Vulnerable Pattern Examples

**Example 1: Immutable Router** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/ccip-router-address-cannot-be-updated.md`
```solidity
// ❌ VULNERABLE: Cannot update if Chainlink changes router
address public immutable ccipRouter;

constructor(address _router) {
    ccipRouter = _router;
}
```

**Example 2: Constant Router** [MEDIUM]
```solidity
// ❌ VULNERABLE: Hardcoded address
address constant CCIP_ROUTER = 0x1234...;
```

### Secure Implementation

**Fix 1: Updatable Router with Access Control**
```solidity
// ✅ SECURE: Router can be updated by admin
address public ccipRouter;

function updateRouter(address newRouter) external onlyOwner {
    require(newRouter != address(0), "Invalid router");
    emit RouterUpdated(ccipRouter, newRouter);
    ccipRouter = newRouter;
}
```

**Fix 2: Override getRouter Pattern**
```solidity
// ✅ SECURE: Following Chainlink's recommended pattern
contract MyCCIPReceiver is CCIPReceiver {
    address private s_router;
    
    constructor(address router) CCIPReceiver(router) {
        s_router = router;
    }
    
    function getRouter() public view override returns (address) {
        return s_router;
    }
    
    function updateRouter(address newRouter) external onlyOwner {
        s_router = newRouter;
    }
}
```

---

## 3. Extra Args Configuration

### Overview

CCIP `extraArgs` configure execution parameters like gas limits. Hardcoding these prevents adaptation to future CCIP changes.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/hardcoded-extraargs-violates-ccip-best-practices.md`

### Vulnerability Description

#### Root Cause

`extraArgs` hardcoded in code rather than passed as parameters or stored in upgradeable storage. Future CCIP versions may require different formats.

### Vulnerable Pattern Examples

**Example 1: Hardcoded extraArgs** [LOW]
> 📖 Reference: `reports/chainlink_findings/hardcoded-extraargs-violates-ccip-best-practices.md`
```solidity
// ❌ VULNERABLE: Hardcoded, cannot adapt to changes
function sendMessage(address receiver, bytes memory data) external {
    Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
        receiver: abi.encode(receiver),
        data: data,
        tokenAmounts: new Client.EVMTokenAmount[](0),
        // Hardcoded!
        extraArgs: Client._argsToBytes(
            Client.EVMExtraArgsV2({
                gasLimit: 200_000,
                allowOutOfOrderExecution: true
            })
        ),
        feeToken: address(0)
    });
}
```

### Secure Implementation

**Fix 1: Configurable extraArgs**
```solidity
// ✅ SECURE: extraArgs is configurable
bytes public defaultExtraArgs;

function setDefaultExtraArgs(bytes calldata _extraArgs) external onlyOwner {
    defaultExtraArgs = _extraArgs;
}

function sendMessage(
    address receiver, 
    bytes memory data,
    bytes calldata extraArgs // Or use defaultExtraArgs
) external {
    Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
        receiver: abi.encode(receiver),
        data: data,
        tokenAmounts: new Client.EVMTokenAmount[](0),
        extraArgs: extraArgs.length > 0 ? extraArgs : defaultExtraArgs,
        feeToken: address(0)
    });
}
```

---

## 4. Source/Sender Validation

### Overview

CCIP receivers must validate the source chain and sender to prevent unauthorized cross-chain messages from being processed.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/missing-source-validation-in-ccip-message-handling.md`

### Vulnerability Description

#### Root Cause

`_ccipReceive` processes messages without validating the source chain selector or sender address, allowing malicious actors to send fake cross-chain messages.

### Vulnerable Pattern Examples

**Example 1: No Source Validation** [HIGH]
> 📖 Reference: `reports/chainlink_findings/missing-source-validation-in-ccip-message-handling.md`
```solidity
// ❌ VULNERABLE: Accepts messages from any source
function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
    // No validation of sourceChainSelector or sender!
    (address recipient, uint256 amount) = abi.decode(message.data, (address, uint256));
    _mint(recipient, amount);
}
```

**Example 2: Missing Sender Whitelist** [MEDIUM]
```solidity
// ❌ VULNERABLE: Only validates chain, not sender
function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
    require(
        message.sourceChainSelector == EXPECTED_CHAIN,
        "Wrong source chain"
    );
    // Missing: sender validation!
    processMessage(message.data);
}
```

### Secure Implementation

**Fix 1: Full Source Validation**
```solidity
// ✅ SECURE: Validate both chain and sender
mapping(uint64 => address) public allowedSenders;

function setAllowedSender(uint64 chainSelector, address sender) external onlyOwner {
    allowedSenders[chainSelector] = sender;
}

function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
    // Validate source chain
    address expectedSender = allowedSenders[message.sourceChainSelector];
    require(expectedSender != address(0), "Chain not allowed");
    
    // Validate sender
    address actualSender = abi.decode(message.sender, (address));
    require(actualSender == expectedSender, "Sender not allowed");
    
    // Now safe to process
    processMessage(message.data);
}
```

---

## 5. Callback/Receive Handling

### Overview

`_ccipReceive` must handle messages gracefully. Reverts can cause message failures that may be difficult to recover from.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/unhandled-exceptions-in-ccip-message-processing-can-lead-to-cross-chain-communic.md`
> - `reports/chainlink_findings/consider-to-avoid-reverting-inside-governanceccipreceiver_ccipreceive.md`

### Vulnerability Description

#### Root Cause

Complex logic, external calls, or state validations in `_ccipReceive` that can fail, causing permanent message loss.

### Vulnerable Pattern Examples

**Example 1: External Calls Without Try/Catch** [MEDIUM]
```solidity
// ❌ VULNERABLE: External call can fail
function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
    (address token, address to, uint256 amount) = 
        abi.decode(message.data, (address, address, uint256));
    
    // Can revert if token transfer fails!
    IERC20(token).transfer(to, amount);
}
```

**Example 2: Strict State Requirements** [MEDIUM]
```solidity
// ❌ VULNERABLE: State validation can fail
function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
    uint256 orderId = abi.decode(message.data, (uint256));
    
    // Can revert if order already processed or cancelled
    require(orders[orderId].status == OrderStatus.PENDING, "Invalid order");
    
    processOrder(orderId);
}
```

### Secure Implementation

**Fix 1: Store and Process Pattern**
```solidity
// ✅ SECURE: Store for later processing
mapping(bytes32 => Client.Any2EVMMessage) public pendingMessages;
mapping(bytes32 => bool) public messageProcessed;

function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
    bytes32 messageId = message.messageId;
    
    // Just store - cannot fail
    pendingMessages[messageId] = message;
    emit MessageReceived(messageId);
}

function processMessage(bytes32 messageId) external {
    require(!messageProcessed[messageId], "Already processed");
    Client.Any2EVMMessage memory message = pendingMessages[messageId];
    
    // Process with full error handling
    try this._processMessageInternal(message) {
        messageProcessed[messageId] = true;
    } catch {
        emit ProcessingFailed(messageId);
    }
}
```

**Fix 2: Graceful Failure Handling**
```solidity
// ✅ SECURE: Handle failures gracefully
function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
    try this._processMessage(message) {
        emit MessageProcessed(message.messageId);
    } catch Error(string memory reason) {
        emit MessageFailed(message.messageId, reason);
        // Store for manual recovery
        failedMessages[message.messageId] = message;
    }
}
```

---

## 6. Gas Limit Configuration

### Overview

Insufficient gas limits cause CCIP message execution to fail. Over-estimation wastes fees.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/relaymessage-should-use-a-custom-gaslimit-value-in-the-extraargs-to-avoid-oog-re.md`

### Vulnerable Pattern Examples

**Example 1: Default Gas Limit** [MEDIUM]
```solidity
// ❌ VULNERABLE: Default might not be enough
function sendMessage(address receiver, bytes memory data) external {
    Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
        receiver: abi.encode(receiver),
        data: data,
        tokenAmounts: new Client.EVMTokenAmount[](0),
        extraArgs: "", // Uses default - might be insufficient
        feeToken: address(0)
    });
}
```

### Secure Implementation

**Fix 1: Calculated Gas Limits**
```solidity
// ✅ SECURE: Appropriate gas limit for operation
function sendMessage(address receiver, bytes memory data) external {
    // Calculate required gas based on operation
    uint256 gasLimit = 200_000 + (data.length * 100); // Base + per-byte
    
    Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
        receiver: abi.encode(receiver),
        data: data,
        tokenAmounts: new Client.EVMTokenAmount[](0),
        extraArgs: Client._argsToBytes(
            Client.EVMExtraArgsV2({
                gasLimit: gasLimit,
                allowOutOfOrderExecution: false
            })
        ),
        feeToken: address(0)
    });
}
```

---

## Prevention Guidelines

### Development Best Practices

1. **Use correct types** - uint64 for chain selectors
2. **Updatable router** - Allow router address updates
3. **Configurable extraArgs** - Don't hardcode execution parameters
4. **Full source validation** - Check both chain and sender
5. **Graceful receive** - _ccipReceive should never revert
6. **Appropriate gas** - Calculate gas limits properly

### Testing Requirements

- Test with actual Chainlink chain selector values
- Simulate router upgrade scenarios
- Test message failure recovery
- Verify source validation across chains

---

## Keywords for Search

`chainlink ccip`, `ccip`, `cross chain`, `ccipReceive`, `ccipSend`, `EVM2AnyMessage`, `extraArgs`, `EVMExtraArgsV2`, `gasLimit`, `router`, `chainSelector`, `sourceChainSelector`, `sender validation`, `source validation`, `bridge`, `message decode`, `chain id`, `uint64`, `token transfer`, `cross chain message`

---

## Related Vulnerabilities

- [Chainlink Price Feed Vulnerabilities](./CHAINLINK_PRICE_FEED_VULNERABILITIES.md)
- [Chainlink VRF Vulnerabilities](./CHAINLINK_VRF_VULNERABILITIES.md)
- [Chainlink Automation Vulnerabilities](./CHAINLINK_AUTOMATION_VULNERABILITIES.md)
