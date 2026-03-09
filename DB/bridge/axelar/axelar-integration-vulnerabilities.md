---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bridge
vulnerability_type: axelar_integration

# Attack Vector Details (Required)
attack_type: gateway_bypass|source_spoofing|express_frontrun|its_misconfiguration
affected_component: Gateway|GasService|ITS|AxelarExecutable|InterchainTokenService

# Bridge-Specific Fields
bridge_provider: axelar
bridge_attack_vector: gateway_validation|source_chain_spoofing|express_execution|its_flow_limit|gas_underpayment

# Technical Primitives (Required)
primitives:
  - AxelarExecutable
  - execute
  - executeWithToken
  - _execute
  - _executeWithToken
  - gateway
  - validateContractCall
  - validateContractCallAndMint
  - callContract
  - callContractWithToken
  - InterchainTokenService
  - TokenManager
  - flowLimit
  - sourceChain
  - sourceAddress
  - payNativeGasForContractCall
  - expressReceive
  - commandId

# Impact Classification (Required)
severity: high
impact: fund_loss|token_stuck|unlimited_minting|state_corruption
exploitability: 0.70
financial_impact: high

# Context Tags
tags:
  - defi
  - bridge
  - cross_chain
  - axelar
  - gmp
  - its
  - gateway

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Gateway & Validation Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Cross-Chain Call Revert | `reports/bridge_crosschain_findings/h-01-cross-chain-smart-contract-calls-can-revert-but-source-chain-tokens-remain-.md` | HIGH | Code4rena |
| Derby - Auth Bypass | `reports/bridge_crosschain_findings/h-6-cross-chain-message-authentication-can-be-bypassed-allowing-an-attacker-to-d.md` | HIGH | Sherlock |

### Token & ITS Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Cap Inflation via Bridging | `reports/bridge_crosschain_findings/bridging-dstoken-back-and-forth-between-chains-causes-totalissuance-cap-to-be-re.md` | MEDIUM | Cyfrin |
| Bridge Limits Bypass | `reports/bridge_crosschain_findings/bypass-of-bridge-limits-in-burnandbridgemulti-function.md` | HIGH | Halborn |

### External Links
- [Axelar Documentation](https://docs.axelar.dev/)
- [Axelar GMP](https://docs.axelar.dev/dev/general-message-passing/overview)
- [Interchain Token Service](https://docs.axelar.dev/dev/send-tokens/interchain-tokens/intro)
- [Axelar Security](https://docs.axelar.dev/learn/security)

---

# Axelar Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Axelar GMP Cross-Chain Security Audits**

---

## Table of Contents

1. [Gateway Validation Bypass](#1-gateway-validation-bypass)
2. [Source Chain & Address Spoofing](#2-source-chain--address-spoofing)
3. [Token Burn-but-Call-Fails](#3-token-burn-but-call-fails)
4. [Express Execution Front-Running](#4-express-execution-front-running)
5. [ITS Token Manager Misconfiguration](#5-its-token-manager-misconfiguration)
6. [Gas Service Payment Issues](#6-gas-service-payment-issues)
7. [String-Based Chain Matching](#7-string-based-chain-matching)
8. [Executable Contract Reentrancy](#8-executable-contract-reentrancy)
9. [Governance Proposal Replay](#9-governance-proposal-replay)
10. [Command ID Collision](#10-command-id-collision)

---

## 1. Gateway Validation Bypass

### Overview

Axelar's `AxelarExecutable` requires calling `gateway.validateContractCall()` inside `_execute()` to confirm the message was approved by the Axelar network. Skipping this check allows anyone to invoke `execute()` with forged parameters.

### Vulnerability Description

#### Root Cause

The `execute()` function in `AxelarExecutable` calls `_execute()` which is overridden by the child contract. If the child contract doesn't call `gateway.validateContractCall()` (either by not inheriting `AxelarExecutable` properly or by implementing a custom `execute()` without validation), any caller can inject fake messages.

#### Attack Scenario

1. Attacker identifies a receiver that doesn't validate via the gateway
2. Attacker calls `execute()` with forged `commandId`, `sourceChain`, `sourceAddress`, `payload`
3. Without `validateContractCall()`, the message is processed as genuine
4. Attacker drains funds or corrupts cross-chain state

### Vulnerable Pattern Examples

**Example 1: Missing validateContractCall** [CRITICAL]
```solidity
// ❌ VULNERABLE: No gateway validation — anyone can call execute
contract VulnerableAxelarReceiver {
    IAxelarGateway public gateway;
    
    function execute(
        bytes32 commandId,
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) external {
        // Missing: gateway.validateContractCall(commandId, sourceChain, sourceAddress, payloadHash)!
        
        (address recipient, uint256 amount) = abi.decode(payload, (address, uint256));
        token.transfer(recipient, amount);
    }
}
```

**Example 2: validateContractCall Return Not Checked** [HIGH]
```solidity
// ❌ VULNERABLE: Return value ignored
contract IgnoredValidation is AxelarExecutable {
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        // AxelarExecutable base handles validation, but if overridden incorrectly:
        // gateway.validateContractCall(...) returns bool that MUST be checked
        
        _processPayload(payload);
    }
}
```

### Secure Implementation

**Fix 1: Properly Inherit AxelarExecutable**
```solidity
// ✅ SECURE: AxelarExecutable handles validation automatically
import {AxelarExecutable} from "@axelar-network/axelar-gmp-sdk-solidity/contracts/executable/AxelarExecutable.sol";

contract SecureAxelarReceiver is AxelarExecutable {
    constructor(address gateway_) AxelarExecutable(gateway_) {}
    
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        // Gateway validation already performed by AxelarExecutable.execute()
        // This is safe to process
        _processPayload(sourceChain, sourceAddress, payload);
    }
}
```

**Fix 2: Manual Validation When Not Inheriting**
```solidity
// ✅ SECURE: Explicit validation
contract ManualAxelarReceiver {
    IAxelarGateway public immutable gateway;
    
    function execute(
        bytes32 commandId,
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) external {
        bytes32 payloadHash = keccak256(payload);
        
        require(
            gateway.validateContractCall(commandId, sourceChain, sourceAddress, payloadHash),
            "Not approved by gateway"
        );
        
        _processPayload(sourceChain, sourceAddress, payload);
    }
}
```

---

## 2. Source Chain & Address Spoofing

### Overview

Axelar passes `sourceChain` and `sourceAddress` as strings. Receivers must validate these match expected counterpart contracts. String comparison is error-prone and case-sensitive.

### Vulnerable Pattern Examples

**Example 1: No Source Validation** [HIGH]
```solidity
// ❌ VULNERABLE: Accepts from any source chain/address
contract NoSourceValidation is AxelarExecutable {
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        // Missing: check sourceChain and sourceAddress!
        // Any approved Axelar message from any chain is accepted
        
        (address recipient, uint256 amount) = abi.decode(payload, (address, uint256));
        token.mint(recipient, amount);
    }
}
```

**Example 2: Case-Sensitive String Comparison** [MEDIUM]
```solidity
// ❌ VULNERABLE: String comparison is case-sensitive
contract CaseSensitiveValidation is AxelarExecutable {
    string public trustedChain = "ethereum";
    
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        // "Ethereum" != "ethereum" — fails for valid messages!
        require(
            keccak256(bytes(sourceChain)) == keccak256(bytes(trustedChain)),
            "Wrong chain"
        );
        _processPayload(payload);
    }
}
```

### Secure Implementation

**Fix: Allowlist-Based Validation With Normalized Strings**
```solidity
// ✅ SECURE: Allowlist with proper string handling
contract SecureSourceValidation is AxelarExecutable {
    mapping(bytes32 => mapping(bytes32 => bool)) public trustedSenders;
    
    function setTrustedSender(
        string calldata chain,
        string calldata senderAddress,
        bool trusted
    ) external onlyOwner {
        bytes32 chainHash = keccak256(bytes(chain));
        bytes32 senderHash = keccak256(bytes(senderAddress));
        trustedSenders[chainHash][senderHash] = trusted;
    }
    
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        bytes32 chainHash = keccak256(bytes(sourceChain));
        bytes32 senderHash = keccak256(bytes(sourceAddress));
        
        require(trustedSenders[chainHash][senderHash], "Untrusted sender");
        _processPayload(sourceChain, sourceAddress, payload);
    }
}
```

---

## 3. Token Burn-but-Call-Fails

### Overview

`callContractWithToken()` burns/locks tokens on the source chain before the destination call executes. If `_executeWithToken()` reverts, tokens are burned but never received — permanent fund loss.

### Vulnerable Pattern Examples

**Example 1: Reverting executeWithToken** [HIGH]
```solidity
// ❌ VULNERABLE: Revert after token burn on source = fund loss
contract RevertingTokenReceiver is AxelarExecutable {
    function _executeWithToken(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload,
        string calldata tokenSymbol,
        uint256 amount
    ) internal override {
        address recipient = abi.decode(payload, (address));
        address token = gateway.tokenAddresses(tokenSymbol);
        
        // If this reverts, tokens were already burned on source chain!
        // No recovery mechanism — funds permanently lost
        require(recipient != address(0), "Bad recipient");  // Can revert!
        
        IERC20(token).transfer(recipient, amount);
    }
}
```

### Secure Implementation

**Fix: Never Revert — Use Try-Catch With Fallback**
```solidity
// ✅ SECURE: Handle all failures gracefully
contract SafeTokenReceiver is AxelarExecutable {
    mapping(bytes32 => PendingTransfer) public pendingTransfers;
    
    function _executeWithToken(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload,
        string calldata tokenSymbol,
        uint256 amount
    ) internal override {
        address token = gateway.tokenAddresses(tokenSymbol);
        
        try this.processTokenTransfer(payload, token, amount) {
            // Success
        } catch {
            // Store for manual recovery — never lose tokens
            bytes32 key = keccak256(abi.encode(sourceChain, sourceAddress, payload));
            pendingTransfers[key] = PendingTransfer(token, amount, block.timestamp);
            emit TransferFailed(key, token, amount);
        }
    }
    
    function recoverFailedTransfer(bytes32 key, address recipient) external onlyOwner {
        PendingTransfer memory pt = pendingTransfers[key];
        require(pt.amount > 0, "No pending transfer");
        delete pendingTransfers[key];
        IERC20(pt.token).transfer(recipient, pt.amount);
    }
}
```

---

## 4. Express Execution Front-Running

### Overview

Axelar Express allows relayers to front-fund cross-chain transfers for faster execution. If the express execution flow isn't properly coordinated, the standard execution can arrive later and double-credit the user.

### Vulnerable Pattern Examples

**Example 1: No Express Check Before Standard Execution** [HIGH]
```solidity
// ❌ VULNERABLE: No check if express already processed
contract VulnerableExpressReceiver is AxelarExecutable {
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        // Both express and standard execution call this!
        // If express already credited user, standard credits again
        
        (address recipient, uint256 amount) = abi.decode(payload, (address, uint256));
        token.mint(recipient, amount);  // Double mint!
    }
}
```

### Secure Implementation

**Fix: Use ExpressExecutable Base Contract**
```solidity
// ✅ SECURE: ExpressExecutable handles express vs standard coordination
import {ExpressExecutable} from "@axelar-network/axelar-gmp-sdk-solidity/contracts/express/ExpressExecutable.sol";

contract SecureExpressReceiver is ExpressExecutable {
    constructor(address gateway_) ExpressExecutable(gateway_) {}
    
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        // ExpressExecutable automatically handles deduplication:
        // - Express execution: funds user immediately
        // - Standard execution: reimburses express relayer (not user again)
        
        (address recipient, uint256 amount) = abi.decode(payload, (address, uint256));
        token.mint(recipient, amount);
    }
}
```

---

## 5. ITS Token Manager Misconfiguration

### Overview

Axelar's Interchain Token Service (ITS) manages cross-chain token operations through TokenManagers. Incorrect TokenManager type or flow limit configuration creates supply imbalance.

### Vulnerable Pattern Examples

**Example 1: Lock-Unlock on Multiple Chains** [CRITICAL]
```solidity
// ❌ VULNERABLE: Lock-Unlock TokenManager on non-origin chains
// Token supply DOUBLES each bridge cycle because neither chain burns

// Chain A (origin): Lock-Unlock → correct, tokens are locked
// Chain B (remote): Lock-Unlock → WRONG! Should be Mint-Burn
// 
// User bridges 100 tokens A→B: locks on A, unlocks on B (200 total circulating)
// User bridges 100 tokens B→A: locks on B, unlocks on A (200 total still)
// Repeat: supply keeps inflating
```

**Example 2: No Flow Limit Set** [HIGH]
```solidity
// ❌ VULNERABLE: Zero flow limit means unlimited bridging
contract UnlimitedITSToken {
    // If flowLimit == 0, there is no restriction on bridge volume
    // A compromised relayer can bridge the entire supply instantly
    
    // TokenManager deployed with:
    // flowLimit: 0  // ← No limit! Entire supply can be drained
}
```

### Secure Implementation

**Fix: Correct Manager Types + Flow Limits**
```solidity
// ✅ SECURE: Mint-Burn on remote chains + flow limits

// Origin chain: LOCK_UNLOCK TokenManager
// Remote chains: MINT_BURN TokenManager

// Configure flow limits per chain:
ITokenManager(tokenManager).setFlowLimit(
    1_000_000e18  // Max 1M tokens per 6-hour epoch
);

// Verify configuration:
// - flowLimit > 0 on all chains
// - Origin uses LOCK_UNLOCK, remotes use MINT_BURN
// - Total remote supply <= locked amount on origin
```

---

## 6. Gas Service Payment Issues

### Overview

Axelar requires gas prepayment via `AxelarGasService.payNativeGasForContractCall()`. Underpaying causes messages to be stuck in the Axelar network — never executed on the destination.

### Vulnerable Pattern Examples

**Example 1: No Gas Payment** [HIGH]
```solidity
// ❌ VULNERABLE: Message sent without gas payment — stuck forever
contract NoGasPayment is AxelarExecutable {
    function sendMessage(
        string calldata destChain,
        string calldata destAddress,
        bytes calldata payload
    ) external {
        // Missing: gasService.payNativeGasForContractCall{value: gasFee}(...)
        
        // Message is approved on Axelar but never relayed to destination
        gateway.callContract(destChain, destAddress, payload);
    }
}
```

**Example 2: Hardcoded Gas Amount** [MEDIUM]
```solidity
// ❌ VULNERABLE: Hardcoded gas doesn't account for destination chain costs
contract HardcodedGasPayment is AxelarExecutable {
    function sendMessage(
        string calldata destChain,
        string calldata destAddress,
        bytes calldata payload
    ) external payable {
        gasService.payNativeGasForContractCall{value: 0.01 ether}(
            address(this), destChain, destAddress, payload, msg.sender
        );
        
        // If destChain is expensive (e.g., Ethereum), 0.01 ether may be insufficient
        // Message gets stuck or executed with insufficient gas on destination
        gateway.callContract(destChain, destAddress, payload);
    }
}
```

### Secure Implementation

**Fix: Dynamic Gas Estimation**
```solidity
// ✅ SECURE: Estimate gas based on destination and payload
contract SecureGasPayment is AxelarExecutable {
    IAxelarGasService public immutable gasService;
    mapping(string => uint256) public gasEstimates;
    
    function setGasEstimate(string calldata chain, uint256 estimate) external onlyOwner {
        gasEstimates[chain] = estimate;
    }
    
    function sendMessage(
        string calldata destChain,
        string calldata destAddress,
        bytes calldata payload
    ) external payable {
        uint256 gasEstimate = gasEstimates[destChain];
        require(gasEstimate > 0, "Chain not configured");
        require(msg.value >= gasEstimate, "Insufficient gas payment");
        
        gasService.payNativeGasForContractCall{value: gasEstimate}(
            address(this), destChain, destAddress, payload, msg.sender
        );
        
        gateway.callContract(destChain, destAddress, payload);
        
        // Refund excess
        if (msg.value > gasEstimate) {
            payable(msg.sender).transfer(msg.value - gasEstimate);
        }
    }
}
```

---

## 7. String-Based Chain Matching

### Overview

Axelar uses strings for chain identifiers (e.g., `"ethereum"`, `"Polygon"`) unlike other bridges that use numeric chain IDs. This introduces encoding and case-sensitivity issues.

### Vulnerable Pattern Examples

**Example 1: String Comparison Inconsistency** [MEDIUM]
```solidity
// ❌ VULNERABLE: Different representations of same chain
contract InconsistentChainNames {
    // Source sends with "Polygon"
    // Receiver expects "polygon"
    // keccak256("Polygon") != keccak256("polygon")
    
    mapping(string => bool) allowedChains;
    
    constructor() {
        allowedChains["polygon"] = true;  // Lowercase
        // But Axelar may deliver as "Polygon" — mismatch!
    }
}
```

### Secure Implementation

**Fix: Use Exact Axelar Chain Names**
```solidity
// ✅ SECURE: Store and compare using Axelar's exact chain IDs
contract ExactChainNames is AxelarExecutable {
    // Use Axelar's canonical chain names from docs
    mapping(bytes32 => bool) public allowedChainHashes;
    
    function setAllowedChain(string calldata chain, bool allowed) external onlyOwner {
        // Store exact chain name as provided by Axelar
        allowedChainHashes[keccak256(bytes(chain))] = allowed;
    }
    
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        require(allowedChainHashes[keccak256(bytes(sourceChain))], "Chain not allowed");
        _processPayload(payload);
    }
}
```

---

## 8. Executable Contract Reentrancy

### Overview

`_executeWithToken()` receives tokens before the callback logic runs. If the callback makes external calls, reentrancy can drain the received tokens.

### Vulnerable Pattern Examples

**Example 1: External Call Before State Update** [HIGH]
```solidity
// ❌ VULNERABLE: Reentrancy in _executeWithToken
contract ReentrantTokenReceiver is AxelarExecutable {
    mapping(address => uint256) public balances;
    
    function _executeWithToken(
        string calldata, string calldata, bytes calldata payload,
        string calldata tokenSymbol, uint256 amount
    ) internal override {
        address recipient = abi.decode(payload, (address));
        address token = gateway.tokenAddresses(tokenSymbol);
        
        // External call BEFORE state update!
        (bool success,) = recipient.call("");
        require(success);
        
        // State update happens after external call
        balances[recipient] += amount;  // Reentrancy vector!
    }
}
```

### Secure Implementation

**Fix: CEI Pattern + Reentrancy Guard**
```solidity
// ✅ SECURE: Checks-Effects-Interactions + ReentrancyGuard
contract SecureTokenReceiver is AxelarExecutable, ReentrancyGuard {
    function _executeWithToken(
        string calldata, string calldata, bytes calldata payload,
        string calldata tokenSymbol, uint256 amount
    ) internal override nonReentrant {
        address recipient = abi.decode(payload, (address));
        address token = gateway.tokenAddresses(tokenSymbol);
        
        // State update FIRST (CEI pattern)
        balances[recipient] += amount;
        
        // Then external call
        IERC20(token).transfer(recipient, amount);
    }
}
```

---

## 9. Governance Proposal Replay

### Overview

Cross-chain governance proposals executed via Axelar must include replay protection. Without it, the same governance action can be executed on multiple chains or multiple times.

### Vulnerable Pattern Examples

**Example 1: No Command ID Tracking** [HIGH]
```solidity
// ❌ VULNERABLE: No tracking of executed governance commands
contract VulnerableGovernance is AxelarExecutable {
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        // commandId not tracked — same governance action can be replayed
        (bytes4 selector, bytes memory data) = abi.decode(payload, (bytes4, bytes));
        
        // Execute governance action without checking if already done
        (bool success,) = address(this).call(abi.encodePacked(selector, data));
        require(success);
    }
}
```

### Secure Implementation

**Fix: Track Executed Commands**
```solidity
// ✅ SECURE: Track all executed governance commands
contract SecureGovernance is AxelarExecutable {
    mapping(bytes32 => bool) public executedCommands;
    
    function execute(
        bytes32 commandId,
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) external override {
        // Track before execution
        require(!executedCommands[commandId], "Already executed");
        executedCommands[commandId] = true;
        
        // Validate through gateway
        bytes32 payloadHash = keccak256(payload);
        require(
            gateway.validateContractCall(commandId, sourceChain, sourceAddress, payloadHash),
            "Not approved"
        );
        
        _execute(sourceChain, sourceAddress, payload);
    }
}
```

---

## 10. Command ID Collision

### Overview

Axelar uses `commandId` to uniquely identify cross-chain messages. If contracts use commandId for their own tracking but don't namespace it properly, collisions can occur across different message types.

### Vulnerable Pattern Examples

**Example 1: Reusing commandId Across Message Types** [MEDIUM]
```solidity
// ❌ VULNERABLE: Same commandId space for different message types
contract SharedCommandSpace is AxelarExecutable {
    mapping(bytes32 => bool) public processedCommands;
    
    function _execute(..., bytes calldata payload) internal override {
        bytes32 cmdId = /* from execute() context */;
        processedCommands[cmdId] = true;
        // If cmdId collides with a token transfer command,
        // the token transfer is blocked
    }
    
    function _executeWithToken(...) internal override {
        bytes32 cmdId = /* from execute() context */;
        processedCommands[cmdId] = true;
        // Same mapping — collision risk with plain execute
    }
}
```

### Secure Implementation

**Fix: Namespace Command Tracking**
```solidity
// ✅ SECURE: Separate tracking per message type
contract NamespacedCommands is AxelarExecutable {
    mapping(bytes32 => bool) public processedCalls;
    mapping(bytes32 => bool) public processedTokenCalls;
    
    function _execute(..., bytes calldata payload) internal override {
        bytes32 key = keccak256(abi.encode("CALL", commandId));
        require(!processedCalls[key], "Already processed");
        processedCalls[key] = true;
        _processPayload(payload);
    }
    
    function _executeWithToken(..., uint256 amount) internal override {
        bytes32 key = keccak256(abi.encode("TOKEN_CALL", commandId));
        require(!processedTokenCalls[key], "Already processed");
        processedTokenCalls[key] = true;
        _processTokenPayload(payload, amount);
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: AxelarExecutable without validateContractCall in custom execute
- Pattern 2: _execute without sourceChain/sourceAddress validation
- Pattern 3: _executeWithToken without try-catch (revert = permanent fund loss)
- Pattern 4: Missing payNativeGasForContractCall before callContract
- Pattern 5: Hardcoded gas payment amounts
- Pattern 6: String comparison without canonical chain name validation
- Pattern 7: External calls in _executeWithToken before state updates
- Pattern 8: ITS TokenManager type mismatch (Lock-Unlock on remote chain)
- Pattern 9: flowLimit == 0 on ITS TokenManagers
- Pattern 10: express execution without deduplication check
```

### Audit Checklist
- [ ] Verify _execute inherits AxelarExecutable and gateway validation occurs
- [ ] Check sourceChain and sourceAddress are validated against allowlist
- [ ] Ensure _executeWithToken never reverts (use try-catch)
- [ ] Verify gas payment via AxelarGasService before every callContract
- [ ] Check string chain names match Axelar's canonical names
- [ ] Validate ITS TokenManager types (Lock-Unlock on origin only)
- [ ] Confirm flowLimit > 0 on all ITS TokenManagers
- [ ] Check for reentrancy in _executeWithToken callbacks
- [ ] Verify express execution doesn't double-credit users
- [ ] Check commandId replay protection

---

## Keywords for Search

`axelar`, `AxelarExecutable`, `gateway`, `validateContractCall`, `callContract`, `callContractWithToken`, `_execute`, `_executeWithToken`, `GasService`, `payNativeGasForContractCall`, `InterchainTokenService`, `ITS`, `TokenManager`, `flowLimit`, `sourceChain`, `sourceAddress`, `commandId`, `expressReceive`, `ExpressExecutable`, `cross_chain`, `bridge`, `gmp`, `general_message_passing`, `token_manager`, `lock_unlock`, `mint_burn`

---

## Related Vulnerabilities

- [CCIP Integration Issues](../ccip/ccip-integration-vulnerabilities.md)
- [Wormhole Integration Issues](../wormhole/wormhole-integration-vulnerabilities.md)
- [Cross-Chain General Vulnerabilities](../custom/cross-chain-general-vulnerabilities.md)
- [LayerZero Integration Issues](../layerzero/layerzero-integration-vulnerabilities.md)
