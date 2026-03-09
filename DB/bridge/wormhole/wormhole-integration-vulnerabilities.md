---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bridge
vulnerability_type: wormhole_integration

# Attack Vector Details (Required)
attack_type: vaa_parsing|guardian_bypass|message_replay|signature_validation
affected_component: VAA|Guardian|Relayer|TokenBridge|NttManager

# Bridge-Specific Fields
bridge_provider: wormhole
bridge_attack_vector: vaa_replay|guardian_set|consistency_level|message_replay|transfer_validation

# Technical Primitives (Required)
primitives:
  - VAA
  - parseAndVerifyVAA
  - verifyVM
  - guardianSet
  - consistencyLevel
  - sequence
  - nonce
  - emitterChainId
  - emitterAddress
  - TokenBridge
  - completeTransfer
  - NttManager
  - TransceiverMessage

# Impact Classification (Required)
severity: high
impact: fund_loss|double_spending|message_replay|governance_bypass
exploitability: 0.70
financial_impact: critical

# Context Tags
tags:
  - defi
  - bridge
  - cross_chain
  - wormhole
  - vaa
  - guardian
  - multichain

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### VAA Parsing & Validation Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Wormhole - Outdated Method | `reports/bridge_crosschain_findings/wormhole-integ.md` | MEDIUM | Sherlock |
| Message Replay | `reports/bridge_crosschain_findings/message-replays-are-possible-across-different-instances.md` | HIGH | Code4rena |

### Guardian & Governance Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Guardian Change Attack | `reports/bridge_crosschain_findings/h-03-an-attacker-can-exploit-the-wormhole-guardian-change-process-to-gain-govern.md` | HIGH | Code4rena |
| Immutable Gas Limit | `reports/bridge_crosschain_findings/h-10-immutable-gaslimit-may-be-insufficient-for-wormhole-relayers-current-impl.md` | HIGH | Code4rena |

### Token Bridge Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Transfer with Payload | `reports/bridge_crosschain_findings/m-20-wormhole-integration-will-not-work-for-bridging-tokens-with-external-calls.md` | MEDIUM | Code4rena |
| Arbitrary Caller | `reports/bridge_crosschain_findings/m-1-wrong-integration-of-wormhole-allows-arbitrary-callers-for-receivewithanycall.md` | MEDIUM | Sherlock |

### External Links
- [Wormhole Documentation](https://docs.wormhole.com/)
- [Wormhole SDK](https://github.com/wormhole-foundation/wormhole)
- [Wormhole Security](https://wormhole.com/security/)

---

# Wormhole Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Wormhole Cross-Chain Security Audits**

---

## Table of Contents

1. [VAA Parsing Vulnerabilities](#1-vaa-parsing-vulnerabilities)
2. [Guardian Set Vulnerabilities](#2-guardian-set-vulnerabilities)
3. [Message Replay Attacks](#3-message-replay-attacks)
4. [Token Bridge Integration](#4-token-bridge-integration)
5. [Gas Limit Issues](#5-gas-limit-issues)
6. [NTT (Native Token Transfers)](#6-ntt-native-token-transfers)

---

## 1. VAA Parsing Vulnerabilities

### Overview

Verified Action Approvals (VAAs) are the core message format in Wormhole. VAAs must be correctly parsed and validated to prevent message forgery, replay attacks, and other exploits. Incorrect VAA handling is a common source of critical vulnerabilities.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/wormhole-integ.md` (Sherlock)
> - `reports/bridge_crosschain_findings/m-1-wrong-integration-of-wormhole-allows-arbitrary-callers-for-receivewithanycall.md` (Sherlock)

### Vulnerability Description

#### Root Cause

Protocols either use outdated/deprecated Wormhole methods for VAA parsing, fail to validate all VAA fields properly, or don't verify the guardian signatures correctly.

#### Attack Scenario

1. Attacker identifies contract using deprecated `parseAndVerifyVAA()` method
2. Attacker crafts malicious VAA that passes weak validation
3. Contract processes fraudulent message
4. Attacker drains funds or corrupts state

### Vulnerable Pattern Examples

**Example 1: Using Deprecated parseAndVerifyVAA** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/wormhole-integ.md`
```solidity
// ❌ VULNERABLE: Uses deprecated method
contract WormholeReceiver {
    IWormhole public wormhole;
    
    function receiveMessage(bytes calldata vaa) external {
        // DEPRECATED: parseAndVerifyVAA is deprecated
        // Should use parseVM and verifyVM separately
        (IWormhole.VM memory vm, bool valid, string memory reason) = 
            wormhole.parseAndVerifyVAA(vaa);
        
        require(valid, reason);
        
        // Process message
        _processPayload(vm.payload);
    }
}
```

**Example 2: Missing Emitter Validation** [HIGH]
```solidity
// ❌ VULNERABLE: No emitter verification
contract VulnerableReceiver {
    function receiveMessage(bytes calldata vaa) external {
        IWormhole.VM memory vm = wormhole.parseVM(vaa);
        (bool valid,) = wormhole.verifyVM(vm);
        require(valid, "Invalid VAA");
        
        // Missing: emitter chain and address verification!
        // Attacker can submit VAA from any chain/emitter
        
        _processPayload(vm.payload);
    }
}
```

**Example 3: Weak Sequence/Nonce Validation** [HIGH]
```solidity
// ❌ VULNERABLE: Sequence tracking not per-emitter
contract WeakSequenceReceiver {
    mapping(uint64 => bool) public processedSequences;  // Global sequence!
    
    function receiveMessage(bytes calldata vaa) external {
        IWormhole.VM memory vm = wormhole.parseVM(vaa);
        
        // Wrong: Same sequence from different emitters would be blocked
        require(!processedSequences[vm.sequence], "Already processed");
        processedSequences[vm.sequence] = true;
        
        _processPayload(vm.payload);
    }
}
```

### Impact Analysis

#### Technical Impact
- **Message Forgery**: Arbitrary messages processed as legitimate
- **Double Processing**: Same message processed multiple times
- **Cross-Chain Confusion**: Messages from wrong source chains accepted

#### Business Impact
- **Fund Theft**: Attacker drains protocol funds via fake transfers
- **State Corruption**: Protocol state becomes inconsistent
- **Trust Loss**: Users lose confidence after exploit

### Secure Implementation

**Fix 1: Proper VAA Parsing with Full Validation**
```solidity
// ✅ SECURE: Complete VAA validation
contract SecureWormholeReceiver {
    IWormhole public immutable wormhole;
    
    // Track per-emitter, per-chain sequences
    mapping(uint16 => mapping(bytes32 => mapping(uint64 => bool))) public processedMessages;
    
    // Registered emitters per chain
    mapping(uint16 => bytes32) public registeredEmitters;
    
    function receiveMessage(bytes calldata vaa) external {
        // Step 1: Parse VAA
        IWormhole.VM memory vm = wormhole.parseVM(vaa);
        
        // Step 2: Verify signatures
        (bool valid, string memory reason) = wormhole.verifyVM(vm);
        require(valid, reason);
        
        // Step 3: Validate emitter chain
        require(registeredEmitters[vm.emitterChainId] != bytes32(0), "Unknown chain");
        
        // Step 4: Validate emitter address
        require(vm.emitterAddress == registeredEmitters[vm.emitterChainId], "Invalid emitter");
        
        // Step 5: Check replay (per chain, per emitter, per sequence)
        require(!processedMessages[vm.emitterChainId][vm.emitterAddress][vm.sequence], 
            "Already processed");
        processedMessages[vm.emitterChainId][vm.emitterAddress][vm.sequence] = true;
        
        // Step 6: Process payload
        _processPayload(vm.payload);
    }
}
```

---

## 2. Guardian Set Vulnerabilities

### Overview

Wormhole guardians validate and sign messages. When guardian sets are updated, old guardian set signatures remain valid for a period. This can be exploited during governance transitions.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-03-an-attacker-can-exploit-the-wormhole-guardian-change-process-to-gain-govern.md` (Code4rena)

### Vulnerability Description

#### Root Cause

Protocols don't account for guardian set transitions properly. During transitions, both old and new guardian set signatures are valid, potentially allowing replay of old guardian actions.

#### Attack Scenario

1. Protocol has governance controlled by Wormhole guardian votes
2. Guardian set update is pending (old set still valid)
3. Attacker replays old guardian-signed governance action with old guardian set
4. Action executes even though new guardians wouldn't approve it

### Vulnerable Pattern Examples

**Example 1: No Guardian Set Index Tracking** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-03-an-attacker-can-exploit-the-wormhole-guardian-change-process-to-gain-govern.md`
```solidity
// ❌ VULNERABLE: Doesn't track which guardian set signed
contract VulnerableGovernance {
    mapping(bytes32 => bool) public executedProposals;
    
    function executeProposal(bytes calldata vaa) external {
        IWormhole.VM memory vm = wormhole.parseVM(vaa);
        (bool valid,) = wormhole.verifyVM(vm);
        require(valid, "Invalid VAA");
        
        bytes32 proposalId = keccak256(vm.payload);
        require(!executedProposals[proposalId], "Already executed");
        executedProposals[proposalId] = true;
        
        // Missing: Check which guardian set signed!
        // Old guardian set can sign governance action
        // during transition period
        
        _executeGovernance(vm.payload);
    }
}
```

### Secure Implementation

**Fix: Track Guardian Set Index**
```solidity
// ✅ SECURE: Track guardian set for governance actions
contract SecureGovernance {
    // Track minimum guardian set index for new actions
    uint32 public minimumGuardianSetIndex;
    
    mapping(bytes32 => bool) public executedProposals;
    
    function executeProposal(bytes calldata vaa) external {
        IWormhole.VM memory vm = wormhole.parseVM(vaa);
        (bool valid,) = wormhole.verifyVM(vm);
        require(valid, "Invalid VAA");
        
        // Verify guardian set is current or newer
        require(vm.guardianSetIndex >= minimumGuardianSetIndex, 
            "Outdated guardian set");
        
        bytes32 proposalId = keccak256(abi.encode(
            vm.payload,
            vm.guardianSetIndex  // Include guardian set in proposal ID
        ));
        require(!executedProposals[proposalId], "Already executed");
        executedProposals[proposalId] = true;
        
        _executeGovernance(vm.payload);
    }
    
    function updateMinimumGuardianSet(uint32 newMin) external onlyOwner {
        require(newMin >= minimumGuardianSetIndex, "Cannot decrease");
        minimumGuardianSetIndex = newMin;
    }
}
```

---

## 3. Message Replay Attacks

### Overview

Cross-chain messages must be uniquely identified to prevent replay attacks. If the same message can be processed multiple times or across different contract instances, attackers can double-spend or corrupt state.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/message-replays-are-possible-across-different-instances.md` (Code4rena)

### Vulnerable Pattern Examples

**Example 1: Replay Across Contract Instances** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/message-replays-are-possible-across-different-instances.md`
```solidity
// ❌ VULNERABLE: Same VAA can be replayed across instances
contract VulnerableInstance {
    mapping(bytes32 => bool) public processedVaas;
    
    function processMessage(bytes calldata vaa) external {
        IWormhole.VM memory vm = wormhole.parseVM(vaa);
        
        // Only checks hash, not specific to this contract!
        bytes32 vaaHash = keccak256(vaa);
        require(!processedVaas[vaaHash], "Already processed");
        processedVaas[vaaHash] = true;
        
        // If multiple instances exist, same VAA works on all
        _processPayload(vm.payload);
    }
}
```

### Secure Implementation

**Fix: Instance-Specific Replay Protection**
```solidity
// ✅ SECURE: Per-instance replay protection
contract SecureInstance {
    bytes32 public immutable instanceId;
    
    mapping(bytes32 => bool) public processedVaas;
    
    constructor(bytes32 _instanceId) {
        instanceId = _instanceId;
    }
    
    function processMessage(bytes calldata vaa) external {
        IWormhole.VM memory vm = wormhole.parseVM(vaa);
        
        // Decode and verify instance ID in payload
        (bytes32 targetInstance, bytes memory actualPayload) = 
            abi.decode(vm.payload, (bytes32, bytes));
        require(targetInstance == instanceId, "Wrong instance");
        
        // Hash includes instance for additional safety
        bytes32 vaaHash = keccak256(abi.encode(instanceId, vaa));
        require(!processedVaas[vaaHash], "Already processed");
        processedVaas[vaaHash] = true;
        
        _processPayload(actualPayload);
    }
}
```

---

## 4. Token Bridge Integration

### Overview

Wormhole Token Bridge has specific patterns for bridging tokens. Incorrect integration can lead to fund loss, especially when using transferWithPayload for tokens that require external calls.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/m-20-wormhole-integration-will-not-work-for-bridging-tokens-with-external-calls.md` (Code4rena)

### Vulnerable Pattern Examples

**Example 1: Wrong Transfer Type** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/m-20-wormhole-integration-will-not-work-for-bridging-tokens-with-external-calls.md`
```solidity
// ❌ VULNERABLE: Uses transferWithPayload incorrectly
contract VulnerableBridge {
    ITokenBridge public tokenBridge;
    
    function bridgeTokens(
        address token,
        uint256 amount,
        uint16 targetChain,
        bytes32 targetAddress
    ) external {
        // transferWithPayload requires recipient contract to implement
        // completeTransferWithPayload and call TokenBridge directly
        
        tokenBridge.transferTokensWithPayload{value: msg.value}(
            token,
            amount,
            targetChain,
            targetAddress,  // If this is an EOA, tokens are stuck!
            0,
            abi.encode(msg.sender)  // Payload
        );
    }
}
```

**Example 2: Arbitrary Caller in receiveWithAnyCall** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/m-1-wrong-integration-of-wormhole-allows-arbitrary-callers-for-receivewithanycall.md`
```solidity
// ❌ VULNERABLE: Anyone can call completeTransfer
contract VulnerableReceiver {
    ITokenBridge public tokenBridge;
    
    // Public function with no access control
    function completeTransfer(bytes calldata vaa) external {
        tokenBridge.completeTransferWithPayload(vaa);
        // Attacker can complete transfer before intended recipient
        // stealing front-run opportunity
    }
}
```

### Secure Implementation

**Fix: Proper Token Bridge Integration**
```solidity
// ✅ SECURE: Correct Token Bridge usage
contract SecureTokenBridge {
    ITokenBridge public tokenBridge;
    
    // For normal transfers to EOAs, use transferTokens (not WithPayload)
    function bridgeToUser(
        address token,
        uint256 amount,
        uint16 targetChain,
        bytes32 targetAddress
    ) external payable {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        IERC20(token).approve(address(tokenBridge), amount);
        
        // Use transferTokens for EOA recipients
        tokenBridge.transferTokens{value: msg.value}(
            token,
            amount,
            targetChain,
            targetAddress,
            0,  // arbiterFee
            0   // nonce
        );
    }
    
    // For contract-to-contract with payload
    function bridgeWithPayload(
        address token,
        uint256 amount,
        uint16 targetChain,
        bytes32 targetContract,  // Must be contract implementing IWormholeReceiver
        bytes calldata payload
    ) external payable {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        IERC20(token).approve(address(tokenBridge), amount);
        
        tokenBridge.transferTokensWithPayload{value: msg.value}(
            token,
            amount,
            targetChain,
            targetContract,
            0,
            payload
        );
    }
}
```

---

## 5. Gas Limit Issues

### Overview

Wormhole relayers have gas limits for message delivery. If gas limits are immutable and become insufficient, messages can fail permanently.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-10-immutable-gaslimit-may-be-insufficient-for-wormhole-relayers-current-impl.md` (Code4rena)

### Vulnerable Pattern Examples

**Example 1: Immutable Gas Limit** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-10-immutable-gaslimit-may-be-insufficient-for-wormhole-relayers-current-impl.md`
```solidity
// ❌ VULNERABLE: Gas limit cannot be updated
contract ImmutableGasReceiver {
    uint256 public constant GAS_LIMIT = 300000;  // immutable!
    
    function requestCrossChainMessage(bytes calldata payload) external payable {
        wormhole.publishMessage{value: msg.value}(
            0,  // nonce
            payload,
            200  // consistencyLevel
        );
        
        // If Wormhole relayer updates and requires more gas,
        // this contract is permanently broken
    }
}
```

### Secure Implementation

**Fix: Configurable Gas Limits**
```solidity
// ✅ SECURE: Updatable gas configuration
contract ConfigurableGasReceiver {
    uint256 public gasLimit;
    address public owner;
    
    constructor(uint256 _initialGasLimit) {
        gasLimit = _initialGasLimit;
        owner = msg.sender;
    }
    
    function updateGasLimit(uint256 _newLimit) external {
        require(msg.sender == owner, "Only owner");
        require(_newLimit >= MIN_GAS_LIMIT, "Below minimum");
        gasLimit = _newLimit;
        emit GasLimitUpdated(_newLimit);
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: parseAndVerifyVAA (deprecated method usage)
- Pattern 2: Missing emitter chain/address validation
- Pattern 3: Sequence tracking without emitter context
- Pattern 4: No guardian set index verification for governance
- Pattern 5: Replay protection without contract instance ID
- Pattern 6: transferTokensWithPayload to non-contract recipients
- Pattern 7: Immutable gas limits
- Pattern 8: Public completeTransfer functions without access control
```

### Audit Checklist
- [ ] Verify using current Wormhole API (parseVM + verifyVM)
- [ ] Check emitter chain and address validation
- [ ] Verify replay protection is per-emitter-per-chain
- [ ] Check guardian set index for governance actions
- [ ] Ensure gas limits are configurable
- [ ] Validate Token Bridge integration patterns
- [ ] Test replay across contract instances
- [ ] Verify consistency level is appropriate

---

## Keywords for Search

`wormhole`, `VAA`, `parseAndVerifyVAA`, `parseVM`, `verifyVM`, `guardianSet`, `guardian`, `emitterChainId`, `emitterAddress`, `sequence`, `nonce`, `consistencyLevel`, `TokenBridge`, `completeTransfer`, `transferTokensWithPayload`, `NttManager`, `cross_chain`, `bridge`, `message_replay`, `governance_bypass`

---

## Related Vulnerabilities

- [LayerZero Integration Issues](../layerzero/layerzero-integration-vulnerabilities.md)
- [Cross-Chain Replay Attacks](../custom/cross-chain-replay-vulnerabilities.md)
- [Bridge Access Control](../custom/bridge-access-control.md)
