---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bridge
vulnerability_type: ccip_integration

# Attack Vector Details (Required)
attack_type: message_validation|fee_miscalculation|token_pool_bypass|rate_limit_griefing
affected_component: Router|OnRamp|OffRamp|TokenPool|RateLimiter|Client

# Bridge-Specific Fields
bridge_provider: chainlink_ccip
bridge_attack_vector: router_validation|fee_estimation|token_pool_config|extra_args|lane_allowlist|manual_execution|rate_limiter

# Technical Primitives (Required)
primitives:
  - ccipReceive
  - ccipSend
  - Client.EVM2AnyMessage
  - Client.Any2EVMMessage
  - Router
  - OnRamp
  - OffRamp
  - TokenPool
  - RateLimiter
  - getFee
  - EVMExtraArgsV1
  - EVMExtraArgsV2
  - sourceChainSelector
  - messageId
  - tokenAmounts
  - allowlistEnabled
  - manuallyExecute
  - getRouter
  - i_router

# Impact Classification (Required)
severity: high
impact: fund_loss|message_replay|dos|token_stuck|fee_loss
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - defi
  - bridge
  - cross_chain
  - chainlink
  - ccip
  - token_pool
  - rate_limiter

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Router & Message Validation Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Axelar - Cross-Chain Call Revert | `reports/bridge_crosschain_findings/h-01-cross-chain-smart-contract-calls-can-revert-but-source-chain-tokens-remain-.md` | HIGH | Code4rena |
| Derby - Message Auth Bypass | `reports/bridge_crosschain_findings/h-6-cross-chain-message-authentication-can-be-bypassed-allowing-an-attacker-to-d.md` | HIGH | Sherlock |

### Fee & Gas Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Tradable - Fee Not Refunded | `reports/bridge_crosschain_findings/excessive-fee-is-not-refunded-to-the-user.md` | MEDIUM | Zokyo |
| Tesseract - Fixed Gas Limit | `reports/bridge_crosschain_findings/fixed-gas-limit-in-single-hop-transfers.md` | MEDIUM | OpenZeppelin |

### Token Pool & Rate Limit Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Securitize - Cap Inflation | `reports/bridge_crosschain_findings/bridging-dstoken-back-and-forth-between-chains-causes-totalissuance-cap-to-be-re.md` | MEDIUM | Cyfrin |
| Lucid Labs - Limits Bypass | `reports/bridge_crosschain_findings/bypass-of-bridge-limits-in-burnandbridgemulti-function.md` | HIGH | Halborn |

### External Links
- [Chainlink CCIP Documentation](https://docs.chain.link/ccip)
- [CCIP Best Practices](https://docs.chain.link/ccip/best-practices)
- [CCIP Architecture](https://docs.chain.link/ccip/architecture)
- [CCIP Supported Networks](https://docs.chain.link/ccip/supported-networks)

---

# Chainlink CCIP Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Chainlink CCIP Cross-Chain Security Audits**

---

## Table of Contents

1. [Router Message Validation](#1-router-message-validation)
2. [Fee Estimation Errors](#2-fee-estimation-errors)
3. [Token Pool Configuration](#3-token-pool-configuration)
4. [Extra Args & Gas Limit Misconfiguration](#4-extra-args--gas-limit-misconfiguration)
5. [Lane Allowlist Bypass](#5-lane-allowlist-bypass)
6. [Manual Execution Replay](#6-manual-execution-replay)
7. [Sender & Receiver Validation](#7-sender--receiver-validation)
8. [Rate Limiter Griefing](#8-rate-limiter-griefing)
9. [Off-Ramp Processing Failures](#9-off-ramp-processing-failures)
10. [Token Amount Validation](#10-token-amount-validation)
11. [Message Size Limit Violations](#11-message-size-limit-violations)
12. [Self-Service Token Registration Issues](#12-self-service-token-registration-issues)

---

## 1. Router Message Validation

### Overview

CCIP receivers implement `ccipReceive()` which is called by the CCIP Router. Failing to validate that only the Router can call this function allows arbitrary message injection. This is the most fundamental CCIP security requirement — the `ccipReceive` function MUST verify `msg.sender == i_router`.

### Vulnerability Description

#### Root Cause

Contracts implementing `IAny2EVMMessageReceiver` expose `ccipReceive()` as a public/external function but omit the critical `msg.sender == getRouter()` check, or fail to inherit from `CCIPReceiver` which provides this guard automatically.

#### Attack Scenario

1. Attacker identifies a CCIP receiver without router validation
2. Attacker calls `ccipReceive()` directly with forged `Client.Any2EVMMessage`
3. Forged message contains attacker-controlled `sender`, `sourceChainSelector`, and `data`
4. Receiver processes the fake message as if it came through CCIP
5. Attacker drains funds or corrupts state

### Vulnerable Pattern Examples

**Example 1: Missing Router Check on ccipReceive** [CRITICAL]
```solidity
// ❌ VULNERABLE: No msg.sender validation — anyone can call
contract VulnerableReceiver is IAny2EVMMessageReceiver {
    function ccipReceive(Client.Any2EVMMessage calldata message) external override {
        // Missing: require(msg.sender == address(router), "only router");
        
        address sender = abi.decode(message.sender, (address));
        (uint256 amount, address token) = abi.decode(message.data, (uint256, address));
        
        // Attacker forges message to mint/transfer tokens
        IERC20(token).transfer(sender, amount);
    }
}
```

**Example 2: Incorrect Router Stored as Mutable** [MEDIUM]
```solidity
// ❌ VULNERABLE: Router address can be changed to attacker-controlled contract
contract MutableRouterReceiver is CCIPReceiver {
    address public router;  // Shadow the immutable from CCIPReceiver!
    
    function setRouter(address _router) external onlyOwner {
        router = _router;  // Attacker front-runs to set malicious router
    }
    
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        // Uses the shadowed mutable router, not the immutable one
        _processMessage(message);
    }
}
```

### Secure Implementation

**Fix 1: Inherit from CCIPReceiver**
```solidity
// ✅ SECURE: CCIPReceiver enforces msg.sender == i_router
import {CCIPReceiver} from "@chainlink/contracts-ccip/src/v0.8/ccip/applications/CCIPReceiver.sol";

contract SecureReceiver is CCIPReceiver {
    constructor(address router) CCIPReceiver(router) {}
    
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        // Router validation already enforced by CCIPReceiver.ccipReceive()
        _processMessage(message);
    }
}
```

**Fix 2: Manual Router Validation**
```solidity
// ✅ SECURE: Manual check if not using CCIPReceiver base
contract ManualSecureReceiver is IAny2EVMMessageReceiver {
    address public immutable i_router;
    
    constructor(address router) {
        i_router = router;
    }
    
    modifier onlyRouter() {
        require(msg.sender == i_router, "Only router can call");
        _;
    }
    
    function ccipReceive(Client.Any2EVMMessage calldata message) external override onlyRouter {
        _processMessage(message);
    }
}
```

---

## 2. Fee Estimation Errors

### Overview

CCIP requires native token (or LINK) payment for cross-chain messages. The `Router.getFee()` function returns the required fee. If protocols don't properly estimate or pass fees, messages either fail to send or excess fees are lost.

### Vulnerable Pattern Examples

**Example 1: Hardcoded Fee Amount** [HIGH]
```solidity
// ❌ VULNERABLE: Hardcoded fee doesn't track actual CCIP costs
contract HardcodedFeeSender {
    uint256 constant CCIP_FEE = 0.1 ether;  // Will break when fees change!
    
    function sendMessage(uint64 destChain, bytes calldata data) external payable {
        require(msg.value >= CCIP_FEE, "Insufficient fee");
        
        Client.EVM2AnyMessage memory message = _buildMessage(data);
        
        // If actual fee > 0.1 ether, transaction reverts
        // If actual fee < 0.1 ether, excess is lost
        router.ccipSend{value: CCIP_FEE}(destChain, message);
    }
}
```

**Example 2: Fee Quoted But Not Validated Against msg.value** [MEDIUM]
```solidity
// ❌ VULNERABLE: getFee result not checked against msg.value
contract UnvalidatedFeeSender {
    function sendMessage(uint64 destChain, bytes calldata data) external payable {
        Client.EVM2AnyMessage memory message = _buildMessage(data);
        
        // Fee is quoted but never compared to msg.value!
        uint256 fee = router.getFee(destChain, message);
        
        // If msg.value < fee, ccipSend reverts with unclear error
        // If msg.value > fee, excess native tokens stuck in router
        router.ccipSend{value: msg.value}(destChain, message);
    }
}
```

**Example 3: LINK Payment Without Approval** [HIGH]
```solidity
// ❌ VULNERABLE: Paying with LINK but no approval to router
contract NoApprovalSender {
    function sendWithLink(uint64 destChain, bytes calldata data) external {
        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(destReceiver),
            data: data,
            tokenAmounts: new Client.EVMTokenAmount[](0),
            feeToken: address(linkToken),  // Pay in LINK
            extraArgs: ""
        });
        
        // Missing: linkToken.approve(address(router), fee);
        // Transaction reverts with transfer failure
        router.ccipSend(destChain, message);
    }
}
```

### Secure Implementation

**Fix 1: Dynamic Fee With Validation**
```solidity
// ✅ SECURE: Quote fee and validate payment
contract SecureFeeSender {
    IRouterClient public immutable router;
    
    function sendMessage(uint64 destChain, bytes calldata data) external payable {
        Client.EVM2AnyMessage memory message = _buildMessage(data);
        
        uint256 fee = router.getFee(destChain, message);
        require(msg.value >= fee, "Insufficient fee");
        
        router.ccipSend{value: fee}(destChain, message);
        
        // Refund excess
        if (msg.value > fee) {
            payable(msg.sender).transfer(msg.value - fee);
        }
    }
}
```

**Fix 2: LINK Payment With Proper Approval**
```solidity
// ✅ SECURE: Approve LINK before sending
contract SecureLinkSender {
    function sendWithLink(uint64 destChain, bytes calldata data) external {
        Client.EVM2AnyMessage memory message = _buildMessageWithLinkFee(data);
        
        uint256 fee = router.getFee(destChain, message);
        linkToken.transferFrom(msg.sender, address(this), fee);
        linkToken.approve(address(router), fee);
        
        router.ccipSend(destChain, message);
    }
}
```

---

## 3. Token Pool Configuration

### Overview

CCIP Token Pools handle the lock/release or burn/mint of tokens during cross-chain transfers. Misconfigured pools can lead to supply imbalance, stuck tokens, or unauthorized minting.

### Vulnerable Pattern Examples

**Example 1: Lock-Release Pool Without Balance Tracking** [HIGH]
```solidity
// ❌ VULNERABLE: No tracking of locked vs released amounts
contract VulnerableTokenPool {
    function lockTokens(address token, uint256 amount) external {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        // No tracking! Cannot verify release doesn't exceed locks
    }
    
    function releaseTokens(address token, address to, uint256 amount) external onlyBridge {
        // Can release more than locked if accounting is broken
        IERC20(token).transfer(to, amount);
    }
}
```

**Example 2: Burn-Mint Pool Without Supply Cap** [HIGH]
```solidity
// ❌ VULNERABLE: No mint cap enforcement
contract VulnerableBurnMintPool {
    IBurnMintERC20 public immutable token;
    
    function releaseOrMint(
        bytes memory,
        address receiver,
        uint256 amount,
        uint64,
        bytes memory
    ) external onlyOffRamp {
        // No supply cap check! Infinite minting possible if offRamp is compromised
        token.mint(receiver, amount);
    }
}
```

### Secure Implementation

**Fix: Proper Pool With Rate Limiting and Supply Tracking**
```solidity
// ✅ SECURE: Rate-limited pool with supply tracking
contract SecureTokenPool is TokenPool {
    uint256 public totalLocked;
    uint256 public immutable maxLockAmount;
    
    constructor(
        IERC20 token,
        address[] memory allowlist,
        address armProxy,
        address router,
        uint256 _maxLock
    ) TokenPool(token, allowlist, armProxy, router) {
        maxLockAmount = _maxLock;
    }
    
    function lockOrBurn(
        Pool.LockOrBurnInV1 calldata lockOrBurnIn
    ) external override returns (Pool.LockOrBurnOutV1 memory) {
        _validateLockOrBurn(lockOrBurnIn);
        
        totalLocked += lockOrBurnIn.amount;
        require(totalLocked <= maxLockAmount, "Exceeds max lock");
        
        // Apply rate limiting
        _consumeOutboundRateLimit(lockOrBurnIn.remoteChainSelector, lockOrBurnIn.amount);
        
        return Pool.LockOrBurnOutV1({
            destTokenAddress: getRemoteToken(lockOrBurnIn.remoteChainSelector),
            destPoolData: ""
        });
    }
}
```

---

## 4. Extra Args & Gas Limit Misconfiguration

### Overview

CCIP's `extraArgs` field controls gas limit and other execution parameters on the destination chain. Using wrong gas limits, wrong `extraArgs` version (V1 vs V2), or omitting `extraArgs` entirely causes message failures.

### Vulnerable Pattern Examples

**Example 1: Empty Extra Args — Default 200k Gas** [MEDIUM]
```solidity
// ❌ VULNERABLE: Empty extraArgs defaults to 200k gas
// Complex operations on destination may need more
Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
    receiver: abi.encode(destReceiver),
    data: abi.encode(complexOperation),  // Needs 500k+ gas!
    tokenAmounts: new Client.EVMTokenAmount[](0),
    feeToken: address(0),
    extraArgs: ""  // Defaults to 200,000 gas — insufficient!
});
```

**Example 2: EVMExtraArgsV1 vs V2 Confusion** [MEDIUM]
```solidity
// ❌ VULNERABLE: Using V1 when V2 is needed (missing strict sequencing control)
bytes memory extraArgs = Client._argsToBytes(
    Client.EVMExtraArgsV1({gasLimit: 500_000})
    // Missing: allowOutOfOrderExecution from V2
    // Default is strict ordering — messages can be stuck
);
```

**Example 3: Excessive Gas Limit Causes Fee Explosion** [LOW]
```solidity
// ❌ VULNERABLE: Extremely high gas wastes user funds
bytes memory extraArgs = Client._argsToBytes(
    Client.EVMExtraArgsV1({gasLimit: 10_000_000})  // 10M gas — fee is enormous
);
// User pays massive fee for gas that will never be used
```

### Secure Implementation

**Fix: Appropriate Gas With V2 Args**
```solidity
// ✅ SECURE: Right gas limit with V2 extra args
contract SecureExtraArgs {
    function _buildMessage(bytes memory data) internal view returns (Client.EVM2AnyMessage memory) {
        return Client.EVM2AnyMessage({
            receiver: abi.encode(destReceiver),
            data: data,
            tokenAmounts: new Client.EVMTokenAmount[](0),
            feeToken: address(0),
            extraArgs: Client._argsToBytes(
                Client.EVMExtraArgsV2({
                    gasLimit: _estimateGas(data),      // Dynamic based on data
                    allowOutOfOrderExecution: true       // Prevent message stuck
                })
            )
        });
    }
    
    function _estimateGas(bytes memory data) internal pure returns (uint256) {
        // Base cost + per-byte cost + operation overhead
        return 100_000 + (data.length * 68) + 200_000;
    }
}
```

---

## 5. Lane Allowlist Bypass

### Overview

CCIP implementations should restrict which source chains and senders can deliver messages. Missing allowlists let any chain or sender inject messages.

### Vulnerable Pattern Examples

**Example 1: No Source Chain Validation** [HIGH]
```solidity
// ❌ VULNERABLE: Accepts messages from ANY chain
contract NoChainAllowlist is CCIPReceiver {
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        // Missing: validate message.sourceChainSelector!
        // Attacker deploys on unsupported chain and sends fake messages
        
        address sender = abi.decode(message.sender, (address));
        _processPayload(sender, message.data);
    }
}
```

**Example 2: No Sender Allowlist** [HIGH]
```solidity
// ❌ VULNERABLE: Accepts from any sender on allowed chain
contract NoSenderAllowlist is CCIPReceiver {
    mapping(uint64 => bool) public allowedChains;
    
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        require(allowedChains[message.sourceChainSelector], "Chain not allowed");
        
        // Missing: validate message.sender!
        // Any contract on the allowed chain can send messages
        address sender = abi.decode(message.sender, (address));
        _processPayload(sender, message.data);
    }
}
```

### Secure Implementation

**Fix: Complete Chain + Sender Allowlist**
```solidity
// ✅ SECURE: Validate both chain and sender
contract SecureAllowlist is CCIPReceiver {
    mapping(uint64 => mapping(address => bool)) public allowedSenders;
    
    modifier onlyAllowlisted(uint64 sourceChainSelector, address sender) {
        require(allowedSenders[sourceChainSelector][sender], "Not allowlisted");
        _;
    }
    
    function setAllowedSender(
        uint64 chainSelector,
        address sender,
        bool allowed
    ) external onlyOwner {
        allowedSenders[chainSelector][sender] = allowed;
    }
    
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override
        onlyAllowlisted(
            message.sourceChainSelector,
            abi.decode(message.sender, (address))
        )
    {
        _processPayload(message);
    }
}
```

---

## 6. Manual Execution Replay

### Overview

CCIP supports manual execution of failed messages via the OffRamp. If the receiver doesn't properly handle replay protection, a manually executed message can be processed multiple times.

### Vulnerable Pattern Examples

**Example 1: No Message ID Tracking** [HIGH]
```solidity
// ❌ VULNERABLE: Same message can be manually executed multiple times
contract NoReplayProtection is CCIPReceiver {
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        // No tracking of message.messageId!
        (address recipient, uint256 amount) = abi.decode(message.data, (address, uint256));
        
        // If ccipReceive reverts and is manually executed,
        // tokens can be minted multiple times
        token.mint(recipient, amount);
    }
}
```

### Secure Implementation

**Fix: Track Processed Message IDs**
```solidity
// ✅ SECURE: Idempotent message processing
contract SecureReplayProtection is CCIPReceiver {
    mapping(bytes32 => bool) public processedMessages;
    
    // Failed messages stored for recovery
    mapping(bytes32 => Client.Any2EVMMessage) public failedMessages;
    
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        require(!processedMessages[message.messageId], "Already processed");
        processedMessages[message.messageId] = true;
        
        try this.processMessage(message) {
            // Success
        } catch {
            failedMessages[message.messageId] = message;
            processedMessages[message.messageId] = false;  // Allow retry
            emit MessageFailed(message.messageId);
        }
    }
    
    function retryFailedMessage(bytes32 messageId) external onlyOwner {
        Client.Any2EVMMessage memory message = failedMessages[messageId];
        require(message.messageId != bytes32(0), "No failed message");
        
        delete failedMessages[messageId];
        processedMessages[messageId] = true;
        
        this.processMessage(message);
    }
}
```

---

## 7. Sender & Receiver Validation

### Overview

CCIP messages contain `sender` (as `bytes` for cross-chain compatibility) and `sourceChainSelector`. Incorrect decoding or validation of these fields enables message spoofing.

### Vulnerable Pattern Examples

**Example 1: Wrong Sender Decoding** [HIGH]
```solidity
// ❌ VULNERABLE: Incorrect sender decoding
contract WrongSenderDecode is CCIPReceiver {
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        // WRONG: This truncates if sender is from non-EVM chain
        address sender = address(bytes20(message.sender));
        
        // Should use: address sender = abi.decode(message.sender, (address));
        _processWithSender(sender, message.data);
    }
}
```

**Example 2: Receiver Set to EOA for Token Transfers** [MEDIUM]
```solidity
// ❌ VULNERABLE: Sending tokens + data to receiver that can't handle both
contract BadReceiverConfig {
    function sendTokensWithData(uint64 destChain, address eoaReceiver) external payable {
        Client.EVMTokenAmount[] memory tokenAmounts = new Client.EVMTokenAmount[](1);
        tokenAmounts[0] = Client.EVMTokenAmount({token: address(usdc), amount: 1000e6});
        
        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(eoaReceiver),  // EOA can't implement ccipReceive!
            data: abi.encode(someInstruction),    // Data will be lost
            tokenAmounts: tokenAmounts,
            feeToken: address(0),
            extraArgs: ""
        });
        
        // Tokens sent to EOA but data/instructions not executable
        router.ccipSend{value: msg.value}(destChain, message);
    }
}
```

### Secure Implementation

**Fix: Proper Sender Validation**
```solidity
// ✅ SECURE: Validate sender format and content
contract SecureSenderValidation is CCIPReceiver {
    mapping(uint64 => bytes) public expectedSenders;
    
    function setExpectedSender(uint64 chain, address sender) external onlyOwner {
        expectedSenders[chain] = abi.encode(sender);
    }
    
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        bytes memory expected = expectedSenders[message.sourceChainSelector];
        require(expected.length > 0, "Chain not configured");
        require(
            keccak256(message.sender) == keccak256(expected),
            "Unauthorized sender"
        );
        
        _processPayload(message);
    }
}
```

---

## 8. Rate Limiter Griefing

### Overview

CCIP includes configurable rate limiters on token pools. Attackers can exploit rate limits to DoS legitimate transfers by filling the rate limit bucket with small transfers.

### Vulnerable Pattern Examples

**Example 1: No Per-User Rate Limiting** [MEDIUM]
```solidity
// ❌ VULNERABLE: Global rate limit shared by all users
contract GlobalRateLimitPool {
    uint256 public constant RATE_LIMIT = 1_000_000e18;  // Per period
    uint256 public currentPeriodAmount;
    
    function lockTokens(uint256 amount) external {
        currentPeriodAmount += amount;
        require(currentPeriodAmount <= RATE_LIMIT, "Rate limited");
        
        // Attacker fills the entire limit with dust transfers
        // Legitimate users blocked for the entire period
    }
}
```

### Secure Implementation

**Fix: Per-User Limits With Priority Queue**
```solidity
// ✅ SECURE: Tiered rate limiting
contract TieredRateLimitPool {
    struct UserLimit {
        uint256 used;
        uint256 lastReset;
    }
    
    uint256 public globalLimit;
    uint256 public perUserLimit;
    uint256 public period;
    
    mapping(address => UserLimit) public userLimits;
    
    function lockTokens(address user, uint256 amount) external {
        _resetIfNeeded(user);
        
        userLimits[user].used += amount;
        require(userLimits[user].used <= perUserLimit, "User rate limited");
        
        globalUsed += amount;
        require(globalUsed <= globalLimit, "Global rate limited");
    }
}
```

---

## 9. Off-Ramp Processing Failures

### Overview

When `ccipReceive` reverts on the destination chain, the message enters a failed state in the OffRamp. Without proper error handling, tokens sent with the message can be permanently stuck.

### Vulnerable Pattern Examples

**Example 1: Reverting ccipReceive With Token Transfers** [HIGH]
```solidity
// ❌ VULNERABLE: Revert causes tokens to be stuck in receiver contract
contract RevertingReceiver is CCIPReceiver {
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        // Tokens are already transferred to this contract by CCIP
        
        (address target, bytes memory callData) = abi.decode(message.data, (address, bytes));
        
        // If this external call reverts, the entire ccipReceive reverts
        // Tokens are stuck in this contract with no recovery path
        (bool success,) = target.call(callData);
        require(success, "External call failed");  // DANGEROUS: causes full revert
    }
}
```

### Secure Implementation

**Fix: Graceful Error Handling With Token Recovery**
```solidity
// ✅ SECURE: Never revert, store failed messages for recovery
contract GracefulReceiver is CCIPReceiver, Ownable {
    enum ErrorCode { RESOLVED, FAILED }
    
    struct FailedMessage {
        bytes32 messageId;
        ErrorCode errorCode;
    }
    
    mapping(bytes32 => FailedMessage) public failedMessages;
    
    event MessageFailed(bytes32 indexed messageId, bytes reason);
    event MessageRecovered(bytes32 indexed messageId);
    
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        try this.processMessage(message) {
            // Success
        } catch (bytes memory reason) {
            // Store for recovery — tokens are safe in this contract
            failedMessages[message.messageId] = FailedMessage(
                message.messageId,
                ErrorCode.FAILED
            );
            emit MessageFailed(message.messageId, reason);
        }
    }
    
    function retryFailedMessage(
        bytes32 messageId,
        address tokenReceiver
    ) external onlyOwner {
        FailedMessage storage fm = failedMessages[messageId];
        require(fm.errorCode == ErrorCode.FAILED, "Not failed");
        
        fm.errorCode = ErrorCode.RESOLVED;
        
        // Transfer stuck tokens to intended recipient
        // Application-specific recovery logic
        emit MessageRecovered(messageId);
    }
}
```

---

## 10. Token Amount Validation

### Overview

CCIP messages can include `tokenAmounts` for cross-chain token transfers. Mismatches between expected and actual token amounts lead to accounting errors.

### Vulnerable Pattern Examples

**Example 1: Not Validating Received Token Amounts** [HIGH]
```solidity
// ❌ VULNERABLE: Trusts message.data instead of actual tokenAmounts
contract TrustingReceiver is CCIPReceiver {
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        // Decodes expected amount from data — NOT actual received amount
        (address recipient, uint256 expectedAmount) = abi.decode(
            message.data, (address, uint256)
        );
        
        // Should check message.destTokenAmounts[0].amount instead!
        // The actual received amount may differ due to fees, rate limiting
        _creditUser(recipient, expectedAmount);  // May not match reality
    }
}
```

### Secure Implementation

**Fix: Use Actual Token Amounts**
```solidity
// ✅ SECURE: Validate against actual received tokens
contract SecureTokenValidation is CCIPReceiver {
    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        require(message.destTokenAmounts.length == 1, "Expected 1 token");
        
        address receivedToken = message.destTokenAmounts[0].token;
        uint256 receivedAmount = message.destTokenAmounts[0].amount;
        
        require(receivedToken == address(expectedToken), "Wrong token");
        require(receivedAmount > 0, "Zero amount");
        
        address recipient = abi.decode(message.data, (address));
        _creditUser(recipient, receivedAmount);  // Use actual amount
    }
}
```

---

## 11. Message Size Limit Violations

### Overview

CCIP enforces maximum data sizes per message. Exceeding limits causes silent failures during `ccipSend`. Protocols that dynamically build payloads must validate size before sending.

### Vulnerable Pattern Examples

**Example 1: Unbounded Payload Construction** [MEDIUM]
```solidity
// ❌ VULNERABLE: No size check on dynamically built payload
contract UnboundedPayload {
    function sendBatchOperation(
        uint64 destChain,
        address[] calldata targets,
        bytes[] calldata callDatas
    ) external payable {
        // Payload grows linearly with array length — can exceed CCIP max
        bytes memory data = abi.encode(targets, callDatas);
        
        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(destReceiver),
            data: data,  // May exceed maxDataBytes!
            tokenAmounts: new Client.EVMTokenAmount[](0),
            feeToken: address(0),
            extraArgs: ""
        });
        
        // Reverts with unclear error if data too large
        router.ccipSend{value: msg.value}(destChain, message);
    }
}
```

### Secure Implementation

**Fix: Validate Payload Size**
```solidity
// ✅ SECURE: Check size before sending
contract BoundedPayload {
    uint256 public constant MAX_CCIP_DATA_LENGTH = 50_000;  // Check CCIP docs for current limit
    
    function sendBatchOperation(
        uint64 destChain,
        address[] calldata targets,
        bytes[] calldata callDatas
    ) external payable {
        bytes memory data = abi.encode(targets, callDatas);
        require(data.length <= MAX_CCIP_DATA_LENGTH, "Payload too large");
        
        Client.EVM2AnyMessage memory message = _buildMessage(data);
        
        uint256 fee = router.getFee(destChain, message);
        require(msg.value >= fee, "Insufficient fee");
        
        router.ccipSend{value: fee}(destChain, message);
    }
}
```

---

## 12. Self-Service Token Registration Issues

### Overview

CCIP allows protocols to register their own tokens for cross-chain transfer via the Token Admin Registry. Incorrect configuration leads to supply imbalance across chains.

### Vulnerable Pattern Examples

**Example 1: Lock-Release on Both Chains** [CRITICAL]
```solidity
// ❌ VULNERABLE: Lock-release pool on BOTH chains means no burn/mint
// Total circulating supply doubles with each bridge cycle!
// Chain A: Lock 100 tokens → Chain B: Release 100 tokens
// Chain B: Lock 100 tokens → Chain A: Release 100 tokens
// Now 200 tokens circulating but only 100 should exist per chain
```

**Example 2: Burn-Mint Without Supply Coordination** [HIGH]
```solidity
// ❌ VULNERABLE: No flow limit means entire supply can migrate to one chain
contract UnlimitedBurnMintPool {
    function releaseOrMint(
        bytes memory,
        address receiver,
        uint256 amount,
        uint64,
        bytes memory
    ) external onlyOffRamp {
        // No per-chain supply limit
        // Entire token supply can be concentrated on one chain
        token.mint(receiver, amount);
    }
}
```

### Secure Implementation

**Fix: Lock-Release on Home Chain, Burn-Mint Everywhere Else**
```solidity
// ✅ SECURE: Correct pool type per chain
// Home chain (where token is native): Lock-Release pool
// All other chains: Burn-Mint pool
// This ensures conservation of total supply

// Additionally, configure flow limits per chain:
// - Outbound: Maximum tokens that can leave per period
// - Inbound: Maximum tokens that can arrive per period
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: ccipReceive without msg.sender == router check
- Pattern 2: Hardcoded fee values instead of router.getFee()
- Pattern 3: Empty extraArgs (defaults to 200k gas)
- Pattern 4: EVMExtraArgsV1 when V2 is needed
- Pattern 5: No sourceChainSelector validation in _ccipReceive
- Pattern 6: No sender validation in _ccipReceive
- Pattern 7: Missing messageId replay protection
- Pattern 8: require/revert in _ccipReceive without try-catch
- Pattern 9: Trusting message.data amounts instead of destTokenAmounts
- Pattern 10: Lock-release pools on multiple chains for same token
- Pattern 11: No LINK approval before ccipSend with LINK fee
- Pattern 12: Unbounded payload construction without size check
```

### Audit Checklist
- [ ] Verify ccipReceive validates msg.sender == router (or inherits CCIPReceiver)
- [ ] Check fee estimation uses router.getFee() dynamically
- [ ] Ensure extraArgs includes appropriate gas limit for destination operations
- [ ] Validate source chain selector allowlist
- [ ] Validate sender address allowlist per chain
- [ ] Check for message ID replay protection
- [ ] Verify _ccipReceive uses try-catch for external calls
- [ ] Ensure token amounts validated against destTokenAmounts, not message data
- [ ] Verify correct pool type per chain (lock-release vs burn-mint)
- [ ] Check rate limiter configuration prevents griefing
- [ ] Validate LINK approval flow if paying fees in LINK
- [ ] Check payload size against CCIP limits

---

## Keywords for Search

`ccip`, `ccipReceive`, `ccipSend`, `chainlink`, `Router`, `OnRamp`, `OffRamp`, `TokenPool`, `Client.EVM2AnyMessage`, `Client.Any2EVMMessage`, `getFee`, `EVMExtraArgsV1`, `EVMExtraArgsV2`, `sourceChainSelector`, `messageId`, `tokenAmounts`, `destTokenAmounts`, `allowlist`, `RateLimiter`, `manuallyExecute`, `CCIPReceiver`, `i_router`, `getRouter`, `cross_chain`, `bridge`, `token_pool`, `burn_mint`, `lock_release`, `fee_estimation`, `message_replay`, `lane_config`

---

## Related Vulnerabilities

- [LayerZero Integration Issues](../layerzero/layerzero-integration-vulnerabilities.md)
- [Wormhole Integration Issues](../wormhole/wormhole-integration-vulnerabilities.md)
- [Cross-Chain General Vulnerabilities](../custom/cross-chain-general-vulnerabilities.md)
- [Axelar Integration Issues](../axelar/axelar-integration-vulnerabilities.md)
