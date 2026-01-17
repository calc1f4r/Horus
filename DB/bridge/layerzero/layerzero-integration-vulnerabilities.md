---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bridge
vulnerability_type: layerzero_integration

# Attack Vector Details (Required)
attack_type: channel_blocking|gas_griefing|message_replay|fund_loss
affected_component: lzReceive|_lzSend|NonblockingLzApp|OFT|ONFT

# Bridge-Specific Fields
bridge_provider: layerzero
bridge_attack_vector: channel_blocking | minimum_gas | gas_estimation | fee_refund | payload_size | composed_message

# Technical Primitives (Required)
primitives:
  - lzReceive
  - _lzSend
  - NonblockingLzApp
  - LzApp
  - adapterParams
  - gasLimit
  - endpoint
  - trustedRemote
  - StoredPayload
  - OFT
  - ONFT
  - compose
  - lzCompose

# Impact Classification (Required)
severity: high|medium|low
impact: channel_dos|fund_loss|gas_griefing|message_stuck
exploitability: 0.80
financial_impact: high

# Context Tags
tags:
  - defi
  - bridge
  - cross_chain
  - omnichain
  - layerzero
  - stargate
  - oft
  - onft

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Channel Blocking Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Velodrome - Channel Blocked | `reports/bridge_crosschain_findings/h-06-attacker-can-block-layerzero-channel.md` | HIGH | Code4rena |
| Tapioca - Variable Gas Blocking | `reports/bridge_crosschain_findings/h-16-attacker-can-block-layerzero-channel-due-to-variable-gas-cost-of-saving-pay.md` | HIGH | Code4rena |
| Tapioca - Missing Min Gas | `reports/bridge_crosschain_findings/h-17-attacker-can-block-layerzero-channel-due-to-missing-check-of-minimum-gas-pa.md` | HIGH | Code4rena |
| Decent - Min Gas Missing | `reports/bridge_crosschain_findings/h-02-due-to-missing-checks-on-minimum-gas-passed-through-layerzero-executions-ca.md` | HIGH | Code4rena |

### Gas Estimation & Fee Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Holograph - Gas Miscalculation | `reports/bridge_crosschain_findings/h-03-layerzeromodule-miscalculates-gas-risking-loss-of-assets.md` | HIGH | Code4rena |
| Mozaic - Gas Underestimation | `reports/bridge_crosschain_findings/trst-m-10-mozbridge-underestimates-gas-for-sending-of-moz-messages.md` | MEDIUM | Trust Security |
| TapiocaDAO - Missing quoteLayerZeroFee | `reports/bridge_crosschain_findings/m-08-missing-implementation-of-the-quotelayerzerofee-in-stargatelbphelpersol.md` | MEDIUM | Pashov |
| Mozaic - No Native Tokens | `reports/bridge_crosschain_findings/trst-h-3-all-layerzero-requests-will-fail-making-the-contracts-are-unfunctional.md` | HIGH | Trust Security |

### Fee Refund Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Nexus - No Receive Function | `reports/bridge_crosschain_findings/m-01-layerzero-fee-refunds-cannot-be-processed.md` | MEDIUM | Pashov |
| LayerZeroZROClaim - lzReceive Reverts | `reports/bridge_crosschain_findings/h-02-_lzreceive-reverts-when-there-is-a-fee-refund.md` | HIGH | Pashov |
| Nexus - Refund Misdirected | `reports/bridge_crosschain_findings/m-04-layerzero-fee-refunds-misdirected-to-deposit-contracts.md` | MEDIUM | Pashov |

### Payload Size & Address Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| UXD - Large toAddress | `reports/bridge_crosschain_findings/h-2-malicious-user-can-use-an-excessively-large-_toaddress-in-oftcoresendfrom-to.md` | HIGH | Sherlock |

### External Links
- [LayerZero Documentation](https://layerzero.gitbook.io/docs/)
- [LayerZero Integration Checklist](https://layerzero.gitbook.io/docs/troubleshooting/layerzero-integration-checklist)
- [NonblockingLzApp Example](https://github.com/LayerZero-Labs/solidity-examples/blob/main/contracts/lzApp/NonblockingLzApp.sol)

---

# LayerZero Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for LayerZero Cross-Chain Security Audits**

---

## Table of Contents

1. [Channel Blocking Vulnerabilities](#1-channel-blocking-vulnerabilities)
2. [Minimum Gas Validation Vulnerabilities](#2-minimum-gas-validation-vulnerabilities)
3. [Gas Estimation & Fee Calculation](#3-gas-estimation--fee-calculation)
4. [Fee Refund Handling](#4-fee-refund-handling)
5. [Payload Size & Address Validation](#5-payload-size--address-validation)
6. [Composed Message Vulnerabilities](#6-composed-message-vulnerabilities)
7. [OFT/ONFT Specific Vulnerabilities](#7-oftonft-specific-vulnerabilities)
8. [Trust & Access Control](#8-trust--access-control)

---

## 1. Channel Blocking Vulnerabilities

### Overview

LayerZero's default behavior is **blocking** - when a message fails on the destination chain, the channel between source and destination is blocked until the failed message is successfully retried. This can be exploited by attackers to permanently DoS cross-chain communication.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-06-attacker-can-block-layerzero-channel.md` (Velodrome - Code4rena)
> - `reports/bridge_crosschain_findings/h-16-attacker-can-block-layerzero-channel-due-to-variable-gas-cost-of-saving-pay.md` (Tapioca - Code4rena)
> - `reports/bridge_crosschain_findings/h-17-attacker-can-block-layerzero-channel-due-to-missing-check-of-minimum-gas-pa.md` (Tapioca - Code4rena)

### Vulnerability Description

#### Root Cause

Protocols inherit from `LzApp` without implementing the non-blocking pattern (`NonblockingLzApp`), or they implement it incorrectly. When `lzReceive()` reverts, the message is stored in `storedPayload` and blocks all subsequent messages.

#### Attack Scenario

1. Attacker identifies a cross-chain contract without non-blocking implementation
2. Attacker sends a message designed to revert on destination (insufficient gas, malicious payload)
3. Message fails and is stored in `storedPayload`
4. All subsequent messages from that source chain are blocked
5. Protocol becomes permanently DoS'd unless `forceResumeReceive` is implemented

### Vulnerable Pattern Examples

**Example 1: Missing Non-Blocking Pattern** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-06-attacker-can-block-layerzero-channel.md`
```solidity
// ❌ VULNERABLE: Inherits LzApp directly without non-blocking wrapper
contract RedemptionReceiver is LzApp {
    function lzReceive(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) external override {
        // Any revert here will block the channel
        _processPayload(_payload);  // If this reverts, channel is blocked
    }
}
```

**Example 2: Gas Draining to Force Blocking** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-16-attacker-can-block-layerzero-channel-due-to-variable-gas-cost-of-saving-pay.md`
```solidity
// ❌ VULNERABLE: External calls before NonblockingLzApp catch
contract BaseTOFT is NonblockingLzApp {
    function _nonblockingLzReceive(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) internal override {
        // Attacker can pass malicious contract that drains gas
        ISendFrom(rewardToken).sendFrom(...);  // Gas drained here
        
        // Never reaches the non-blocking catch block
        // because gas exhausted in external call
    }
}
```

**Example 3: Missing forceResumeReceive** [HIGH]
```solidity
// ❌ VULNERABLE: No recovery mechanism
contract BridgeReceiver is LzApp {
    // Missing forceResumeReceive implementation
    // If channel gets blocked, no way to unblock it
    
    function lzReceive(...) external override {
        require(msg.sender == address(lzEndpoint), "Invalid endpoint");
        _processMessage(_payload);
    }
}
```

### Impact Analysis

#### Technical Impact
- **Channel DoS**: All messages from affected source chain are blocked
- **Permanent Blocking**: Without `forceResumeReceive`, channel may be permanently blocked
- **State Corruption**: Pending messages cannot be processed

#### Business Impact
- **Protocol Unusable**: Cross-chain functionality completely disabled
- **User Funds Locked**: Tokens in transit may be stuck
- **Trust Loss**: Users lose confidence in protocol's reliability

#### Affected Scenarios
- Protocols without `NonblockingLzApp` implementation
- External calls before non-blocking try-catch
- Missing `forceResumeReceive` implementation
- No gas limit validation on user-supplied parameters

### Secure Implementation

**Fix 1: Use NonblockingLzApp Correctly**
```solidity
// ✅ SECURE: Proper NonblockingLzApp implementation
contract SecureBridgeReceiver is NonblockingLzApp {
    mapping(uint16 => mapping(bytes => mapping(uint64 => bytes32))) public failedMessages;
    
    function _nonblockingLzReceive(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) internal override {
        // Wrap in try-catch for additional safety
        try this.processPayload(_srcChainId, _payload) {
            // Success
        } catch {
            // Store failed message for retry
            failedMessages[_srcChainId][_srcAddress][_nonce] = keccak256(_payload);
            emit MessageFailed(_srcChainId, _srcAddress, _nonce, _payload);
        }
    }
    
    function retryMessage(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) external {
        bytes32 payloadHash = failedMessages[_srcChainId][_srcAddress][_nonce];
        require(payloadHash != bytes32(0), "No stored message");
        require(keccak256(_payload) == payloadHash, "Invalid payload");
        
        delete failedMessages[_srcChainId][_srcAddress][_nonce];
        this.processPayload(_srcChainId, _payload);
    }
}
```

**Fix 2: Implement forceResumeReceive**
```solidity
// ✅ SECURE: Emergency recovery mechanism
contract SecureLzApp is LzApp {
    function forceResumeReceive(uint16 _srcChainId, bytes calldata _srcAddress) external onlyOwner {
        lzEndpoint.forceResumeReceive(_srcChainId, _srcAddress);
    }
}
```

---

## 2. Minimum Gas Validation Vulnerabilities

### Overview

LayerZero allows senders to specify gas through `adapterParams`. If protocols don't enforce minimum gas requirements, attackers can send messages with insufficient gas that revert on destination, blocking the channel.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-17-attacker-can-block-layerzero-channel-due-to-missing-check-of-minimum-gas-pa.md` (Tapioca - Code4rena)
> - `reports/bridge_crosschain_findings/h-02-due-to-missing-checks-on-minimum-gas-passed-through-layerzero-executions-ca.md` (Decent - Code4rena)

### Vulnerability Description

#### Root Cause

Protocols allow users to specify arbitrary `adapterParams` without validating the gas limit meets minimum requirements for the destination chain operation.

#### Attack Scenario

1. Attacker calls a cross-chain function with minimal gas in `adapterParams`
2. LayerZero relayer delivers message with specified gas
3. Transaction reverts due to out-of-gas before reaching `NonblockingLzApp` catch
4. Message is stored in `storedPayload`, blocking channel

### Vulnerable Pattern Examples

**Example 1: No AdapterParams Validation** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-17-attacker-can-block-layerzero-channel-due-to-missing-check-of-minimum-gas-pa.md`
```solidity
// ❌ VULNERABLE: User controls gas amount without validation
function triggerSendFrom(
    address _from,
    uint16 _dstChainId,
    bytes calldata _toAddress,
    uint _amount,
    bytes calldata _adapterParams  // User can pass minimal gas
) external payable {
    _lzSend(
        _dstChainId,
        abi.encode(_from, _toAddress, _amount),
        payable(msg.sender),
        address(0),
        _adapterParams,  // No validation!
        msg.value
    );
}
```

**Example 2: Hardcoded Insufficient Gas** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-02-due-to-missing-checks-on-minimum-gas-passed-through-layerzero-executions-ca.md`
```solidity
// ❌ VULNERABLE: Hardcoded gas too low for some operations
contract DecentEthRouter {
    uint256 GAS_FOR_RELAY = 100000;  // May be insufficient
    
    function bridge(..., uint64 _dstGasForCall, ...) public payable {
        uint256 gasAmount = GAS_FOR_RELAY + _dstGasForCall;  // User controls _dstGasForCall
        // No minimum validation on _dstGasForCall
    }
}
```

### Secure Implementation

**Fix 1: Enforce Minimum Gas**
```solidity
// ✅ SECURE: Validate minimum gas per message type
contract SecureLzSender is LzApp {
    mapping(uint16 => uint256) public minDstGasLookup;
    
    function setMinDstGas(uint16 _dstChainId, uint256 _minGas) external onlyOwner {
        minDstGasLookup[_dstChainId] = _minGas;
    }
    
    function _lzSend(
        uint16 _dstChainId,
        bytes memory _payload,
        address payable _refundAddress,
        address _zroPaymentAddress,
        bytes memory _adapterParams,
        uint _nativeFee
    ) internal virtual override {
        uint256 gasLimit = _getGasLimit(_adapterParams);
        require(gasLimit >= minDstGasLookup[_dstChainId], "Gas too low");
        
        super._lzSend(_dstChainId, _payload, _refundAddress, _zroPaymentAddress, _adapterParams, _nativeFee);
    }
    
    function _getGasLimit(bytes memory _adapterParams) internal pure returns (uint256 gasLimit) {
        require(_adapterParams.length >= 34, "Invalid adapterParams");
        assembly {
            gasLimit := mload(add(_adapterParams, 34))
        }
    }
}
```

**Fix 2: Use LayerZero's setMinDstGas**
```solidity
// ✅ SECURE: Use built-in minimum gas configuration
contract SecureOFT is OFT {
    constructor(...) OFT(...) {
        // Set minimum gas for each packet type per chain
        setMinDstGas(ARBITRUM_CHAIN_ID, PT_SEND, 200000);
        setMinDstGas(ARBITRUM_CHAIN_ID, PT_SEND_AND_CALL, 500000);
        setMinDstGas(OPTIMISM_CHAIN_ID, PT_SEND, 200000);
    }
}
```

---

## 3. Gas Estimation & Fee Calculation

### Overview

Incorrect gas estimation for cross-chain messages leads to either overpaying (wasted funds) or underpaying (failed execution, potential fund loss).

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-03-layerzeromodule-miscalculates-gas-risking-loss-of-assets.md` (Holograph - Code4rena)
> - `reports/bridge_crosschain_findings/trst-m-10-mozbridge-underestimates-gas-for-sending-of-moz-messages.md` (Mozaic - Trust)
> - `reports/bridge_crosschain_findings/trst-h-3-all-layerzero-requests-will-fail-making-the-contracts-are-unfunctional.md` (Mozaic - Trust)

### Vulnerable Pattern Examples

**Example 1: Using Source Chain Gas Costs for Destination** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-03-layerzeromodule-miscalculates-gas-risking-loss-of-assets.md`
```solidity
// ❌ VULNERABLE: Uses source chain gas config for destination
contract LayerZeroModule {
    uint256 private _baseGas;  // Single value for all chains!
    uint256 private _gasPerByte;
    
    function send(..., bytes calldata crossChainPayload) external payable {
        // Wrong: _baseGas and _gasPerByte are for source chain
        lZEndpoint.send{value: msgValue}(
            dstChainId,
            abi.encodePacked(address(this), address(this)),
            crossChainPayload,
            payable(msgSender),
            address(this),
            abi.encodePacked(
                uint16(1),
                uint256(_baseGas() + (crossChainPayload.length * _gasPerByte()))  // Source chain values!
            )
        );
    }
}
```

**Example 2: Incorrect Payload for Fee Estimation** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/trst-m-10-mozbridge-underestimates-gas-for-sending-of-moz-messages.md`
```solidity
// ❌ VULNERABLE: Fee estimation uses different payload than actual send
function quoteLayerZeroFee(uint16 _chainId, uint16 _msgType, ...) public view returns (uint256, uint256) {
    bytes memory payload = "";
    if (_msgType == TYPE_REPORT_SNAPSHOT) {
        payload = abi.encode(TYPE_REPORT_SNAPSHOT);  // Wrong! Actual includes Snapshot struct
    }
    // Actual payload is longer, causing underestimation
    return layerZeroEndpoint.estimateFees(_chainId, address(this), payload, ...);
}
```

**Example 3: No Native Token Value Sent** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/trst-h-3-all-layerzero-requests-will-fail-making-the-contracts-are-unfunctional.md`
```solidity
// ❌ VULNERABLE: No value passed for LayerZero fees
function requestSnapshot() external {
    bridge.send(...);  // No msg.value! All LZ calls fail
}
```

### Secure Implementation

**Fix 1: Per-Chain Gas Configuration**
```solidity
// ✅ SECURE: Chain-specific gas configuration
contract SecureLayerZeroModule {
    mapping(uint16 => uint256) public dstChainBaseGas;
    mapping(uint16 => uint256) public dstChainGasPerByte;
    
    function setDstChainGasConfig(
        uint16 _dstChainId,
        uint256 _baseGas,
        uint256 _gasPerByte
    ) external onlyOwner {
        dstChainBaseGas[_dstChainId] = _baseGas;
        dstChainGasPerByte[_dstChainId] = _gasPerByte;
    }
    
    function send(uint16 _dstChainId, bytes calldata _payload) external payable {
        uint256 gasAmount = dstChainBaseGas[_dstChainId] + 
            (_payload.length * dstChainGasPerByte[_dstChainId]);
        // Use destination-specific values
    }
}
```

**Fix 2: Accurate Fee Estimation**
```solidity
// ✅ SECURE: Use actual payload for estimation
function quoteLayerZeroFee(
    uint16 _chainId,
    Snapshot memory _snapshot
) public view returns (uint256 nativeFee) {
    bytes memory actualPayload = abi.encode(TYPE_REPORT_SNAPSHOT, _snapshot);
    (nativeFee,) = layerZeroEndpoint.estimateFees(
        _chainId,
        address(this),
        actualPayload,  // Same as actual send
        false,
        _adapterParams
    );
}
```

---

## 4. Fee Refund Handling

### Overview

LayerZero refunds excess fees to the specified refund address. If contracts cannot receive ETH or the refund address is incorrect, funds are lost or transactions revert.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/m-01-layerzero-fee-refunds-cannot-be-processed.md` (Nexus - Pashov)
> - `reports/bridge_crosschain_findings/h-02-_lzreceive-reverts-when-there-is-a-fee-refund.md` (LayerZero ZRO Claim - Pashov)
> - `reports/bridge_crosschain_findings/m-04-layerzero-fee-refunds-misdirected-to-deposit-contracts.md` (Nexus - Pashov)

### Vulnerable Pattern Examples

**Example 1: Missing receive() Function** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-02-_lzreceive-reverts-when-there-is-a-fee-refund.md`
```solidity
// ❌ VULNERABLE: Contract cannot receive refunds
contract ClaimLocal is OApp {
    // Missing receive() or fallback()!
    
    function _lzReceive(...) internal override {
        IOFT(zroToken).send{value: msg.value}(
            sendParams,
            MessagingFee(msg.value, 0),
            address(this)  // Refund to this contract - will revert!
        );
    }
}
```

**Example 2: Refund to Wrong Address** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/m-04-layerzero-fee-refunds-misdirected-to-deposit-contracts.md`
```solidity
// ❌ VULNERABLE: Refunds go to contract, not user
function sendMessage(bytes memory _data, uint32 _destId, uint256 _lzFee) 
    external payable onlyDeposit 
{
    _lzSend(
        _destId,
        _data,
        optionsDestId[_destId],
        MessagingFee(_lzFee, 0),
        payable(msg.sender)  // msg.sender is deposit contract, not user!
    );
}
```

### Secure Implementation

**Fix 1: Add receive() Function**
```solidity
// ✅ SECURE: Contract can receive ETH refunds
contract SecureOApp is OApp {
    receive() external payable {}
    
    function withdrawRefunds() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

**Fix 2: Pass User as Refund Address**
```solidity
// ✅ SECURE: Refund to actual user
function sendMessage(
    bytes memory _data,
    uint32 _destId,
    uint256 _lzFee,
    address refundAddress  // User address passed explicitly
) external payable onlyDeposit {
    _lzSend(
        _destId,
        _data,
        optionsDestId[_destId],
        MessagingFee(_lzFee, 0),
        payable(refundAddress)  // Correct refund address
    );
}
```

---

## 5. Payload Size & Address Validation

### Overview

LayerZero allows arbitrary payload sizes and address lengths. Malicious users can exploit this to create messages that cannot be processed on destination chains with different gas limits.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-2-malicious-user-can-use-an-excessively-large-_toaddress-in-oftcoresendfrom-to.md` (UXD - Sherlock)

### Vulnerable Pattern Examples

**Example 1: Unbounded toAddress Length** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-2-malicious-user-can-use-an-excessively-large-_toaddress-in-oftcoresendfrom-to.md`
```solidity
// ❌ VULNERABLE: No limit on _toAddress length
function sendFrom(
    address _from,
    uint16 _dstChainId,
    bytes calldata _toAddress,  // Can be megabytes!
    uint _amount,
    ...
) public payable virtual override {
    _send(_from, _dstChainId, _toAddress, _amount, ...);
    // Massive _toAddress can cause OOG on destination
}
```

### Secure Implementation

**Fix: Limit Address Length**
```solidity
// ✅ SECURE: Validate address length
function sendFrom(
    address _from,
    uint16 _dstChainId,
    bytes calldata _toAddress,
    uint _amount,
    ...
) public payable virtual override {
    require(_toAddress.length <= 32, "Address too long");  // Max 32 bytes (Solana)
    _send(_from, _dstChainId, _toAddress, _amount, ...);
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: Contracts inheriting LzApp without NonblockingLzApp
- Pattern 2: User-controlled adapterParams without gas validation
- Pattern 3: External calls inside _nonblockingLzReceive before try-catch
- Pattern 4: Missing receive() function in contracts receiving refunds
- Pattern 5: Hardcoded gas values that don't account for chain differences
- Pattern 6: Fee estimation using different payload than actual send
- Pattern 7: msg.sender used as refund address in delegated calls
- Pattern 8: No length validation on bytes parameters
```

### Audit Checklist
- [ ] Check if NonblockingLzApp pattern is correctly implemented
- [ ] Verify minimum gas is enforced for all message types
- [ ] Confirm gas configuration is per-destination-chain
- [ ] Ensure contracts can receive ETH refunds
- [ ] Validate refund addresses are correct (user, not contract)
- [ ] Check payload size limits on user inputs
- [ ] Verify forceResumeReceive is implemented for recovery
- [ ] Test fee estimation matches actual payload

---

## Keywords for Search

`layerzero`, `lzReceive`, `_lzSend`, `NonblockingLzApp`, `LzApp`, `adapterParams`, `StoredPayload`, `forceResumeReceive`, `trustedRemote`, `endpoint`, `channel_blocking`, `gas_griefing`, `OFT`, `ONFT`, `omnichain`, `cross_chain`, `bridge`, `relayer`, `minimum_gas`, `lzCompose`, `composed_message`, `stargate`, `sgReceive`, `fee_refund`

---

## Related Vulnerabilities

- [Stargate Integration Issues](../stargate/stargate-integration-vulnerabilities.md)
- [Cross-Chain Replay Attacks](../custom/cross-chain-replay-vulnerabilities.md)
- [Bridge Access Control](../custom/bridge-access-control.md)
