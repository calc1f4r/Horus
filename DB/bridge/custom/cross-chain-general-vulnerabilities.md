---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bridge
vulnerability_type: cross_chain_general

# Attack Vector Details (Required)
attack_type: replay_attack|access_control|message_validation|token_handling|reentrancy
affected_component: Bridge|Receiver|Sender|TokenHandler|MessageProcessor

# Bridge-Specific Fields
bridge_provider: custom
bridge_attack_vector: cross_chain_replay|signature_validation|token_mismatch|slippage|sequencer_down

# Technical Primitives (Required)
primitives:
  - receiveMessage
  - sendMessage
  - processMessage
  - bridgeTokens
  - mint
  - burn
  - lock
  - unlock
  - chainId
  - nonce
  - signature
  - sequencer

# Impact Classification (Required)
severity: high
impact: fund_loss|double_spending|replay_attack|token_stuck
exploitability: 0.75
financial_impact: critical

# Context Tags
tags:
  - defi
  - bridge
  - cross_chain
  - multichain
  - replay
  - signature
  - access_control

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Cross-Chain Replay Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Replay Across Instances | `reports/bridge_crosschain_findings/message-replays-are-possible-across-different-instances.md` | HIGH | Code4rena |
| Cross-Chain Signature Replay | `reports/bridge_crosschain_findings/signatures-can-be-replayed-cross-chain.md` | HIGH | Sherlock |
| Nonce Replay | `reports/bridge_crosschain_findings/h-1-replay-of-mpc-signed-messages.md` | HIGH | Sherlock |

### Sequencer & L2 Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Sequencer Down | `reports/bridge_crosschain_findings/access-controlled-functions-cannot-be-called-when-l2-sequencers-are-down.md` | MEDIUM | Sherlock |
| Blast Gateway Reverts | `reports/bridge_crosschain_findings/m-15-blast-gateway-reverts-if-it-receives-rebasing-yield-mode-tokens.md` | MEDIUM | Sherlock |

### Token Handling Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DAI to Blast | `reports/bridge_crosschain_findings/across-it-will-not-be-possible-to-bridge-dai-to-blast.md` | MEDIUM | Sherlock |
| Token Mismatch | `reports/bridge_crosschain_findings/m-09-wrong-token-address-is-passed-to-lzcompose-when-msg_-is-of-compose-type.md` | MEDIUM | Sherlock |
| Slippage Issues | `reports/bridge_crosschain_findings/_slippagetol-does-not-adjust-for-decimal-differences.md` | MEDIUM | Sherlock |

### Access Control Issues  
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Lock Approval Bypass | `reports/bridge_crosschain_findings/a-user-can-steal-an-already-transfered-and-bridged-resdl-lock-because-of-approva.md` | HIGH | Code4rena |
| Front-running Bridge | `reports/bridge_crosschain_findings/account-creation-front-running-vulnerability-leading-to-gas-fee-theft.md` | MEDIUM | Sherlock |

### External Links
- [Cross-Chain Security Best Practices](https://docs.openzeppelin.com/)
- [Bridge Security Framework](https://github.com/defi-wonderland)
- [EIP-712 Signatures](https://eips.ethereum.org/EIPS/eip-712)

---

# Cross-Chain General Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Custom Bridge & Cross-Chain Security Audits**

---

## Table of Contents

1. [Cross-Chain Replay Attacks](#1-cross-chain-replay-attacks)
2. [Signature Validation Issues](#2-signature-validation-issues)
3. [Token Bridging Issues](#3-token-bridging-issues)
4. [Sequencer & L2 Specific Issues](#4-sequencer--l2-specific-issues)
5. [Access Control Vulnerabilities](#5-access-control-vulnerabilities)
6. [Slippage & MEV Issues](#6-slippage--mev-issues)
7. [Message Ordering & Timing](#7-message-ordering--timing)

---

## 1. Cross-Chain Replay Attacks

### Overview

Cross-chain replay attacks occur when a valid message on one chain can be replayed on another chain (or same chain multiple times). This is one of the most critical vulnerability classes in bridge security.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/message-replays-are-possible-across-different-instances.md`
> - `reports/bridge_crosschain_findings/signatures-can-be-replayed-cross-chain.md`
> - `reports/bridge_crosschain_findings/h-1-replay-of-mpc-signed-messages.md`

### Vulnerability Description

#### Root Cause

Bridge messages or signatures don't include sufficient context (chain ID, contract address, nonce) to prevent replay across different chains or contract instances.

#### Attack Scenarios

**Scenario 1: Cross-Chain Signature Replay**
1. User signs message to bridge tokens on Chain A
2. Relayer executes on Chain A successfully
3. Attacker replays same signature on Chain B
4. Tokens minted on Chain B without burning on source

**Scenario 2: Same-Chain Instance Replay**
1. Protocol has multiple bridge instances on same chain
2. User bridges via Instance A
3. Attacker replays message on Instance B
4. User receives double the tokens

**Scenario 3: Nonce Collision**
1. Bridge uses simple incrementing nonce
2. Different users get same nonce on different chains
3. Messages can be confused or replayed

### Vulnerable Pattern Examples

**Example 1: Missing Chain ID in Signature** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/signatures-can-be-replayed-cross-chain.md`
```solidity
// ❌ VULNERABLE: No chain ID in signed message
contract VulnerableBridge {
    function bridgeWithSignature(
        address token,
        uint256 amount,
        address recipient,
        bytes calldata signature
    ) external {
        bytes32 messageHash = keccak256(abi.encode(
            token,
            amount,
            recipient
            // Missing: block.chainid!
        ));
        
        address signer = ECDSA.recover(messageHash, signature);
        require(signer == trustedSigner, "Invalid signature");
        
        // Same signature works on all chains!
        _mintTokens(recipient, amount);
    }
}
```

**Example 2: Missing Contract Address** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/message-replays-are-possible-across-different-instances.md`
```solidity
// ❌ VULNERABLE: No contract address in replay protection
contract VulnerableReceiver {
    mapping(bytes32 => bool) public processedMessages;
    
    function processMessage(
        bytes32 messageHash,
        bytes calldata payload
    ) external {
        // Hash doesn't include this contract's address!
        require(!processedMessages[messageHash], "Already processed");
        processedMessages[messageHash] = true;
        
        // If multiple instances exist, same message works on all
        _executePayload(payload);
    }
}
```

**Example 3: Weak Nonce Handling** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-1-replay-of-mpc-signed-messages.md`
```solidity
// ❌ VULNERABLE: Global nonce allows replay
contract WeakNonceBridge {
    mapping(uint256 => bool) public usedNonces;  // Global, not per-sender
    
    function execute(
        uint256 nonce,
        bytes calldata data,
        bytes calldata signature
    ) external {
        require(!usedNonces[nonce], "Nonce used");
        usedNonces[nonce] = true;
        
        // Different signers can use same nonce!
        // Or same nonce on different chains
        _execute(data, signature);
    }
}
```

### Impact Analysis

#### Technical Impact
- **Double Minting**: Tokens minted multiple times for single deposit
- **Fund Drainage**: Protocol reserves depleted
- **State Corruption**: Accounting becomes incorrect

#### Business Impact
- **Protocol Insolvency**: Cannot redeem all tokens
- **User Loss**: Legitimate users cannot withdraw
- **Token Devaluation**: Supply inflation destroys value

### Secure Implementation

**Fix 1: Complete Domain Separation (EIP-712)**
```solidity
// ✅ SECURE: Full EIP-712 domain separation
contract SecureBridge {
    bytes32 public immutable DOMAIN_SEPARATOR;
    bytes32 public constant BRIDGE_TYPEHASH = keccak256(
        "Bridge(address token,uint256 amount,address recipient,uint256 nonce,uint256 deadline)"
    );
    
    mapping(address => uint256) public nonces;
    
    constructor() {
        DOMAIN_SEPARATOR = keccak256(abi.encode(
            keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
            keccak256("SecureBridge"),
            keccak256("1"),
            block.chainid,
            address(this)  // Contract address included!
        ));
    }
    
    function bridgeWithSignature(
        address token,
        uint256 amount,
        address recipient,
        uint256 deadline,
        bytes calldata signature
    ) external {
        require(block.timestamp <= deadline, "Expired");
        
        uint256 nonce = nonces[recipient]++;
        
        bytes32 structHash = keccak256(abi.encode(
            BRIDGE_TYPEHASH,
            token,
            amount,
            recipient,
            nonce,
            deadline
        ));
        
        bytes32 digest = keccak256(abi.encodePacked(
            "\x19\x01",
            DOMAIN_SEPARATOR,
            structHash
        ));
        
        address signer = ECDSA.recover(digest, signature);
        require(signer == trustedSigner, "Invalid signature");
        
        _mintTokens(recipient, amount);
    }
}
```

**Fix 2: Per-Sender Nonce with Chain/Contract**
```solidity
// ✅ SECURE: Complete replay protection
contract SecureReplayProtection {
    // Nonce per sender, per source chain
    mapping(uint256 => mapping(address => uint256)) public nonces;
    
    // Message tracking includes all context
    mapping(bytes32 => bool) public processedMessages;
    
    function processMessage(
        uint256 sourceChainId,
        address sender,
        uint256 nonce,
        bytes calldata payload,
        bytes calldata proof
    ) external {
        // Check nonce is expected
        require(nonce == nonces[sourceChainId][sender], "Invalid nonce");
        nonces[sourceChainId][sender]++;
        
        // Create unique message ID with all context
        bytes32 messageId = keccak256(abi.encode(
            sourceChainId,      // Source chain
            block.chainid,       // Destination chain
            address(this),       // This contract
            sender,              // Sender
            nonce,               // Nonce
            payload              // Payload
        ));
        
        require(!processedMessages[messageId], "Already processed");
        processedMessages[messageId] = true;
        
        _verifyAndExecute(payload, proof);
    }
}
```

---

## 2. Signature Validation Issues

### Overview

Bridges often rely on trusted signatures (multisig, MPC, or oracle signatures) to validate cross-chain messages. Incorrect signature validation can lead to unauthorized message execution.

### Vulnerable Pattern Examples

**Example 1: Missing Signature Length Check** [HIGH]
```solidity
// ❌ VULNERABLE: No signature length validation
contract WeakSignatureValidation {
    function verify(bytes32 hash, bytes memory signature) internal view returns (bool) {
        // Missing length check - compact signatures not handled
        (uint8 v, bytes32 r, bytes32 s) = abi.decode(signature, (uint8, bytes32, bytes32));
        return ecrecover(hash, v, r, s) == trustedSigner;
    }
}
```

**Example 2: Signature Malleability** [MEDIUM]
```solidity
// ❌ VULNERABLE: Malleable signatures
contract MalleableSignatures {
    mapping(bytes => bool) public usedSignatures;
    
    function execute(bytes32 hash, bytes calldata signature) external {
        require(!usedSignatures[signature], "Used");
        usedSignatures[signature] = true;  // Malleable sig can bypass!
        
        // s can be flipped to create different but valid signature
        require(verify(hash, signature), "Invalid");
        _execute(hash);
    }
}
```

### Secure Implementation

**Fix: Use OpenZeppelin ECDSA**
```solidity
// ✅ SECURE: Proper signature validation
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract SecureSignatureValidation {
    using ECDSA for bytes32;
    
    mapping(bytes32 => bool) public usedMessageHashes;  // Track hash, not signature!
    
    function execute(bytes32 hash, bytes calldata signature) external {
        // Track by hash, not signature (prevents malleability bypass)
        require(!usedMessageHashes[hash], "Already executed");
        usedMessageHashes[hash] = true;
        
        // ECDSA library handles all edge cases
        address signer = hash.toEthSignedMessageHash().recover(signature);
        require(signer == trustedSigner, "Invalid signer");
        
        _execute(hash);
    }
}
```

---

## 3. Token Bridging Issues

### Overview

Token bridging involves complex token handling patterns. Issues arise from token incompatibilities, decimal mismatches, and special token behaviors.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/across-it-will-not-be-possible-to-bridge-dai-to-blast.md`
> - `reports/bridge_crosschain_findings/m-15-blast-gateway-reverts-if-it-receives-rebasing-yield-mode-tokens.md`
> - `reports/bridge_crosschain_findings/m-09-wrong-token-address-is-passed-to-lzcompose-when-msg_-is-of-compose-type.md`

### Vulnerable Pattern Examples

**Example 1: Fee-on-Transfer Token Incompatibility** [MEDIUM]
```solidity
// ❌ VULNERABLE: Doesn't account for transfer fees
contract VulnerableTokenBridge {
    function bridgeTokens(address token, uint256 amount) external {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        
        // For fee-on-transfer tokens, actual received < amount
        _sendCrossChain(token, amount);  // Mints too many tokens!
    }
}
```

**Example 2: Rebasing Token Issues** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/m-15-blast-gateway-reverts-if-it-receives-rebasing-yield-mode-tokens.md`
```solidity
// ❌ VULNERABLE: Rebasing tokens break accounting
contract RebasingVulnerable {
    mapping(address => uint256) public deposits;
    
    function deposit(address token, uint256 amount) external {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        deposits[msg.sender] += amount;
        // For rebasing tokens, balance changes over time!
        // User can withdraw more than deposited
    }
}
```

**Example 3: Decimal Mismatch** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/_slippagetol-does-not-adjust-for-decimal-differences.md`
```solidity
// ❌ VULNERABLE: No decimal normalization
contract DecimalMismatch {
    function bridge(
        address sourceToken,  // 6 decimals (USDC)
        address destToken,    // 18 decimals
        uint256 amount
    ) external {
        // 1 USDC (1e6) bridged as if 1e6 of 18-decimal token
        // User loses massive value!
        _bridge(sourceToken, destToken, amount);
    }
}
```

### Secure Implementation

**Fix 1: Measure Actual Received Amount**
```solidity
// ✅ SECURE: Handle fee-on-transfer tokens
contract SecureTokenBridge {
    function bridgeTokens(address token, uint256 amount) external {
        uint256 balanceBefore = IERC20(token).balanceOf(address(this));
        
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        
        uint256 actualReceived = IERC20(token).balanceOf(address(this)) - balanceBefore;
        
        // Use actual received amount
        _sendCrossChain(token, actualReceived);
    }
}
```

**Fix 2: Decimal Normalization**
```solidity
// ✅ SECURE: Normalize decimals
contract SecureDecimalHandling {
    uint8 constant STANDARD_DECIMALS = 18;
    
    function normalizeAmount(
        uint256 amount,
        uint8 tokenDecimals
    ) internal pure returns (uint256) {
        if (tokenDecimals < STANDARD_DECIMALS) {
            return amount * (10 ** (STANDARD_DECIMALS - tokenDecimals));
        } else if (tokenDecimals > STANDARD_DECIMALS) {
            return amount / (10 ** (tokenDecimals - STANDARD_DECIMALS));
        }
        return amount;
    }
    
    function denormalizeAmount(
        uint256 normalizedAmount,
        uint8 tokenDecimals
    ) internal pure returns (uint256) {
        if (tokenDecimals < STANDARD_DECIMALS) {
            return normalizedAmount / (10 ** (STANDARD_DECIMALS - tokenDecimals));
        } else if (tokenDecimals > STANDARD_DECIMALS) {
            return normalizedAmount * (10 ** (tokenDecimals - STANDARD_DECIMALS));
        }
        return normalizedAmount;
    }
}
```

---

## 4. Sequencer & L2 Specific Issues

### Overview

L2 bridges face unique challenges with sequencer availability, forced transactions, and L1<->L2 timing assumptions.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/access-controlled-functions-cannot-be-called-when-l2-sequencers-are-down.md`

### Vulnerable Pattern Examples

**Example 1: Sequencer Down DoS** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/access-controlled-functions-cannot-be-called-when-l2-sequencers-are-down.md`
```solidity
// ❌ VULNERABLE: Blocked when sequencer down
contract SequencerDependentBridge {
    function emergencyWithdraw() external onlyOwner {
        // If sequencer is down, owner cannot call this!
        // Users may be locked out during emergency
        _executeWithdraw();
    }
}
```

**Example 2: Timestamp Assumptions** [MEDIUM]
```solidity
// ❌ VULNERABLE: L2 timestamp assumptions
contract TimestampVulnerable {
    uint256 public constant FINALITY_DELAY = 1 hours;
    
    function claim(bytes32 messageId) external {
        require(
            block.timestamp >= messageTimestamp[messageId] + FINALITY_DELAY,
            "Not finalized"
        );
        // On L2, block.timestamp behavior differs!
        // May not provide expected security guarantees
    }
}
```

### Secure Implementation

**Fix: Sequencer-Aware Design**
```solidity
// ✅ SECURE: Account for sequencer downtime
contract SequencerAwareBridge {
    AggregatorV3Interface public sequencerUptimeFeed;
    uint256 public constant GRACE_PERIOD = 1 hours;
    
    modifier sequencerActive() {
        (, int256 answer, uint256 startedAt,,) = sequencerUptimeFeed.latestRoundData();
        
        // Answer == 0: Sequencer is up
        // Answer == 1: Sequencer is down
        bool isSequencerUp = answer == 0;
        
        if (!isSequencerUp) {
            revert("Sequencer down");
        }
        
        // Check grace period after restart
        uint256 timeSinceUp = block.timestamp - startedAt;
        if (timeSinceUp < GRACE_PERIOD) {
            revert("Grace period active");
        }
        
        _;
    }
    
    // Alternative: Allow L1 force-include for emergencies
    function emergencyWithdrawL1(
        bytes calldata proof
    ) external {
        // Verify this is a valid L1 force-included tx
        require(_verifyL1ForceInclusion(proof), "Invalid proof");
        _executeWithdraw();
    }
}
```

---

## 5. Access Control Vulnerabilities

### Overview

Cross-chain access control is complex because the caller on the destination chain differs from the original user. Improper access control leads to unauthorized actions.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/a-user-can-steal-an-already-transfered-and-bridged-resdl-lock-because-of-approva.md`
> - `reports/bridge_crosschain_findings/account-creation-front-running-vulnerability-leading-to-gas-fee-theft.md`

### Vulnerable Pattern Examples

**Example 1: Approval Persistence After Bridge** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/a-user-can-steal-an-already-transfered-and-bridged-resdl-lock-because-of-approva.md`
```solidity
// ❌ VULNERABLE: Approval persists after bridging
contract VulnerableNFTBridge {
    function bridge(uint256 tokenId) external {
        // Transfer NFT to bridge contract
        nft.transferFrom(msg.sender, address(this), tokenId);
        
        // Issue: If msg.sender had approved someone,
        // that approval may persist in original contract
        // Attacker can transfer the bridged NFT representation
        
        _mintBridgedNFT(msg.sender, tokenId);
    }
}
```

**Example 2: Front-Running Account Creation** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/account-creation-front-running-vulnerability-leading-to-gas-fee-theft.md`
```solidity
// ❌ VULNERABLE: Predictable account addresses
contract VulnerableAccountBridge {
    function createCrossChainAccount(address user) external {
        // Attacker can front-run with same user address
        // and steal deposited gas fees
        
        address account = _computeAddress(user);
        // Account created at predictable address
    }
}
```

### Secure Implementation

**Fix: Revoke Approvals and Secure Account Creation**
```solidity
// ✅ SECURE: Clear approvals and use salt
contract SecureBridge {
    function bridgeNFT(uint256 tokenId) external {
        // Clear any existing approvals
        nft.approve(address(0), tokenId);
        
        nft.transferFrom(msg.sender, address(this), tokenId);
        _mintBridgedNFT(msg.sender, tokenId);
    }
    
    function createCrossChainAccount(
        address user,
        bytes32 salt  // User-provided salt
    ) external {
        // Use salt to prevent front-running
        address account = _computeAddressWithSalt(user, salt);
        require(account == msg.sender, "Wrong caller");
        
        _createAccount(account);
    }
}
```

---

## 6. Slippage & MEV Issues

### Overview

Cross-chain swaps and bridges are vulnerable to MEV attacks and slippage issues due to timing differences between chains.

### Vulnerable Pattern Examples

**Example 1: No Slippage Protection** [MEDIUM]
```solidity
// ❌ VULNERABLE: No minimum output
contract NoSlippageProtection {
    function bridgeAndSwap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) external {
        _bridge(tokenIn, amountIn);
        
        // On destination, swap at whatever rate
        // Attacker sandwiches for profit
        _swap(tokenIn, tokenOut, amountIn);
    }
}
```

**Example 2: Stale Price During Bridge Delay** [MEDIUM]
```solidity
// ❌ VULNERABLE: Price can change during bridge delay
contract StalePriceBridge {
    function quote(uint256 amount) external view returns (uint256) {
        // Price quoted at time T
        return oracle.getPrice() * amount;
    }
    
    function complete(uint256 quotedAmount) external {
        // Executed at time T + bridgeDelay
        // Price may have moved significantly
        _mintTokens(msg.sender, quotedAmount);  // Stale!
    }
}
```

### Secure Implementation

**Fix: Slippage Protection and Price Guards**
```solidity
// ✅ SECURE: Slippage protection and deadlines
contract SecureSlippageBridge {
    function bridgeAndSwap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut,  // Slippage protection
        uint256 deadline       // Timing protection
    ) external {
        require(block.timestamp <= deadline, "Expired");
        
        _bridge(tokenIn, amountIn);
        
        // Pass slippage params to destination
        _sendSwapInstruction(tokenIn, tokenOut, amountIn, minAmountOut, deadline);
    }
    
    function completeSwap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut,
        uint256 deadline
    ) external {
        require(block.timestamp <= deadline, "Expired");
        
        uint256 amountOut = _swap(tokenIn, tokenOut, amountIn);
        require(amountOut >= minAmountOut, "Slippage too high");
        
        IERC20(tokenOut).transfer(msg.sender, amountOut);
    }
}
```

---

## 7. Message Ordering & Timing

### Overview

Cross-chain messages may arrive out of order or with significant delays. Protocols must handle these scenarios correctly.

### Vulnerable Pattern Examples

**Example 1: Order-Dependent State** [MEDIUM]
```solidity
// ❌ VULNERABLE: Assumes message order
contract OrderDependentBridge {
    mapping(uint256 => bool) public tokensMinted;
    
    function deposit(uint256 tokenId) external {
        _sendCrossChain(MINT_MESSAGE, tokenId);
    }
    
    function withdraw(uint256 tokenId) external {
        _sendCrossChain(BURN_MESSAGE, tokenId);
        // If BURN arrives before MINT, state is corrupted!
    }
}
```

### Secure Implementation

**Fix: Order-Independent State Machine**
```solidity
// ✅ SECURE: State machine handles any order
contract OrderIndependentBridge {
    enum TokenState { NotExists, Pending, Minted, Burned }
    mapping(uint256 => TokenState) public tokenStates;
    
    function processMint(uint256 tokenId) external {
        require(
            tokenStates[tokenId] == TokenState.NotExists ||
            tokenStates[tokenId] == TokenState.Pending,
            "Invalid state for mint"
        );
        tokenStates[tokenId] = TokenState.Minted;
        _mint(tokenId);
    }
    
    function processBurn(uint256 tokenId) external {
        if (tokenStates[tokenId] == TokenState.NotExists) {
            // Burn arrived before mint - queue it
            tokenStates[tokenId] = TokenState.Pending;
            pendingBurns[tokenId] = true;
            return;
        }
        
        require(tokenStates[tokenId] == TokenState.Minted, "Invalid state");
        tokenStates[tokenId] = TokenState.Burned;
        _burn(tokenId);
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: Signatures without chain ID (EIP-712 domain)
- Pattern 2: Message hashes without contract address
- Pattern 3: Global nonces instead of per-sender
- Pattern 4: Direct transfer amount usage (not measuring actual received)
- Pattern 5: No decimal normalization between tokens
- Pattern 6: Approvals not cleared after bridging
- Pattern 7: No slippage or deadline parameters
- Pattern 8: State machines assuming message ordering
- Pattern 9: Sequencer-dependent emergency functions
- Pattern 10: Signature tracking instead of message hash tracking
```

### Audit Checklist
- [ ] Verify signatures include chain ID and contract address
- [ ] Check nonces are per-sender and per-chain
- [ ] Confirm fee-on-transfer token handling
- [ ] Validate decimal normalization
- [ ] Test with rebasing tokens
- [ ] Verify slippage protection parameters
- [ ] Check approval clearing after bridges
- [ ] Test message ordering scenarios
- [ ] Verify sequencer-down handling for L2
- [ ] Check signature malleability protection

---

## Keywords for Search

`cross_chain`, `bridge`, `replay_attack`, `signature`, `nonce`, `chain_id`, `DOMAIN_SEPARATOR`, `EIP712`, `fee_on_transfer`, `rebasing`, `decimal`, `slippage`, `sequencer`, `L2`, `MEV`, `sandwich`, `front_run`, `approval`, `message_ordering`, `finality`

---

## Related Vulnerabilities

- [LayerZero Integration Issues](../layerzero/layerzero-integration-vulnerabilities.md)
- [Wormhole Integration Issues](../wormhole/wormhole-integration-vulnerabilities.md)
- [Hyperlane Integration Issues](../hyperlane/hyperlane-integration-vulnerabilities.md)

---

## DeFiHackLabs Real-World Exploits (8 incidents)

**Category**: Bridge | **Total Losses**: $1936.1M | **Sub-variants**: 3

### Sub-variant Breakdown

#### Bridge/Generic (6 exploits, $1245.1M)

- **Ronin Network** (2022-03, $624.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2022-03/Ronin_exp.sol`
- **Poly Network** (2021-08, $611.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2021-08/PolyNetwork_exp.sol`
- **Chainswap** (2021-07, $4.4M, bsc) | PoC: `DeFiHackLabs/src/test/2021-07/Chainswap_exp2.sol`
- *... and 3 more exploits*

#### Bridge/Modifier Bypass (1 exploits, $611.0M)

- **Poly Network** (2021-08, $611.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2021-08/PolyNetwork_exp.sol`

#### Bridge/Logic Flaw (1 exploits, $80.0M)

- **Qubit Finance** (2022-01, $80.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2022-01/Qubit_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| Ronin Network | 2022-03-29 | $624.0M | Bridge | ethereum |
| Poly Network | 2021-08-11 | $611.0M | Bridge, getting around modifier through cross-chain message | ethereum |
| Poly Network | 2021-08-11 | $611.0M | Bridge, getting around modifier through cross-chain message | ethereum |
| Qubit Finance | 2022-01-28 | $80.0M | Bridge address(0).safeTransferFrom() does not revert | ethereum |
| Chainswap | 2021-07-10 | $4.4M | Bridge, logic flaw | bsc |
| Meter | 2022-02-06 | $4.3M | Bridge | moonriver |
| Chainswap | 2021-07-02 | $800K | Bridge, logic flaw | ethereum |
| Li.Fi | 2022-03-20 | $570K | Bridges | ethereum |

### Top PoC References

- **Ronin Network** (2022-03, $624.0M): `DeFiHackLabs/src/test/2022-03/Ronin_exp.sol`
- **Poly Network** (2021-08, $611.0M): `DeFiHackLabs/src/test/2021-08/PolyNetwork_exp.sol`
- **Poly Network** (2021-08, $611.0M): `DeFiHackLabs/src/test/2021-08/PolyNetwork_exp.sol`
- **Qubit Finance** (2022-01, $80.0M): `DeFiHackLabs/src/test/2022-01/Qubit_exp.sol`
- **Chainswap** (2021-07, $4.4M): `DeFiHackLabs/src/test/2021-07/Chainswap_exp2.sol`
- **Meter** (2022-02, $4.3M): `DeFiHackLabs/src/test/2022-02/Meter_exp.sol`
- **Chainswap** (2021-07, $800K): `DeFiHackLabs/src/test/2021-07/Chainswap_exp1.sol`
- **Li.Fi** (2022-03, $570K): `DeFiHackLabs/src/test/2022-03/LiFi_exp.sol`
