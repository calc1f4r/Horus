---
# Core Classification
protocol: generic
chain: ethereum, bsc, polygon, multi-chain
category: bridge
vulnerability_type: cross_chain_access_control_bypass

# Pattern Identity
root_cause_family: missing_access_control
pattern_key: unrestricted_cross_chain_target | bridge_executor | privileged_call | validator_takeover

# Interaction Scope
interaction_scope: cross_chain
involved_contracts:
  - EthCrossChainManager
  - EthCrossChainData
  - ChainswapBridge
  - LockProxy
path_keys:
  - unrestricted_cross_chain_target | verifyHeaderAndExecuteTx | EthCrossChainManager -> EthCrossChainData -> LockProxy
  - self_referential_keeper | receive | ChainswapBridge.addKeeper -> ChainswapBridge.receive
  - missing_replay_protection | receive | ChainswapBridge.receive

# Attack Vector Details
attack_type: logical_error
affected_component: cross_chain_messenger, signature_verification, keeper_management

# Technical Primitives
primitives:
  - cross_chain_target_bypass
  - self_referential_signature
  - relay_verification_bypass
  - keeper_privilege_escalation
  - validator_key_replacement
  - signature_replay

# Grep / Hunt-Card Seeds
code_keywords:
  - verifyHeaderAndExecuteTx
  - executeCrossChainTx
  - putCurEpochConPubKeyBytes
  - onlyOwner
  - addKeeper
  - onlyKeeper
  - keepers
  - ecrecover
  - abi.encodePacked
  - toEthSignedMessageHash
  - DOMAIN_SEPARATOR
  - block.chainid
  - allowedTargets

# Impact Classification
severity: critical
impact: fund_loss
exploitability: 0.7
financial_impact: critical

# Context Tags
tags:
  - bridge
  - cross_chain
  - access_control
  - signature
  - relay
  - keeper
  - validator
  - DeFiHackLabs

# Version Info
language: solidity
version: ">=0.6.0"
---

## References & Source Reports

| Label | Source | Path / URL | Severity | Loss |
|-------|--------|------------|----------|------|
| [POLY-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-08/PolyNetwork_exp.sol` | CRITICAL | $611M |
| [CS2-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-07/Chainswap_exp2.sol` | CRITICAL | $4.4M |
| [CS1-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-07/Chainswap_exp1.sol` | HIGH | $0.8M |

---

# Cross-Chain Bridge Access Control Bypass Patterns (2021)

## Overview

Cross-chain bridge exploits from 2021 totaling **$617M+ in losses** through two core access-control failures: (1) unrestricted cross-chain message targets that allow calling privileged contracts to replace validator keys (Poly Network $611M), and (2) self-referential signature schemes where a keeper can add more keepers and sign arbitrary mints (Chainswap $5.2M).

### Agent Quick View

- Root cause statement: "This vulnerability exists because bridge executors place no restrictions on which contracts can be called via cross-chain messages, or because keeper/signer management is self-referential — a single compromised keeper can escalate to full bridge control."
- Pattern key: `unrestricted_cross_chain_target | bridge_executor | privileged_call | validator_takeover`
- Interaction scope: `cross_chain`
- Primary affected component(s): `cross-chain message executor, keeper registry, signature verification`
- Contracts / modules involved: `EthCrossChainManager, EthCrossChainData, LockProxy, ChainswapBridge`
- Path keys: `unrestricted_cross_chain_target | verifyHeaderAndExecuteTx | EthCrossChainManager -> EthCrossChainData -> LockProxy`; `self_referential_keeper | receive | ChainswapBridge.addKeeper -> ChainswapBridge.receive`
- High-signal code keywords: `verifyHeaderAndExecuteTx, executeCrossChainTx, putCurEpochConPubKeyBytes, addKeeper, onlyKeeper, ecrecover`
- Typical sink / impact: `validator key replacement → unlimited cross-chain drain; arbitrary token minting`
- Validation strength: `strong`

### Contract / Boundary Map

- Entry surface(s): `verifyHeaderAndExecuteTx()`, `receive()`, `addKeeper()`
- Contract hop(s): `EthCrossChainManager._executeCrossChainTx -> EthCrossChainData.putCurEpochConPubKeyBytes`; `ChainswapBridge.receive -> mint`
- Trust boundary crossed: `cross-chain message verification → privileged keeper registry`; `single keeper → keeper management`
- Shared state or sync assumption: `EthCrossChainData.ConKeepersPkBytes must only be updated through governance, not through cross-chain messages`; `keeper addition must not be self-referential`

### Valid Bug Signals

- Signal 1: Cross-chain executor can call ANY contract address including the keeper/validator registry that it owns
- Signal 2: The keeper registry contract is owned by the cross-chain executor contract (ownership chain creates the vulnerability)
- Signal 3: Keepers can add other keepers without governance/timelock — self-referential authorization
- Signal 4: Signature hash does not include `chainId` or `address(this)` — cross-chain replay is possible

### False Positive Guards

- Not this bug when: The cross-chain executor has a strict target whitelist that excludes all privileged contracts
- Safe if: Keeper management requires governance vote or timelock with M-of-N threshold higher than the bridge signing threshold
- Safe if: Signature hashes include `chainId`, `address(this)` (EIP-712), and have proper nonce management
- Requires attacker control of: At least one valid cross-chain message submission path (Path A), or one compromised keeper key (Path B/C)

---

## Vulnerability Description

### Root Cause

Two distinct access-control failures in bridge architectures:

1. **Unrestricted cross-chain message targets**: The bridge executor contract (`EthCrossChainManager`) can call ANY contract, including the keeper registry (`EthCrossChainData`) that it owns. Since the executor is the owner of the registry, a crafted cross-chain message can replace all validator keys.

2. **Self-referential keeper management**: Bridge keeper/signer operations verify against a keeper set that keepers themselves can modify. A single compromised keeper can add attacker-controlled keepers, then sign arbitrary mint/transfer messages.

### Attack Scenario / Path Variants

**Path A: Cross-Chain Validator Key Replacement (Poly Network — $611M)** [CRITICAL]
Path key: `unrestricted_cross_chain_target | verifyHeaderAndExecuteTx | EthCrossChainManager -> EthCrossChainData -> LockProxy`
Entry surface: `EthCrossChainManager.verifyHeaderAndExecuteTx()` — callable by anyone
Contracts touched: `EthCrossChainManager -> EthCrossChainData.putCurEpochConPubKeyBytes -> LockProxy.unlock`
Boundary crossed: `cross-chain message → privileged keeper registry (owned by executor)`
pathShape: `staged`

Setup (staging):
1. Analyze EthCrossChainManager — discover it has no target whitelist for `_executeCrossChainTx`
2. Discover EthCrossChainData is OWNED by EthCrossChainManager — so cross-chain calls pass `onlyOwner`
3. Craft a Poly chain transaction targeting `EthCrossChainData.putCurEpochConPubKeyBytes()` with attacker's key

Firing:
4. Submit the cross-chain message to `verifyHeaderAndExecuteTx()` on Ethereum
5. Manager verifies the Poly chain header signature, extracts the message payload
6. Manager calls `_executeCrossChainTx(EthCrossChainData, "putCurEpochConPubKeyBytes", attacker_pubkey)` — succeeds because Manager is owner
7. All validator keys now replaced with attacker's key
8. Attacker signs arbitrary `LockProxy.unlock()` messages across Ethereum, BSC, and Polygon → drains $611M

**Path B: Self-Referential Keeper Escalation (Chainswap v2 — $4.4M)** [CRITICAL]
Path key: `self_referential_keeper | receive | ChainswapBridge.addKeeper -> ChainswapBridge.receive`
Entry surface: `ChainswapBridge.addKeeper()` — callable by any keeper
Contracts touched: `ChainswapBridge.addKeeper -> ChainswapBridge.receive -> IMappableToken.mint`
Boundary crossed: `keeper set → keeper management (self-referential)`
pathShape: `staged`

Setup (staging):
1. Compromise ONE keeper key (or exploit the keeper addition flow)
2. Call `addKeeper()` to register multiple attacker-controlled addresses as keepers

Firing:
3. Sign arbitrary `receive()` messages specifying bridged tokens and amounts
4. Each call mints bridged tokens to attacker → $4.4M drained across multiple token types

**Path C: Missing Replay Protection in Signature (Chainswap v1 — $0.8M)** [HIGH]
Path key: `missing_replay_protection | receive | ChainswapBridge.receive`
Entry surface: `ChainswapBridge.receive()` — callable by anyone with valid signature
Contracts touched: `ChainswapBridge.receive -> IERC20.transfer`
Boundary crossed: `signature verification`
pathShape: `atomic`

1. Signature hash uses `keccak256(abi.encodePacked(token, to, amount, nonce))` — missing `chainId` and `address(this)`
2. Valid signatures can be replayed across chains and contracts
3. Weak nonce management allows reuse with predictable increments
4. With one leaked keeper key, unlimited valid signatures can be forged

### Vulnerable Pattern Examples

**Example 1: Poly Network — Unrestricted Cross-Chain Executor Target ($611M)** [Approx Vulnerability: CRITICAL] `@audit` [POLY-POC]

```solidity
// ❌ VULNERABLE: EthCrossChainManager can execute on ANY target contract
// Including EthCrossChainData which stores the keeper (validator) list

contract EthCrossChainManager {
    function _executeCrossChainTx(
        address _toContract,   // @audit No whitelist — can be EthCrossChainData!
        bytes memory _method,  // @audit Can be putCurEpochConPubKeyBytes!
        bytes memory _args,    // @audit Can be attacker's public key!
        bytes memory _fromContract,
        uint64 _fromChainId
    ) internal returns (bool) {
        // @audit Calls _toContract._method(_args) with NO target restriction
        (bool success, bytes memory result) = _toContract.call(
            abi.encodePacked(
                bytes4(keccak256(abi.encodePacked(_method, "(bytes,bytes,uint64)"))),
                abi.encode(_args, _fromContract, _fromChainId)
            )
        );
        return success;
    }
}

// The privileged contract that stores keepers — OWNED by EthCrossChainManager:
contract EthCrossChainData {
    function putCurEpochConPubKeyBytes(bytes memory curEpochPkBytes) public onlyOwner {
        ConKeepersPkBytes = curEpochPkBytes;
        // @audit onlyOwner passes because EthCrossChainManager IS the owner
    }
}

// PoC flow from actual exploit (block 12,996,658):
// 1. Crafted Poly chain message: toContract=EthCrossChainData, method="f1121318093"
//    (4-byte selector collision with putCurEpochConPubKeyBytes(bytes,bytes,uint64))
// 2. args = attacker's public key (0xa87fb85a93ca072cd4e5f0d4f178bc831df8a00b)
// 3. verifyHeaderAndExecuteTx() processes it → replaces all validators
// 4. Second tx calls LockProxy.unlock() with attacker-signed header → drains ETH
```

**Example 2: Chainswap v2 — Keeper Self-Addition ($4.4M)** [Approx Vulnerability: CRITICAL] `@audit` [CS2-POC]

```solidity
// ❌ VULNERABLE: A single compromised keeper can add more keeper addresses
// then sign arbitrary mint messages for any bridged token

contract ChainswapBridgeV2 {
    mapping(address => bool) public keepers;

    function receive(
        uint256[] memory amounts,
        address[] memory tokens,
        address to,
        uint256 nonce,
        uint256 fromChainId,
        bytes memory signature
    ) external {
        bytes32 hash = keccak256(abi.encodePacked(amounts, tokens, to, nonce, fromChainId));
        address signer = hash.toEthSignedMessageHash().recover(signature);
        require(keepers[signer], "not a keeper");

        for (uint256 i = 0; i < tokens.length; i++) {
            IMappableToken(tokens[i]).mint(to, amounts[i]);
            // @audit Mints arbitrary amounts of any bridged token
        }
    }

    // @audit CRITICAL: Keepers can add keepers — self-referential!
    function addKeeper(address keeper) external onlyKeeper {
        keepers[keeper] = true;
    }
}

// PoC: Single signature from keeper 0xF1790Ac4... mints 500,000 tokens on BSC (block 9,042,274)
```

**Example 3: Chainswap v1 — Missing chainId in Signature Hash ($0.8M)** [Approx Vulnerability: HIGH] `@audit` [CS1-POC]

```solidity
// ❌ VULNERABLE: Signature hash does not include chainId or contract address
// enabling cross-chain and cross-contract replay

contract ChainswapBridgeV1 {
    function receive(
        uint256 fromChainId,
        address to,
        uint256 nonce,
        uint256 volume,
        Signature[] memory signatures
    ) external payable {
        for (uint i = 0; i < signatures.length; i++) {
            bytes32 structHash = keccak256(abi.encode(
                RECEIVE_TYPEHASH, fromChainId, to, nonce, volume,
                signatures[i].signatory
            ));
            bytes32 digest = keccak256(abi.encodePacked("\x19\x01", _DOMAIN_SEPARATOR, structHash));
            address signatory = ecrecover(digest, signatures[i].v, signatures[i].r, signatures[i].s);
            require(signatory == signatures[i].signatory, "unauthorized");
            // @audit _DOMAIN_SEPARATOR may not include chainId — cross-chain replay
            // @audit Signer self-asserts identity, no check against keeper set
            _decreaseAuthQuota(signatures[i].signatory, volume);
        }
    }
}

// PoC: 4 signatures from known keepers used to withdraw 19,392 tokens (block 12,751,487)
// The same signature set could potentially be replayed on other chains
```

---

## Impact Analysis

### Technical Impact
- Complete bridge takeover via validator key replacement (Poly Network) — attacker controls all message validation
- Multi-chain cascade: a single Ethereum exploit drains BSC and Polygon simultaneously
- Self-referential keeper systems convert a single key compromise into unlimited minting authority

### Business Impact

| Protocol | Date | Loss | Root Cause |
|----------|------|------|------------|
| Poly Network | Aug 2021 | $611M | Unrestricted cross-chain executor targets keeper registry |
| Chainswap v2 | Jul 2021 | $4.4M | Keeper can add other keepers + sign arbitrary mints |
| Chainswap v1 | Jul 2021 | $0.8M | Missing chainId in signature hash, self-asserted signer identity |

### Affected Scenarios
- Any bridge where the cross-chain executor can call its own data/configuration contracts
- Bridges where the executor contract is the owner of the validator registry
- Single-keeper or low-threshold keeper systems with self-referential management
- Bridges using `abi.encodePacked` for signatures without `chainId` and `address(this)`

---

## Secure Implementation

**Fix 1: Whitelist Cross-Chain Executor Targets**
```solidity
// ✅ SECURE: Restrict which contracts can be called via cross-chain messages
contract SecureCrossChainManager {
    mapping(address => bool) public allowedTargets;

    function executeCrossChainTx(address target, bytes memory data) internal {
        require(allowedTargets[target], "target not whitelisted");
        // @audit NEVER allow targeting the keeper/validator management contract
        require(target != address(crossChainData), "cannot target data contract");
        (bool success,) = target.call(data);
        require(success, "execution failed");
    }
}
```

**Fix 2: Governance-Controlled Keeper Management + Multi-Sig**
```solidity
// ✅ SECURE: Require M-of-N signatures and governance-only keeper management
contract SecureBridge {
    uint256 public constant REQUIRED_SIGS = 3;

    function receive(
        address token, address to, uint256 amount,
        uint256 nonce, uint256 fromChainId,
        bytes[] memory signatures
    ) external {
        require(signatures.length >= REQUIRED_SIGS, "insufficient sigs");

        bytes32 hash = keccak256(abi.encodePacked(
            token, to, amount, nonce, fromChainId,
            block.chainid,     // @audit Include target chainId
            address(this)      // @audit Include contract address
        ));

        address[] memory signers = new address[](signatures.length);
        for (uint i = 0; i < signatures.length; i++) {
            signers[i] = hash.toEthSignedMessageHash().recover(signatures[i]);
            require(keepers[signers[i]], "not a keeper");
            for (uint j = 0; j < i; j++) {
                require(signers[j] != signers[i], "duplicate signer");
            }
        }
        IERC20(token).transfer(to, amount);
    }

    // @audit Keeper management requires governance, NOT keeper self-addition
    function addKeeper(address keeper) external onlyGovernance {
        keepers[keeper] = true;
    }
}
```

**Fix 3: EIP-712 Typed Signatures**
```solidity
// ✅ SECURE: EIP-712 prevents cross-chain and cross-contract replay
bytes32 public immutable DOMAIN_SEPARATOR;

constructor() {
    DOMAIN_SEPARATOR = keccak256(abi.encode(
        keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
        keccak256("SecureBridge"),
        keccak256("1"),
        block.chainid,     // @audit Chain-specific
        address(this)      // @audit Contract-specific
    ));
}
```

---

## Detection Patterns

### Contract / Call Graph Signals
```
- Cross-chain executor that can call ANY contract via .call() without a target whitelist
- Executor contract is the owner of the validator/keeper registry it protects
- Keeper management functions gated by onlyKeeper (self-referential)
- Signature hashes using abi.encodePacked without chainId and address(this)
```

### High-Signal Grep Seeds
```
- verifyHeaderAndExecuteTx
- executeCrossChainTx
- putCurEpochConPubKeyBytes
- addKeeper AND onlyKeeper
- ConKeepersPkBytes
- ecrecover
- DOMAIN_SEPARATOR
- abi.encodePacked.*signature
```

### Code Patterns to Look For
```
- Bridge executor .call() with unconstrained target address
- onlyOwner modifier where owner is the cross-chain executor
- keeper/signer self-addition: addKeeper() WITH onlyKeeper modifier
- Signature hash missing chainId or address(this)
- Signer identity self-assertion (signatory == signatures[i].signatory)
```

### Audit Checklist
- [ ] Can the cross-chain executor call ANY contract? → Must have a target whitelist
- [ ] Is the keeper/validator registry callable via cross-chain messages? → NEVER allow this
- [ ] Can keepers add other keepers? → Self-referential = single point of failure
- [ ] Does the signature hash include `chainId` AND `address(this)`? → Both required
- [ ] How many valid signatures are required? → Single-sig bridges are extremely high risk
- [ ] What happens if one keeper key is compromised? → Should not enable full bridge takeover

---

## Real-World Examples

### Known Exploits
- **Poly Network** — Cross-chain executor targets keeper registry, replaces all validator keys — Aug 2021 — $611M
  - Link: https://rekt.news/polynetwork-rekt/
  - Root cause: EthCrossChainManager owned EthCrossChainData; no target whitelist on `_executeCrossChainTx`
- **Chainswap v2** — Keeper can add new keepers + sign arbitrary mints — Jul 2021 — $4.4M
  - Link: https://rekt.news/chainswap-rekt/
  - Root cause: `addKeeper()` gated by `onlyKeeper` — single compromised key escalates to full control
- **Chainswap v1** — Missing chainId in signature, self-asserted signer identity — Jul 2021 — $0.8M
  - Root cause: `ecrecover` result compared against signer-supplied address, not a keeper registry

### Related Entries
- [LayerZero Bridge Vulnerabilities](../../bridge/layerzero/LAYERZERO_VULNERABILITIES.md)
- [Wormhole Bridge Vulnerabilities](../../bridge/wormhole/WORMHOLE_VULNERABILITIES.md)
- [Hyperlane Bridge Vulnerabilities](../../bridge/hyperlane/HYPERLANE_VULNERABILITIES.md)
- [Signature Vulnerabilities](../../general/signature/signature-vulnerabilities.md)

---

## Prevention Guidelines

### Development Best Practices
1. Always maintain a strict whitelist for cross-chain executor targets — never allow calls to config/registry contracts
2. Keeper/validator management must be governed by timelock + governance, never by keepers themselves
3. Use EIP-712 typed signatures with `chainId` and `address(this)` in the domain separator
4. Require M-of-N threshold signatures where M > N/2 for all bridge operations
5. Implement rate limiting and per-transaction caps on bridge transfers

### Testing Requirements
- Unit tests for: cross-chain executor target restriction, rejection of privileged targets
- Integration tests for: keeper addition requiring governance, signature replay across chains
- Invariant tests for: keeper set cannot be modified through cross-chain messages
